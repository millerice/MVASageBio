#!/usr/bin/env python3
"""cross_review.py —— 交叉审核 runner：按 docs/11 协议把五轮 prompt + 白名单材料
打包发往 OpenAI 兼容 API，输出落盘 data/processed/cross_review/（gitignored），
并自动登记 docs/llm-usage.log。

用法:
    python3 src/track2_repurposing/cross_review.py check            # 校验 prompt 解析与白名单文件
    python3 src/track2_repurposing/cross_review.py R4               # 跑单轮
    python3 src/track2_repurposing/cross_review.py all              # 顺序跑（R4→R1→R2→R3→R5）
    python3 src/track2_repurposing/cross_review.py R4 --dry-run     # 组装 prompt 落盘预览，不调 API 不记账

配置（.env，已 gitignored；模板 .env.example）:
    CROSS_REVIEW_BASE_URL    OpenAI 兼容端点（自动补 /v1；已含 /v数字 结尾则不补）
    CROSS_REVIEW_API_KEY     密钥（绝不入 git，本脚本绝不打印）
    CROSS_REVIEW_MODEL       模型名
    CROSS_REVIEW_TERMS_ACK   必须为 I_HAVE_VERIFIED —— 红线 #3 的机器门
                             （表示你已核对该服务为 Processor 型：不训练/不取得数据权利/限时留存）
    CROSS_REVIEW_MAX_TOKENS  可选，默认 16384

    多服务商写法：CROSS_REVIEW_PROVIDER=deepseek|qwen|glm 时改读对应 CROSS_<NAME>_* 块
    （含 TERMS_ACK——各家条款分开核对、独立放行）；不设 provider 用上面单块旧写法

设计约束:
    - prompt 单一来源 = docs/11 的 ```text 代码块；手改文档即生效，runner 不存副本
    - 材料白名单硬编码于 ROUNDS；data/ 下路径一律拒绝（基因组红线双保险）
    - 原始输出进 gitignored 区；是否入账由人工分诊（docs/cross-review-findings-2026-09.md）
    - ⚠️ R1 需联网核源，普通 chat API 无浏览能力会大面积退化为 UNVERIFIABLE——
      R1 建议走带联网/Deep Research 类产品手动执行（prompt 照抄 docs/11 §3）
"""
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / 'docs/11-交叉审核协议.md'
OUT_DIR = ROOT / 'data/processed/cross_review'
USAGE_LOG = ROOT / 'docs/llm-usage.log'
ENV = ROOT / '.env'

# 材料白名单（alias, 仓库相对路径）。改动需同步更新 docs/11 §1 的表格。
ROUNDS = {
    'R1': dict(web=True, files=[
        ('report.md', 'reports/JiuTian-Bio_track2_report.md'),
        ('evidence.jsonl', 'research/evidence.jsonl'),
        ('plan.md', 'docs/10-数据实验计划.md')]),
    'R2': dict(web=False, files=[
        ('report.md', 'reports/JiuTian-Bio_track2_report.md'),
        ('mechanism_chain.json', 'research/mechanism_chain.json')]),
    'R3': dict(web=False, files=[
        ('report.md', 'reports/JiuTian-Bio_track2_report.md'),
        ('rules.py', 'references/official/tabs/rules.py'),
        ('evaluation.py', 'references/official/evaluation.py')]),
    'R4': dict(web=False, files=[
        ('report.md', 'reports/JiuTian-Bio_track2_report.md')]),
    'R5': dict(web=False, files=[
        ('report.md', 'reports/JiuTian-Bio_track2_report.md')]),
}
RUN_ORDER = ['R4', 'R1', 'R2', 'R3', 'R5']


def load_env():
    cfg = {}
    if not ENV.exists():
        return cfg
    for line in ENV.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        cfg[k.strip()] = v.strip().strip('"').strip("'")
    return cfg


# .env 多服务商块前缀（CROSS_REVIEW_PROVIDER 选择其一；条款确认门随块独立）
PROVIDERS = {'deepseek': 'CROSS_DEEPSEEK_', 'qwen': 'CROSS_QWEN_', 'glm': 'CROSS_GLM_'}


