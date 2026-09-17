# 交叉审核发现与分诊 · 2026-09

按 docs/11 协议对 R1–R5 审核输出的修/缓/驳分诊记录。
本文件是人工分诊的权威记录；审核原始输出在 `data/processed/cross_review/`（gitignored）。

## 批次状态

| 批次 | 时间 | 模型 | 状态 |
|---|---|---|---|
| 第一批 R4/R2/R3/R5 | 2026-09-17 17:42–17:43 | deepseek-chat | ✅ 已分诊（本文） |
| 第二批 R4/R2/R3/R5 | 2026-09-17 17:55–17:56 | qwen-max | ✅ 已分诊（本文） |
| 修订批次 A1–A21 | 2026-09-17（用户批准后执行） | — | ✅ 已执行：报告 28 处编辑 + 机制链 6 节点降 inference + report_claims.tsv 锚点同步（CL-004/CL-007）；lint / validate_chain / validate_all 重跑全绿，摘要 498/500 词 |
| R4 复审 #1 | 2026-09-17 18:30 | deepseek-chat | ⚠️ FAIL（24 条，性质已软化为就地 hedge 密度；反证 tokenism 核查六处全过）→ D1–D11 分诊修订已落地，摘要 499/500 |
| R4 复审 #2 | 2026-09-17 18:33 | deepseek-chat | ⚠️ FAIL（实质 10 条，裁决挂 2 处：摘要 bridge / 表格 age 1）→ E1–E9 落地（含 C4 括注补课），摘要 494/500 |
| R4 复审 #3 | 2026-09-17 18:36 | deepseek-chat | ⚠️ FAIL（25 条：实质改进 + 重翻已对冲项 + 1 条审查者虚构 #7）→ F1–F15 分诊落地，摘要 499/500 |
| R4 复审 #4（终轮） | 2026-09-17 18:42 | deepseek-chat | ❌ FAIL（22 条）→ loop-guard 触发终止 → **用户 2026-09-17 批准人工裁决结案**（采纳 #19/#20/#17，驳回 19 条存档 F 节末） |
| R1 引文核验 | 2026-09-17 | ChatGPT Deep Research（手动联网） | ✅ 已执行并分诊（G1–G7；REFUTED 1 + OVERSTATED 3 + 报告越界 3 → 全部修订落地；C 项两条支柱阴性声明活查存活） |

两次 API 批次均已登记 `docs/llm-usage.log`（DeepSeek 4 行 + qwen 4 行，Provider 条款门各自确认）。

## 审核者质量核验（分诊前置）

- 分诊前对本方仓库做了抽查：R3 引用的 A12 措辞（report L274）、§0 私有材料披露句、
  R2 引用的 SAC enhancer 强阴性句（L148–150）**全部真实存在**（初查两处"疑似幻觉"系
  本方 grep 被换行拆句所误，非审核者虚构）。
- 机制链 N4/N7/N9/N11/N13/N14 的 fact 类型标注已对照 `research/mechanism_chain.json` 确认。
- 报告全文零次出现 N14（grep 确认），而摘要写 "14 nodes"——R2 的呈现不一致指控成立。
- **双模型质量不对称**（影响下文裁决权重）：qwen-max 四轮输出显著偏浅（R2 912 字符 vs
  DeepSeek 7,828；R3 零发现全 pass，与 A12 矛盾客观存在相悖；R4 仅扫摘要判 PASS）。DeepSeek
  为分析主力；qwen 的价值在于对核心问题簇的**独立收敛**（N3/N5、场景分离、蠕虫平台、
  niacinamide 缺口五点全与 DeepSeek 重合）。单侧发现按 docs/11 §4 由人工裁决。

## 分诊结果

### A. 修（本次修订批次，约 20 项）

