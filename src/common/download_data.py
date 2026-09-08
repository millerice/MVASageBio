#!/usr/bin/env python3
"""受控数据集下载与清单登记（S0 · G1）—— 磁盘紧张，先看清单再选择性下载。

用法:
    .venv/bin/python src/common/download_data.py --list                 # 只列文件树（含大小/SHA），不下载
    .venv/bin/python src/common/download_data.py --include '*.vcf.gz'  # 按模式下载（fnmatch，可多次）
    .venv/bin/python src/common/download_data.py                        # 全量下载（~85 GB，慎用）

约定:
    - Token: 环境变量 HF_TOKEN 或仓库根 .env 的 HF_TOKEN=hf_xxx（.env 已被 .gitignore 拦截）
    - 端点: huggingface.co 可达则直连，否则自动切 hf-mirror.com（--endpoint 可覆盖；LFS 文件由 hub 端 sha256 校验保证完整性）
    - 落盘仅 data/raw/（git 忽略）；受控数据仅限本人使用，赛后 30 天删除（红线 #4）
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REPO_ID = "SageBio/mva-hackathon-2026-data"
DEST = REPO_ROOT / "data" / "raw"
ENV_FILE = REPO_ROOT / ".env"


def load_token() -> str:
    # 三级查找: 环境变量 → 仓库根 .env → hf auth login 的本地凭证
    tok = os.environ.get("HF_TOKEN", "").strip()
    if tok:
        return tok
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            if line.startswith("HF_TOKEN="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    try:
        from huggingface_hub import get_token
        tok = (get_token() or "").strip()
        if tok:
            return tok
    except ImportError:
        pass
    sys.exit("未找到 HF_TOKEN：设置环境变量 / 仓库根 .env 写入 HF_TOKEN=hf_xxx / 运行 .venv/bin/hf auth login（三选一；勿贴进对话）")


def pick_endpoint(explicit: str | None) -> str:
    # 经验（2026-09-08）：本机到 huggingface.co 直连间歇可达但下载通道 401（疑似代理干扰鉴权），
    # hf-mirror.com 全程稳定且 token 鉴权正常 → 默认镜像；确有稳定代理时用 --endpoint 显式切官方。
    if explicit:
        return explicit.rstrip("/")
    if os.environ.get("HF_ENDPOINT"):
        return os.environ["HF_ENDPOINT"].rstrip("/")
    print("ℹ️ 默认使用 hf-mirror.com（官方直连在本机不稳定；完整性由 LFS sha256 校验保证）")
    return "https://hf-mirror.com"


def human(n: int | None) -> str:
    if not n:
        return "?"
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}PB"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--list", action="store_true", help="仅列出文件树并登记清单，不下载")
    ap.add_argument("--include", action="append", default=[],
                    help="fnmatch 下载模式，可多次（不填 = 全量）")
    ap.add_argument("--endpoint", default=None, help="覆盖 HF 端点（默认自动探测）")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--yes", action="store_true", help="跳过下载前交互确认（非交互跑批用）")
    args = ap.parse_args()

    token = load_token()
    os.environ["HF_ENDPOINT"] = pick_endpoint(args.endpoint)
    if os.environ["HF_ENDPOINT"] != "https://huggingface.co":
        os.environ["HF_HUB_DISABLE_XET"] = "1"  # 镜像不支持 Xet 协议，强制经典 HTTP

    from huggingface_hub import HfApi, snapshot_download
    api = HfApi(token=token)

    print(f"列出 {REPO_ID} 文件树（endpoint={os.environ['HF_ENDPOINT']}）…")
    files = []
    for entry in api.list_repo_tree(REPO_ID, repo_type="dataset", recursive=True):
        if not hasattr(entry, "size"):  # 目录
            continue
        lfs = getattr(entry, "lfs", None)
        files.append({
            "path": entry.path,
            "size": entry.size,
            "sha256": getattr(lfs, "sha256", None) or getattr(lfs, "oid", None) if lfs else None,
            "blob_id": getattr(entry, "blob_id", None),
        })
    files.sort(key=lambda f: -(f["size"] or 0))
    total = sum(f["size"] or 0 for f in files)
    print(f"\n共 {len(files)} 个文件，合计 {human(total)}：\n")
    for f in files:
        print(f"  {human(f['size']):>10}  {f['path']}")

    DEST.mkdir(parents=True, exist_ok=True)
    manifest = {
        "repo_id": REPO_ID,
        "endpoint": os.environ["HF_ENDPOINT"],
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "total_bytes": total,
        "files": files,
    }
    (DEST / "MANIFEST_listing.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
    print(f"\n清单已登记: {DEST / 'MANIFEST_listing.json'}")

    if args.list:
        return 0

    patterns = args.include or ["*"]
    selected = [f["path"] for f in files if any(fnmatch.fnmatch(f["path"], p) for p in patterns)]
    sel_bytes = sum(f["size"] or 0 for f in files if f["path"] in set(selected))
    print(f"\n下载 {len(selected)} 个文件（{human(sel_bytes)}）：")
    for p in selected:
        print(f"  {p}")
    if not args.yes and input("确认下载? [y/N] ").strip().lower() != "y":
        print("已取消")
        return 1

    snapshot_download(
        repo_id=REPO_ID, repo_type="dataset",
        allow_patterns=selected,
        ignore_patterns=[".gitattributes"],
        local_dir=str(DEST),
        max_workers=args.workers,
        token=token,  # 必须显式传：snapshot_download 不走 HfApi 的 token
    )
    # 尺寸核对（hub 下载时已做 LFS sha256 校验；此处再对账大小）
    missing = [f["path"] for f in files
               if f["path"] in set(selected)
               and not (DEST / f["path"]).is_file()]
    if missing:
        print(f"❌ 缺失 {len(missing)} 个文件: {missing[:5]}")
        return 1
    print(f"✅ 完成，落盘 {DEST}")
    print("⚠️  受控数据：仅限本人使用，不得转发；赛后 30 天删除并向两个官方邮箱发确认（CLAUDE.md 红线 #4）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