def resolve_cfg(cfg):
    """CROSS_REVIEW_PROVIDER=deepseek|qwen 时，把对应 CROSS_<NAME>_* 块映射为旧版
    CROSS_REVIEW_* 键（含 TERMS_ACK——各家条款需分别核对）；未设 provider 时按
    旧版单块写法原样返回，向后兼容。"""
    provider = cfg.get('CROSS_REVIEW_PROVIDER', '').strip().lower()
    if not provider:
        return cfg
    if provider not in PROVIDERS:
        sys.exit(f"✗ 未知 CROSS_REVIEW_PROVIDER: {provider}（可选: {', '.join(PROVIDERS)}）")
    resolved = {'CROSS_REVIEW_PROVIDER': provider}
    for suffix in ('BASE_URL', 'API_KEY', 'MODEL', 'TERMS_ACK', 'MAX_TOKENS'):
        if cfg.get(PROVIDERS[provider] + suffix):
            resolved['CROSS_REVIEW_' + suffix] = cfg[PROVIDERS[provider] + suffix]
    return resolved


def parse_prompts():
    """docs/11 的 ```text 代码块 = prompt 单一来源；按内容前缀识别，不依赖位置。"""
    blocks = re.findall(r'```text\n(.*?)\n```', DOC.read_text(encoding='utf-8'), re.S)
    found = {}
    for b in blocks:
        if b.startswith('GLOBAL RULES'):
            found['global'] = b
            continue
        m = re.match(r'ROUND (R[1-5]) —', b)
        if m:
            found[m.group(1)] = b
    missing = [k for k in ['global'] + list(ROUNDS) if not found.get(k)]
    if missing:
        sys.exit(f'✗ docs/11 prompt 解析失败，缺失: {missing}（检查 ```text 代码块是否被改动格式）')
    return found


def resolve_files(rnd):
    out = []
    for alias, rel in ROUNDS[rnd]['files']:
        if rel.startswith('data/'):
            sys.exit(f'✗ 红线：白名单试图包含 data/ 路径 {rel}')
        p = ROOT / rel
        if not p.exists():
            sys.exit(f'✗ 白名单文件缺失: {rel}')
        out.append((alias, p))
    return out


def build_prompt(prompts, rnd):
    parts = [prompts['global'], '', prompts[rnd], '',
             'ATTACHED MATERIALS (verbatim, one file per delimiter):']
    for alias, p in resolve_files(rnd):
        parts.append(f'\n===== FILE: {alias} =====\n'
                     f'{p.read_text(encoding="utf-8")}\n'
                     f'===== END FILE: {alias} =====')
    return '\n'.join(parts)


def call_api(cfg, prompt):
    base = cfg['CROSS_REVIEW_BASE_URL'].rstrip('/')
    if not re.search(r'/v\d+$', base):
        base += '/v1'
    url = base + '/chat/completions'
    payload = {
        'model': cfg['CROSS_REVIEW_MODEL'],
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.2,
        'max_tokens': int(cfg.get('CROSS_REVIEW_MAX_TOKENS') or 16384),
    }
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json',
                 'Authorization': f"Bearer {cfg['CROSS_REVIEW_API_KEY']}"})
    last = None
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', 'replace')[:2000]
            if e.code == 429 and attempt == 1:
                print(f'  429 限流，20s 后重试一次…')
                time.sleep(20)
                continue
            sys.exit(f'✗ HTTP {e.code} from {url}\n{body}')
        except Exception as e:  # 超时/网络抖动：重试一次
            last = e
            if attempt == 1:
                time.sleep(5)
    sys.exit(f'✗ API 调用失败（重试后）: {last}')