| # | 来源 | 发现 | 处置 |
|---|---|---|---|
| A1 | R3-d F1 | A12 "publicly available sources only"（L274）与 §0 "not an exclusively public-material workflow" 直接矛盾 | §4 A12 改为「公开来源 + 经 hackathon 许可的受控数据集（仅 §1 基因型刻画）；受控材料未进公开仓库」 |
| A2 | R3-d F2 + R4-d#3 + R5-q#3 | niacinamide 无已验证单方上市产品，不满足 market-approved 硬门槛，不应占提名位 | 从 §2 提名表移入「excluded — fails market-approval gate」（与 NMN/AICAR/17-AAG 同列）；§2.1 与摘要同步改口径 |
| A3 | R2-d（本方核验确认） | N4/N7/N9/N11/N13/N14 标 fact 但 counter_note 自认未在相关系统验证——系统性类型误标 | 六节点降为 inference；重跑 ledger/chain 校验器；报告 §1.2 图注同步 |
| A4 | R2-d（核验确认） | §1.2 链图止于 N13，N14 仅存在于 JSON；摘要称 14 nodes | §1.2 图补 N14（SIRT2–NAD+ 轴） |
| A5 | R2-d N11 | everolimus "direct target engagement" 与 "disease-model bridge" 未分离，前者是事实后者是推断 | §2.3 措辞分离两者（见驳回 #1：不重算排名） |
| A6 | R2-d | "no pharmacological SAC enhancer exists anywhere in the literature"（L148–150）强于 EV-0068 的检索范围 | 改 "in the published literature we searched [EV-0068]" |
| A7 | R3-d F7 | §0 自述私有材料对 LLM 工具可见，但未声明 safeguards | §0 加一句：材料全程在参与者控制的计算环境内、仅 Processor 型服务、未向任何第三方授予数据访问 |
| A8 | R3-d F8 | 30 天删除义务、确认邮件、embargo 未在报告体现 | §5 或 §6 加一句义务声明 |
| A9 | R4-d 裁决驱动项 + R4-q#1/3/4/5 收敛 | 摘要与 §2 表多处可被读作获益/推荐（"selected two eligible candidates"、"highest-ranked eligible hypothesis"、探针/平台句） | §2 表头与摘要各加一句统一免责；#6/#12 类排名语言改为 "falsification-priority" 表述 |
| A10 | R5-d① + R5-q#1 收敛 | trans 构型仅为推断且未定相 | §1.1 顶部加条件句：基因型为官方确认的变异对级 comp-het，相位未测，下游机制推理以 trans 为前提 |
| A11 | R2-d N3/软肋1 | Mao 2003 激酶活性少数派观点只在 counter_note，未在正文展开对 L1 的证伪含义 | §1.3 加一句：若激酶缺陷（而非丰度）观成立，L1 轴机制上失效 |
| A12 | R2-d 软肋5 + R4-d#4 | L1 证据缺口（衰老小鼠、非 MVA 突变体）在 §1.3/§2.1/摘要的论证使用点未随句携带 | 每处使用点加 "in BubR1-insufficient aging mice, not MVA mutants" 类限定 |
| A13 | R2-d 软肋2/N5 + R2-q 最弱环节收敛 | 13%/6% 阈值被用作可操作药理学目标 | 使用点降为定性方向 + "model-derived, not measured in this proband"；数字仅出现在来源标注处 |
| A14 | R4-d#7–9 + R2-q §3 收敛 | §3 预测表 "improves/raises" 获益动词缺模型限定 | 逐条加 "in C. elegans only" 前缀 + 中性化动词；患者细胞路线标注 "laboratory assay only" |
| A15 | R2-d 软肋4 | chloroquine 预测要求肿瘤选择性窗口，但蠕虫平台无肿瘤，不可执行 | 该行标注需哺乳动物转化/非转化细胞对，移出蠕虫平台表或明确 platform mismatch |
| A16 | R4-d#17–19 | 三条反证过于模糊/内部术语（"growth uncertainty"、"DS endpoints differ"、"two major transfers"） | 具体化改写（保留 EV 引用） |
| A17 | R4-d#16 | "therapeutic window" 可误读为治疗窗口 | 改 "selectivity window" |
| A18 | R5-d③ | metformin 的 DS→MVA 病因学鸿沟未论证 | §2.2 加 transfer-gap 段（三点差异 + 为何 AMPK 轴或可跨病因复用/或承认纯探索性） |
| A19 | R5-d④ | everolimus TSC 儿科经验 ≠ MVA 疗效机制外推 | §2.3 区分「药代/ADR 谱可外推」vs「疗效机制不可外推」，后者写入 §3 falsification 条件 |
| A20 | R5-d② + R2-d 软肋3 | 300/300 模拟呈现可被读作排除性证据；场景分离回避了时序权衡 | §6.6 的 300/300 降格为一句限制性解读；§2.2 承认同一干预的时序权衡而非独立场景 |
| A21 | R4-d#22 | §6.5 交叉引用 §2.4 只覆盖 chloroquine，儿科安全反证实际在 §2.1–2.4 | 改 §2.1–2.4 |

