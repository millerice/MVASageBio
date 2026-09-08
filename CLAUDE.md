# CLAUDE.md — MVASageBio 项目指令

MVA 黑客松 2026 参赛项目（Sage Bionetworks × MVA Society × Hugging Face × BEACON）。
截止 **2026-10-24 23:59 UTC**。调研报告与架构见 `docs/00–04`，里程碑验收见 `docs/05`，证据台账在 `research/evidence.jsonl`。

## 合规红线（违反即出局，优先级最高）

1. **基因组数据绝不入 git**：`data/raw`、`data/processed` 已被 .gitignore 拦截；任何 VCF/BAM/CRAM/基因组级基因型表不得进入仓库、提交物或公开报告
2. **不转发数据、不 recontact**：受控数据集仅限本人使用；不得联系患儿家庭、家族成员或 MVA Society 任何联系人
3. **LLM 使用**：仅向 Processor 型服务（不训练、不取得数据权利、限时留存）发送数据；不给模型输出点评分/反馈；使用 credits 前先读 credits 附加条款；数据交互记录到 `docs/llm-usage.log`；methods 报告必须含披露行
4. **赛后 30 天**删除全部原始 + 基因组级衍生数据，并发送确认邮件：**主送 `MVAHackathon2026@synapse.org`**（数据集门禁表单，用户 2026-09-08 决定），抄送 `RarediseaserealkidMVAhackathon2026@synapse.org`（Rules 页 L64 明文要求，且注明 30 天未联系会被主动追联）——两处官方来源不一致（EV-0032）（删除/保留清单见 docs/01 §6）
5. **T2 只提名已上市药物**（market-approved），全部产出不得出现治疗建议措辞
6. GitHub 评审开始前公开；公开前自检无基因组级数据
7. 提交物 CC-BY；发表带官方致谢段；禁稿期内不投稿使用本数据集的论文

## 证据规则

**来源分级**：

| Tier | 来源类型 | 例 |
|---|---|---|
| 0 | 官方页面 / 规则 / 源码 / 公告 / 官方讨论回复 | Space 的 `evaluation.py`、讨论 #18 |
| 1 | 权威生物医学库 / 同行评审 | OMIM、Orphanet、PMC、FDA、ClinicalTrials.gov |
| 2 | 学术机构 / 疾病基金会 | MVA Society |
| 3 | 社区 / 代码库 | GitHub、非官方讨论帖 |
| 4 | 博客 / 媒体 / 论坛 | — |

**标注规则**：每条关键 claim 标注 `fact / inference / hypothesis / strategic_opinion` 并入账 `research/evidence.jsonl`（schema 见 `research/README.md`）。

**冲突检测**：用户前提、网页、数据库之间有矛盾必须主动指出，不得迎合。范例：用户提示「BUB1B 与 MVA 2 型」——实际 BUB1B = MVA1、CEP57 = MVA2（EV-0017）。

**Reporter 隔离**：终版报告（T1 methods / T2 报告）只能引用证据台账中的 EV 编号生成，禁止写作时临场补充未入账事实。

## 医学安全

主角是真实患儿，所有产出公开（CC-BY）。药物重定位内容只能以 research hypothesis 表述（附可检验预测与反面证据），**不得写成治疗建议**；医学措辞检查是 T2 提交前必过项。

## 技术事实速查（已源码级验证，勿重复考证）

- 参考基因组 **GRCh38**（讨论 #17）
- T1 答案 = **comp-het 双变异，必须写在同一行**（chrom_1..alt_2 齐全）才是 full match；只命中一个 = 档位半分
- T1 评分档位：第 1 名 100 / ≤3 名 50 / ≤5 名 25 / ≤10 名 10；F-max 为变异级 epcr 阈值扫描
- T1 每人 6 次（取最高分，每次返回 full/partial/no match 反馈）；T2 共 3 次**只审最新**
- T1 CSV 12 列：`proband_id,chrom_1,pos_1,ref_1,alt_1,chrom_2,pos_2,ref_2,alt_2,epcr,finding_type,notes`；proband 固定 `PROBAND01`；≤10 行；epcr ∈ (0,1]
- T2 必交：报告（含变异机制刻画）+ GitHub URL + 3 分钟视频链接
- 榜单数据存私有数据集，公开页面抓取不到；战况以官方讨论区公告为准
- T1 表单除 CSV 外**必须**同时给 GitHub URL（https://github.com/ 前缀）+ 报告（.pdf/.md）（EV-0029）
- **数据集**（EV-0033~0035）：8×FASTQ(~79GB，未下载) + WGS VCF(315MB，GATK/GRCh38/未定相/无注释) + 临床表型 docx；无 BAM——read-backed 定相需自比对（磁盘不足，届时走云端）；HPO 8 词条已提取（EV-0036）
- **VCF contig 无 chr 前缀**（1/2/…/X）；提交 CSV 必须 chr 前缀（模板与答案键风格，评分前缀敏感）——S6 打包时强制转换（EV-0034）
- 本机网络：HF 官方域名走本地代理 `127.0.0.1:7890`（HTTPS_PROXY）；hf-mirror 可列目录但 gated 大文件 302 回官方 CDN；源码镜像获取已官方复核 7/7 一致（EV-0038）
- **提交物一律英文**：官方无明文语言要求（源码 grep 零命中），但 methods 表单（xlsx）本身是英文结构化问卷、评审方为 SageBio/国际评委——对提交面的产物（CSV notes/报告/表单/视频）全部英文；中文仅限内部工作文档（CLAUDE.md/docs/台账）。官方 methods 表单（references/official/static/templates/）为 A 列问题 B 列作答结构，**A10 生成式 AI 披露为必填项**
- gnomAD v4.1 无 af-only 发布；可行战术 = bcftools 经代理按基因区域远程拉切片（~70s/基因），v4.1 INFO 自带 AF/CADD/REVEL/SpliceAI/VEP；候选级全新变异注释走 Ensembl VEP REST；SnpEff 数据库下载被 Azure 阻断（Java 代理参数也无效）

## 工作方式

- 分阶段开发，一阶段一验收（Exit Gate 见 `docs/05`），不跳门
- T1/T2 终版提交前：本地评分 harness 全绿 + 子代理对抗审查（claim 溯源审计 + 医学措辞检查）
- 不为「看起来高级」增加基础设施（无 Docker / 向量库 / 自建 Agent 框架）；可运行 > 可验证 > 可扩展
- 每次提交留档 `submissions/`（时间、配额消耗、官方反馈、分数）