def run_round(rnd, prompts, cfg, dry=False):
    prompt = build_prompt(prompts, rnd)
    files = [a for a, _ in resolve_files(rnd)]
    n = len(prompt)
    print(f'\n[{rnd}] 材料: {", ".join(files)} | prompt {n:,} 字符（≈{n // 4:,} tokens）')
    if ROUNDS[rnd]['web']:
        print(f'[{rnd}] ⚠️ R1 需联网核源：普通 chat API 无浏览能力，多数条目会退化为 '
              f'UNVERIFIABLE——R1 建议改用带联网/Deep Research 类产品手动执行（prompt 照抄 docs/11 §3）')
    if dry:
        f = OUT_DIR / f'dry_run_{rnd}.txt'
        f.write_text(prompt, encoding='utf-8')
        print(f'[{rnd}] dry-run 完成 → {f.relative_to(ROOT)}（未调 API、未记账）')
        return
    print(f'[{rnd}] 调用 {cfg["CROSS_REVIEW_MODEL"]} @ {cfg["CROSS_REVIEW_BASE_URL"]} …（最长等 15 分钟）')
    resp = call_api(cfg, prompt)
    try:
        content = resp['choices'][0]['message']['content']
    except (KeyError, IndexError):
        sys.exit(f'✗ 响应结构异常: {json.dumps(resp, ensure_ascii=False)[:2000]}')
    usage = resp.get('usage', {})
    ts = datetime.now().strftime('%Y%m%d-%H%M')
    safe = re.sub(r'[^A-Za-z0-9._-]', '_', cfg['CROSS_REVIEW_MODEL'])
    out = OUT_DIR / f'{rnd}_{safe}_{ts}.md'
    header = (f'<!-- 交叉审核 {rnd} | model={cfg["CROSS_REVIEW_MODEL"]} | '
              f'base={cfg["CROSS_REVIEW_BASE_URL"]} | '
              f'{datetime.now().isoformat(timespec="seconds")} | usage={usage} -->\n\n')
    out.write_text(header + content, encoding='utf-8')
    print(f'[{rnd}] ✓ 输出 → {out.relative_to(ROOT)}（{len(content):,} 字符）')
    host = re.sub(r'^https?://', '', cfg['CROSS_REVIEW_BASE_URL']).split('/')[0]
    ack_name = ('CROSS_' + cfg['CROSS_REVIEW_PROVIDER'].upper() + '_TERMS_ACK'
                if cfg.get('CROSS_REVIEW_PROVIDER') else 'CROSS_REVIEW_TERMS_ACK')
    with open(USAGE_LOG, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d')} | {cfg['CROSS_REVIEW_MODEL']} via {host}"
                f"（交叉审核 runner） | Processor 型（{ack_name} 已确认核对） | "
                f"公开级材料（{', '.join(files)}；无受控数据） | "
                f"交叉审核 {rnd}，输出 {out.relative_to(ROOT)} |\n")
    print(f'[{rnd}] ✓ llm-usage.log 已登记')


def main():
    argv = [a for a in sys.argv[1:] if not a.startswith('--')]
    dry = '--dry-run' in sys.argv[1:]
    if not argv:
        sys.exit(__doc__)
    prompts = parse_prompts()
    if argv[0] == 'check':
        print('✓ prompt 解析: global + ' + ', '.join(ROUNDS))
        for rnd in ROUNDS:
            for alias, p in resolve_files(rnd):
                print(f'  {rnd}: {alias:<22} {p.relative_to(ROOT)} ({p.stat().st_size:,} B)')
        print('✓ check 通过（未调 API）')
        return
    rounds = RUN_ORDER if argv[0] == 'all' else [a.upper() for a in argv]
    for rnd in rounds:
        if rnd not in ROUNDS:
            sys.exit(f'✗ 未知轮次 {rnd}（可选: R1-R5 / all / check）')
    cfg = resolve_cfg(load_env())
    if not dry:
        p = (cfg.get('CROSS_REVIEW_PROVIDER') or '').strip().upper()
        pref = f"CROSS_{p or 'REVIEW'}_"
        missing = [pref + k for k in ('BASE_URL', 'API_KEY', 'MODEL')
                   if not cfg.get('CROSS_REVIEW_' + k)]
        if missing:
            sys.exit(f'✗ .env 缺 {missing}（当前 provider 块前缀 {pref}；模板见 .env.example；'
                     f'--dry-run 不需要配置）')
        if cfg.get('CROSS_REVIEW_TERMS_ACK') != 'I_HAVE_VERIFIED':
            sys.exit(f'✗ 红线 #3 未放行：请在 .env 设 {pref}TERMS_ACK=I_HAVE_VERIFIED\n'
                     '  （表示你已核对该服务为 Processor 型：不训练/不取得数据权利/限时留存）')
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for rnd in rounds:
        run_round(rnd, prompts, cfg, dry=dry)
        if rnd != rounds[-1]:
            time.sleep(3)


if __name__ == '__main__':
    main()