### B. 缓（冻结/提交时处理，已有跟踪）

| # | 来源 | 事项 | 时点 |
|---|---|---|---|
| B1 | R3-d F4 | GitHub URL 插入 §5 | 报告冻结（附"评审开始时公开"注记） |
| B2 | R3-d F5 | 3 分钟视频链接 | M4 视频完成后、冻结前 |
| B3 | R3-d F6 | 数据集官方引用 | 提交时（Synapse 页引用） |
| B4 | R3-d F3 | §0 披露 "remain pending" 措辞收尾 | ✅ 2026-09-17 完成（用户确认 OpenAI Data Controls 关闭后执行；见变更记录终收条） |
| B5 | R5-d⑤ | §7 接口规范表（输入→输出+人工介入时长） | 可选增强，冻结前有余力则做 |
| B6 | R5-d 影响 | "未给剂量/终点/试验设计" | 受医学措辞红线约束不展开；§3 实验室证伪步骤已是合规上限（见驳回 #2） |

### C. 驳（不采纳，附理由）

| # | 来源 | 要求 | 驳回理由 |
|---|---|---|---|
| C1 | R2-d N11 | N11 降 inference 后重算 everolimus 排名 | 评分度量证伪优先级（证据密度/可测性），节点类型不是评分输入；采纳措辞分离（A5）替代 |
| C2 | R5-d Impact | 给出剂量/终点/试验设计轮廓 | T2 规则与医学安全红线禁止治疗邻近性内容；跨线反而制造 R4 级风险 |
| C3 | R5-q #4 | "解决" 38.7% vs ~75% 癌症外显率冲突 | 冲突在文献层面，报告义务是披露与分级呈现（已做，EV-0049/0050/0051）；无本方数据可裁决 |
| C4 | R4-d#14 | MVA Society 资助句完整重写 | 采纳简短"非关联/非背书"括注，不用冗长版 |
| C5 | R4-d#15 | 全文 "candidate"→"hypothesis" 改名 | 与官方表单/rules.py 用语及管线产物（candidates_ranked.tsv）冲突；仅 §3 表内安全处采纳 |
| C6 | R5-q 总评 | 85/100 却判"不进短名单"，自相矛盾 | 内部不一致，评分参考 DeepSeek 批为主 |

### D. R4 复审分诊（2026-09-17 18:30，deepseek-chat，报告已含 A1–A21 修订）

复审结论仍为 **FAIL**（24 条），但性质变化显著：类别四（反证 tokenism 反向核查）六处全部
「无发现」——A16/A19/A20 的反证具体化被复审确认有效；剩余发现几乎全部为「就地 hedge 密度」
要求（表格单元/摘要单句级别的截图安全性）。分诊如下：

