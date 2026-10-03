# 仓库公开前置扫描记录（红线 6 合规，2026-10-03）

- 扫描基线：HEAD `5a2eef7`（2026-09-22 13:44）+ 工作区未提交改动；执行 Claude Code（GPT-5.6
  无关，本扫描为本地 git 对象遍历，无数据外发）
- 覆盖面：全部 git 对象（`--batch-all-objects`，可达 292 + 不可达 38，共 330 blob）；
  refs 仅 `main` + `origin/main`，无 tag、无 stash；push 仅上传可达对象，不可达对象不上 GitHub

## 一、路径层（全历史提交过的文件名）

- `data/raw/`、`data/processed/`：**零文件曾经入库**（含全部历史版本）✓
- 基因组文件类型（vcf/bcf/bam/cram/sam/fastq/ped/fam/idat 等，含 .gz 变体）：零命中 ✓
- `evidence_private.jsonl`（私有附录）：从未入库 ✓——历史上入库的 .jsonl 仅
  `research/evidence.jsonl`（公开台账）与 `research/review_attestations.jsonl`
- 凭证类（.env 实值/.pem/id_rsa/.synapseConfig）：零命中；唯一路径命中 `.env.example`
  为模板（全部 API key 空值 + Processor 条款确认门设计）✓
- `.gitignore` 拦截验证：`data/raw/`、`data/processed/` 规则生效 ✓

## 二、内容层（逐 blob 字节扫描）

- VCF/SAM 头（`##fileformat=VCF`/`#CHROM	POS`/`##contig`/`@HD`）：零命中 ✓
- 坐标数据行（TSV/CSV/JSON 嵌入三种格式，含 `PROBAND01,<chrom>,<pos>` T1 数据行格式）：零命中 ✓
- JSON 坐标字段（`"pos": ≥5位数` 等）、AD 值：零命中 ✓
- T1 表头字样（`proband_id,chrom_1,pos_1`）24 处命中 = schema 描述文字（CLAUDE.md/AGENTS.md/
  官方模板/evaluation.py/台账 claim/EV 描述），非数据行 ✓
- 凭证特征 3 处 = 官方源码函数名 `hf_username_to_display_slug`，非 token ✓
- 最大对象 106 KB（evidence.jsonl 历史版本），无意外大文件 ✓

## 三、不可达对象专项（38 个，不会随 push 泄露）

- 37 个文本对象 = 台账/文档/脚本/日志的 amend 前旧版，坐标特征零命中 ✓
- 1 个 gzip tar（9 KB，9/15）= `q1_full_reference_recheck/` Q1 服务器任务包
  （parse_pileup.py + run_q1_full_reference.sh + README + pyc）：
  - `PROBAND01` 出现处 = bwa 读组 SM 标签（`@RG	ID:Q1FULL	SM:PROBAND01`），
    官方 schema 固定值，非患儿标识 ✓
  - 冒号格式坐标（`chr?:N:≥5位数`）复扫：零命中 ✓
  - 唯一 6 位连续数字 = .pyc 内 IEEE754 浮点尾数字节（0.3/0.8），非坐标 ✓

## 结论

**通过。** 全历史（含不可达对象）无基因组级数据、无私有附录内容、无 T1 答案坐标行、
无患儿可识别信息、无真实凭证。仓库满足红线 1/6 的公开条件。

## 公开落地复验（2026-10-03，用户 flip 后，全部匿名无凭证）

- GitHub API：`visibility: public` / `private: false`；远端 main HEAD = `0372ffb`（冻结批）
- raw 匿名拉取 `reports/JiuTian-Bio_track2_report.md`，sha256 =
  `7eb6037a423a50beebc94df2ee5e2cf36e624327a502583451fcb469ad8a534a`，
  与本地及 attestation 第 4 行绑定值**逐字节一致**——公开所见 = 审签版本
- 敏感路径 raw 匿名访问全 404：`submissions/track2/pitch-narration.zh.md`、
  `data/processed/evidence_private.jsonl`、`data/raw/`、`docs/17-*` 专家评审版
- attestation flip_gate（commit→push→public）满足；T2 提交前置条件齐备

## 遗留（非阻断）

- 38 个不可达对象留存本地（含 Q1 任务包 tar）；随 `git gc` 自然过期即可，无需主动清除
- 工作区待提交：docs/18（配音决策落定）、llm-usage.log（MiniMax 条目）、
  submissions/track2/ 留档与本文件；`pitch-narration.zh.md` 是否入库待定
