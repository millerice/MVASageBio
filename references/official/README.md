# references/official — 官方 Space 源码快照（Tier 0）

本地评分 harness（`src/track1_variant/scorer.py`）**直接 import 此处的 `evaluation.py` 作为评分内核**，不转写、不改逻辑。任何对此目录文件的改动都会影响本地评分结果——不要手改。

## 来源与获取渠道

- 仓库：https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026
- 获取日期：2026-09-08
- 渠道说明：本机直连 huggingface.co 超时，经 **hf-mirror.com 镜像**获取。**已于同日走本地代理从官方域名重取 7 份文件逐字节复核，sha256 全部一致（EV-0038）——完整性疑虑关闭。**

## 文件清单与 SHA256

| 文件 | 用途 | SHA256 |
|---|---|---|
| `evaluation.py` | **评分内核**（load_submission / score_proband / F-max） | `6d18b581e65a45e1ccc120071d588e740c2e42e983ff50704c60a40232b19180` |
| `groundtruth.py` | 答案加载器（真实答案在私有数据集，此处仅占位 fallback） | `650cddf36e7d08582df750f6d4a0cae241b59e295158e00fc4f218d7994846c6` |
| `config.py` | 配额（T1×6 / T2×3）、私有数据集名 | `a65e67fca2fb698ac3f3fe6610e585f549cf29f175d636ce77543d7db6dc8bdc` |
| `utils.py` | 提交留档/身份工具 | `b53ae3bbce7e0c9729f27a53f4e315e85590e4cdddce4155c5d966d6aed1d9e9` |
| `app.py` | Space 入口 | `ca3157b3a26653cd9af6777f97110ed15b7acdb6f7f0ae85b0ca20ba719f93ad` |
| `tabs/submit_track1.py` | T1 提交表单校验（GitHub URL + 报告必填） | `685a3b6d57ef3a1c49a8be47845b10d77cb576ed2d30b5a90879b09707659b86` |
| `tabs/submit_track2.py` | T2 提交表单 | （未单独校验，随包下载） |
| `static/templates/track1_submission_template.csv` | 官方 12 列提交模板 | `7b3ed41c091d34fb6c5622d049c7a3f46124211fc7ec02947e69daef8752755a` |
| `static/templates/methods_description_form.xlsx` | T1 methods 报告模板（S7 用） | （二进制，随包下载） |
| `*-tree.json` | HF API 文件树响应（来源凭证） | — |

对应证据条目：EV-0001~0003（2026-09-02 首批）、EV-0025~0030（2026-09-08 细读入账）。