| # | 来源 | 处置 | 动作 |
|---|---|---|---|
| D1 | 复审#5 | **修** | §2.1 ONTRAC 剂量方案（500 mg bid ×12 月）从报告移除（台账 EV-0070 保留全量）；加「deliberately not reproduced」句 |
| D2 | 复审#1/2 | **修（表头级）** | §2 表头 hypothesis 列改 "Research hypothesis (abridged; not treatment advice)"——拒绝逐格加样板前缀（表格已有 Table note + 反证列同格可视，表头级 hedge 达到截图安全） |
| D3 | 复审#3 | **修** | chloroquine 格 "First test" → "First experiment (not a treatment)" + selectivity window |
| D4 | 复审#4 | **修** | §2.1 假设句改 "We hypothesize that … would enhance"（虚拟式）+ 标题加 not a treatment recommendation |
| D5 | 复审#6 | **修** | §2.3 SEGA 句后就地加「TSC/SEGA indication only … not as expected benefit in MVA」 |
| D6 | 复审#15 | **修** | §3 表头 Candidate → Research hypothesis；Prediction → Prediction (experiment design)（C5 的 §3 内安全改名范围） |
| D7 | 复审#16 | **修** | §3 引导句加「nomination = selection for falsification work, not selection of a drug for use」 |
| D8 | 复审#10 | **修** | 患者细胞路线改 "in vitro laboratory assay only" + "with and without … in culture" |
| D9/D10 | 复审#23/24 | **修** | 两条 ✗ 行的空 counter-evidence 格填充指向说明 |
| D11 | 复审#11/14 | **修（部分）** | 摘要首问句就地加 "as research hypotheses, not treatment options"；配套裁词保持 ≤500（终 499） |
| — | 复审#7/8/9 | **驳（部分）** | §3 各格已有 "predicted, in *C. elegans* only:" 前缀；表级 frame（D6+D7）已覆盖，逐格再加 "not a treatment protocol" 样板收益递减 |
| — | 复审#12 | **驳（实质已满足）** | 提名句紧邻前置 hedge「falsification-priority ordering, not an efficacy or benefit ranking」+ 句内 "research hypotheses" + 结尾总免责 + D11 首句 hedge，共四处分布；再加则超 500 词表单上限 |
| — | 复审#13 | **驳** | "retained only as … not a finalist" 同句后半即反证（no selective window has been shown）；「值得一试」误读需无视同句第二半，判定充分 |

D1–D11 已全部落地（校验器重跑全绿，摘要 499/500）。第三次 R4 确认跑进行中。

### E. R4 复审 #2 分诊（2026-09-17 18:33，deepseek-chat）

复审 #2 仍 **FAIL**（13 条，其中 3 条自查「无发现」= 实质 10 条），裁决理由明确挂在两处：
摘要 "closest disease-model bridge"（可读作「最接近可用」）与 §2 表 "SEGA from age 1"（可读作
「一岁就能用」）。发现 #8（§3 表整体格式）、#12（反证非 tokenism）、#13（摘要双重对冲）均自查
通过——D 批修订被确认有效。分诊：

| # | 来源 | 处置 | 动作 |
|---|---|---|---|
| E1 | #1（裁决项） | **修** | 摘要 "closest disease-model bridge" → "closest disease-model **evidence** bridge"（比较类从药物可用性改为证据距离） |
| E2 | #2 + C4 补课 | **修** | 摘要移除 "that the MVA Society itself funds"（机构背书误读）；§3 保留该事实并补 C4 已裁决的非背书括注（上批漏执行） |
| E3 | #3（裁决项） | **修** | §2 表 approval 格 → "approved for TSC-associated SEGA (age ≥1 yr) — pediatric exposure precedent only, not an MVA indication" |
| E4 | #4 | **修** | "First experiment (not a treatment)" → "Probe hypothesis (not a treatment, not a nomination)" |
| E5 | #5 | **修** | metformin 格补 "in either direction (scenario-dependent, untested in MVA)"（CL-005 锚点保留） |
| E6 | #6 | **修** | ONTRAC 效应量/CI/亚组统计移出报告（台账 EV-0070 保留全量）——与 D1 剂量移除同一逻辑：排除化合物章节不携带可记忆数字 |
| E7 | #7 | **修** | §2.3 "placing this hypothesis first … as a falsification priority" → "assigning … the highest falsification-priority score … — an ordering of which hypothesis to test first, not a ranking of expected benefit"（CL-004 锚点再同步） |
| E8 | #9 | **修** | §3 niacinamide 格 "NAD+ precursor exposure" 后加 "(research reagent, not a supplement)" |
| E9 | #10 | **修** | 患者细胞路线 "an NAD+ precursor (research-grade compound)" |
| — | #11 | **驳** | §7 "druggable property" 为药物发现术语（描述病变性质非患者行动），§7 为方法论章节、无药物命名；改 "researchable" 损失术语精度 |
| — | #8/12/13 | 复核通过 | 无动作 |

E1–E9 落地后：摘要 494/500；lint / validate_chain / validate_all 全绿。

### F. R4 复审 #3 分诊（2026-09-17 18:36，deepseek-chat）

复审 #3 仍 **FAIL**（25 条）。性质判定：本轮混合三类——(a) 真实残余改进（免责顺序前置、
模型系统限定、in vitro 标注）；(b) 对已对冲项的重翻（D/E 批已处理项的更高标准重提）；
(c) **1 条审查者虚构**（#7）。轨迹 22→24→10→25，且发现性质从「缺对冲」漂移到「对冲措辞
选词」再到「重翻已对冲项」——判定为对冲军备竞赛/标准漂移，进入 loop-guard：复审 #4 为
最后一次自动迭代，仍 FAIL 则转人工裁决。分诊：

| # | 来源 | 处置 | 动作 |
|---|---|---|---|
| F1 | 复审#3-#1 | **修** | §2 表 everolimus 格 → "Hypothesis from mouse models: mTORC1 inhibition may attenuate…(never tested in MVA)" |
| F2 | 复审#3-#2 | **修** | §2 表 metformin 格补 "model-system data only;"（CL-005 锚点保留格首） |
| F3 | 复审#3-#3 | **修** | §2 表 chloroquine 格 → "Probe hypothesis (in vitro only; not a treatment, not a nomination): a mammalian cell-triplet assay would test…" |
| F4 | 复审#3-#4 | **修** | §2.1 假设句锚定 "in an in-vitro assay of cells expressing the proband's genotype" |
| F5 | 复审#3-#5 | **修** | §2.2 → "scenario-limited and model-bound: modulating energy stress might improve…" |
| F6 | 复审#3-#6+#25 | **修** | §2.3 免责句前置（"cited solely as pediatric exposure and ADR precedent, not as expected benefit in MVA"）；"SEGA stable/reduced in 76%" 疗效数字移出正文（台账 EV-0079 指针） |
| F8 | 复审#3-#8 | **修** | §3 患者细胞路线 → "added to the culture dish only (no compound is administered to the patient)" |
| F9 | 复审#3-#9 | **修** | 摘要 "an experimental route to raising" → "a mechanism shown only in BubR1-insufficient aging mice (not MVA mutants) by which BUBR1 abundance might be raised"（合并括注，净 +3 词） |
| F10 | 复审#3-#10 | **修** | 摘要 everolimus 括注补 "in the eligible set, still untested in MVA"；metformin "cross-species protection"→"cross-species data"（去疗效暗示） |
| F11 | 复审#3-#11 | **修** | 摘要 "retained only as"→"listed only as"（CL-006 锚点 "high-risk mechanistic probe, not a finalist" 不受影响） |
| F12 | 复审#3-#13(半) | **修** | §3 niacinamide 格 "exposure"→"addition to the worm culture"（去毒理暴露误读） |
| F13 | 复审#3-#14 | **修** | §3 氯喹段 → "in-vitro mammalian cell-line triplet … with no in-vivo or patient testing" |
| F14 | 复审#3-#16 | **修** | §2 表 metformin 反证 "direction tension vs L3 clearance" → 展开为非术语可读形式 |
| F15 | 复审#3-#23 | **修** | §2 表 niacinamide ✗ 行 → "mechanistic rationale retained for hypothesis-testing only (§2.1)" |
| — | 复审#3-#7 | **驳（审查者虚构）** | 声称 everolimus §3 行缺 "predicted, in *C. elegans* only:" 前缀——grep 证伪：报告 L299 前缀在位，全文 3 处齐全。审查者引用时裁掉前缀后声称缺失。记录为发现生成压力下的虚构 |
| — | 复审#3-#12/#22 | **驳** | 摘要再加全局/就地免责句：500 词表单上限下不可行（当前 499）；摘要已有 5 处对冲分布 + F10 就地 "still untested in MVA"，密度已达上限 |
| — | 复审#3-#24 | **驳** | ONTRAC "reported a reduction" 改 "studied exposure"（零结果内容）会使引文科学上空洞——该试验被引用的唯一目的就是暴露先例；R4 提示词允许已引用文献的结果陈述；效应量/CI/剂量已按 D1/E6 移入台账，正文无任何可记忆数字 |
| — | 复审#3-#15/17–21 | 复核通过 | 反证 tokenism 反向检查 5/6 无发现（#16 已由 F14 处理） |

F1–F15 落地后：lint（90 条）/ validate_chain（14 节点 15 边）/ validate_all 全绿；摘要 499/500；
CL-001/004/005/006/007/009 锚点逐一复核在位。**复审 #4（终轮）按 loop-guard 启动。**

#### 复审 #4（终轮）结果与人工裁决案（2026-09-17 18:42，FAIL 22 条）

**Loop-guard 触发：R4 自动迭代终止。** 裁决依据（原始输出
`R4_deepseek-chat_20260917-1842.md`）：

1. **轨迹不收敛**：22→24→10→25→22。在报告逐批满足提示词自列标准后，发现数不归零、
   标准持续漂移（缺对冲 → 对冲选词 → 重翻已对冲项 → 标记审查者自己上轮建议的改写）。
2. **重翻自采纳文本（对冲军备竞赛直接证据，5 例）**：#3＝F1 原文（复审#3-#1 建议）、
   #4＝F2 原文（复审#3-#2 建议）、#5＝F3 原文（复审#3-#3 建议原句）、#8 的 "might improve"
   ＝复审#3-#5 建议动词、#6 的 "would enhance"＝复审#3-#4 建议改写原词。审查者对上一轮
   自己的处方再次判 FAIL，证明验收标准是「必须产出发现」而非「报告是否达标」。
3. **事实错误（1 例）**：#9 称 §2.3 免责句「位置偏后」——F6 后免责句已在数据句之前，文件在案。
4. **重翻已裁决驳回项（2 例）**：#13 重翻 E11（druggable property，方法论章节无药物命名）；
   #7 重翻 F 批 #24（ONTRAC）且新建议 "reported an outcome on" 信息量为零，反向验证驳回理由。
5. **提示词标准逐项审计（通过）**：就地 hedge 在位（全提名行均含模型限定 + untested in MVA）；
   hypothesis 框架在位（§2 表头 + 各行 + §2.1–2.4 小节级声明）；反证附着（本轮 #19/#20 补强
   后表格反证格自足，类别四自查通过项维持）；无超引用范围的剂量/时机建议（剂量/效应量已全部
   移台账）；无比较级 best/first-choice 获益暗示（"closest disease-model evidence bridge" 经
   E1+F10 两轮降格为证据距离表述并附 "still untested in MVA"，#1 要求的 "least distant" 改写
   在 500 词摘要预算内不可行且文体降级）。
6. **官方红线归属**：T2 rules.py 的 no-treatment-recommendation 检查属 R3 域（历轮 PASS）；
   R4 是本方自设的更严措辞标准，其提示词标准已全部满足。

**终局处置**：采纳 3 条（#19 everolimus 反证格前置 "No MVA-model or MVA-patient data exist"、
#20 metformin 反证格补 DS→MVA transfer gap、#17 metformin 证伪格补 "(trisomy models only;
not MVA)"——均为提示词类别四自身标准）；驳回 19 条（重翻 12 / 冗余 5 / 事实错误 1 / 词上限 1）。
落地后 lint / validate_chain / validate_all 全绿，摘要 499/500，CL 锚点全部在位。
**R4 以人工裁决结案：报告满足 R4 提示词全部自列标准；剩余发现为超提示词最大主义，驳回理由
如上存档。** 待用户签字确认后进入 R1（上传包须先以终版报告重新生成）。

### G. R1 引文核验分诊（2026-09-17，ChatGPT Deep Research，输出 `R1_output_chatgpt_2026-09-17.md`）

总览：42 条公开 EV 判定 **CONFIRMED 20 / OVERSTATED 3 / REFUTED 1 / UNVERIFIABLE 18**。
UNVERIFIABLE 均为预期不可核类（受控数据/私有计算、API 动态快照、文献访问受限、absence-based），
无一构成事实反证。**本方独立复核（分诊前置义务）**：REFUTED 项 PMID 26681807 efetch 确认
Huntington's disease（台账题录转录错误坐实）；EV-0079 引语逐字吻合且摘要 "longest" 零出现；
EV-0068 反例 poloxin（PMID 21839059）/simvastatin（PMID 38604342）题录逐字存在；**C 项
EV-0059 本方 ClinicalTrials.gov API v2 亲查双空集（2026-09-17）**——R1 关键判定全部经一手
证据确认后采纳。C 项两条支柱阴性声明均存活（带日期戳）。

| # | 来源 | 处置 | 动作 |
|---|---|---|---|
| G1 | EV-0073 **REFUTED** | **修（最高优先）** | 台账条目整体更正（疾病领域 HD、题录/evidence/counter_evidence 重写、更正注记、置信 0.9）；报告 §2.2 重构（DS 单层证据 + 台账误记披露 + 「无跨物种非整倍体链」明示）、摘要 metformin 括注 → "DS-cell mitochondrial data only"、§2 表反证格单层口径、§3 预测/证伪格同步；CL-005 species_model 同步 |
| G2 | EV-0047 OVERSTATED | **修** | 台账 claim 收窄（经典系列 2004–2010 + 2026-09-08 检索范围 + absence-based 声明）；报告 §1.1 → "absent from those series and from our 2026-09-08 search…not a permanent exclusion"；§1.2 链图 "architecture rule"→"reported architecture pattern" |
| G3 | EV-0068 OVERSTATED | **修** | 台账收窄为「无恢复型增强剂」口径；反例入账 EV-0093（poloxin）/EV-0094（simvastatin），题录 WebSearch + R1 双重复核；报告 §1.3 改收窄表述并引 EV-0093/0094 |
| G4 | EV-0079 OVERSTATED | **修** | 台账 + 报告 §2.3 去最高级（"the longest documented"→"a very long documented…cohort"；台账注记摘要未作最高级主张）；全部数字逐字确认保留 |
| G5 | EV-0057 报告越界 | **修** | 摘要 "mTORC1-driven"→"mTORC1-associated"（台账与 JCI 原文均为 correlating / may be a driver） |
| G6 | EV-0059 报告越界 | **修** | §6.5 去 "ever"、限定 ClinicalTrials.gov 范围、加 2026-09-17 复核日期戳；摘要本已带 (ClinicalTrials.gov query) 不动；台账 evidence 补两级独立复核记录 |
| G7 | EV-0054 报告越界 | **修** | §1.2 → "our PubMed search found no published MVA/BUB1B–nephrocalcinosis association (absence-based, as of 2026-09-08)" |
| — | EV-0023 UNVERIFIABLE | 无动作 | 台账 tier-2 记录 society 官网资助方向（2026-09-02 留档）；R1 未证伪仅未能独立复核资金关系；§3 已带非背书括注 |
| — | 其余 17 条 UNVERIFIABLE | 无动作 | 受控/私有计算（0039/0040/0042/0076/0085/0087/0089）、API 快照（0069）、FDA 标签未抓取（0078）、规则镜像映射（0082/0083）、文献访问受限（0051/0052/0055/0065）、absence-based（0054）——外部不可核属预期，无一事实反证 |
| — | 20 条 CONFIRMED | 复核通过 | 含 C 项 EV-0059 活查阴性维持；EV-0051 精确数字因 PMC 表格访问未复核（冲突披露义务已履行，未获反证） |

G1–G7 落地后：lint 92 条（EV-0001~0094）/ validate_chain / validate_all 全绿；摘要 497/500；
CL-001/004/005/006/007/009 锚点全部在位。**教训入账：题录级（esummary）入账必须 efetch 校验
疾病领域等关键限定词——EV-0073 错误即源于此。** B4（§0 "remain pending" 收尾）剩余范围收窄为
attestation + 服务条款核验。

## 修订执行顺序（用户批准后）

1. 报告 + 机制链 JSON + 台账按 A1–A21 一次批次编辑
2. 重跑 `ledger.py lint` + `validate_chain.py` + `validate_all.py`
3. R4 复审一次（DeepSeek）确认 FAIL→PASS
4. R1 输出并入分诊 → 终版收尾（claims 升格 independent_reviewed + review_attestations.jsonl + `--final` 门）

## 变更记录

- 2026-09-17 初建：DeepSeek + qwen-max 两批 API 轮分诊完毕（修 21 / 缓 6 / 驳 6）；R1 待执行。
- 2026-09-17 追记（用户批准后执行）：A1–A21 修订批次落地。要点：A2 将 niacinamide 移入 ✗ 排除行
  （market-approval gate）；A3 六节点（N4/N7/N9/N11/N13/N14）fact→inference 并在 §1.2 加图注声明
  JSON 为权威分级源；A4 图补 N14；A9 表注 + 摘要免责句，排名语言改 falsification-priority
  （CL-004 锚点同步）；A15 chloroquine 预测移出蠕虫表（哺乳动物三联细胞 + selectivity window，
  A17 全文 window 措辞统一）；A20 场景分离补时序权衡承认。摘要 498/500。
- 2026-09-17 再追记：R4 复审循环 #1–#3（D1–D11 / E1–E9 / F1–F15 三批分诊全部落地）。轨迹
  22→24→10→25，发现性质从「缺对冲」漂移到「重翻已对冲项 + 1 条虚构（#7，grep 证伪）」。
  Loop-guard 生效：复审 #4 为最后一次自动迭代，仍 FAIL 即转人工裁决。摘要 499/500。
- 2026-09-17 终局：复审 #4 FAIL 22 条 → loop-guard 触发，自动迭代终止。裁决：采纳 3 条反证
  格自足项（#19/#20/#17），驳回 19 条（5 例系复审 #4 标记复审 #3 自己建议的改写原文——对冲
  军备竞赛直接证据；1 例事实错误；2 例重翻已裁决驳回项）。**用户同日批准人工裁决结案。**
  `r1_upload/` 已用终版报告重新生成（含提示词 43→42 修正），R1 操作卡已交付，待用户执行。
- 2026-09-17 R1 收官：用户执行 ChatGPT Deep Research 引文核验（输出已归档）；本方完成四项
  独立复核（PMID 26681807 / Becker 引语 / poloxin+simvastatin 题录 / ClinicalTrials.gov API 亲查）
  后执行 G1–G7：台账 5 条修正 + 新增 EV-0093/0094（92 条）+ 报告 12 处 + tsv 1 处；
  校验全绿，摘要 497/500。**R1–R5 五轮交叉审核全部闭环。**
- 2026-09-17 终收（claims 升格 + attestation）：report_claims.tsv 全部 10 条
  `machine_checked` → `independent_reviewed`；`research/review_attestations.jsonl` 建档
  （绑报告 sha256 `9f9de7c9…74e5a`，记录 R1–R5 全部审者/日期/覆盖 + 人工裁决 +
  per-claim 覆盖说明 + 局限声明：独立审者为异提供商 LLM + 人工裁决、非同行评审；
  R1 会话账号侧条款核验仍开（B4）；attestation 严格绑定当前报告字节——
  **B1–B4 任何报告改动后须对新版本重新审签**）。`validate_all.py --final` **首次全绿**
  （0 failing gates）。
- 2026-09-17 B4 收尾：用户确认 OpenAI 账号 Data Controls（训练）已关闭后，报告 §0 三处重写
  （Recorded tools 补交叉审核服务 DeepSeek/Qwen/ChatGPT；per-service 条款核验收口——API 提供商
  按发布条款核 + OpenAI 账号侧参赛者自证，残余：不可独立审计、Codex 逐轮模型版本未记录；
  "remain pending" → 交叉审核已完成 + 残余局限声明「LLM 审者 + 人工裁决，非领域专家同行评审」）。
  git diff 确认改动仅限 §0（科学内容/锚点/摘要零改动）→ attestation 追加重审签行
  （sha256 2da17800…035cc，diff-scope-verified）；llm-usage.log R1 行补记 + 收尾节。
  `validate_all.py --final` 全绿。**B1–B6 中 B4 关闭；剩余 B1/B2/B3 冻结时点项 + B5 可选。**
