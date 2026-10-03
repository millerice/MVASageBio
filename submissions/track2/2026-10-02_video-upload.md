# T2 视频上传留档（2026-10-02）

## 链接

- YouTube：https://youtu.be/sKnrdGWi8o8
- 匿名可达性：✅ **已验证**（2026-10-03 复验：oEmbed 200 / 缩略图 200 / 播放页
  playabilityStatus=OK；Unlisted 生效）
- 标题：One child, zero trials, two testable hypotheses — JiuTian Bio | MVA Hackathon 2026
  Pitch（方案 A）；频道 knight white（个人账号，团队名在标题中，无合规问题）
- YouTube 侧时长：lengthSeconds=180，页面显示 3:00——本地母版实测 179.91 s，为 YouTube
  取整显示，实际未超 3:00
- 简介：已发布（致谢段 ✓ / CC-BY 行 ✓ / 关键词 6/8 / TTS 披露行 ✓——2026-10-03
  用户补加后复验在位）
- 许可设置：外部不可核（license 字段未随页返回）；简介行已声明 CC-BY 4.0，Studio 内
  改 Creative Commons 更佳但非必需

## 本地母版

- 文件：`~/Documents/JiuTian-Bio_track2_pitch_v1.mov`（仓库外，1920×1080，H.264+AAC，34 MB）
- 时长：**179.91 s（2:59.9）**，Spotlight 元数据实测；距 3:00 上限仅 0.09 s
  ——已建议剪片头/尾卡 2–4 s 落到 ~2:56，用户未确认是否执行；若未剪，成片=179.91 s

## 配音与披露（本批次新增义务，docs/18 §6 TTS 分支生效）

- 旁白 = **MiniMax TTS**（输入 = docs/18 §2 逐字稿 425 词，公开级，无受控数据）
- [x] llm-usage.log 条目（2026-10-02 已记：speech-2.8-hd 网页版；条款不及 Processor 型——
  平台 ToS 允许输入用于服务改进、无不训练承诺；因输入为公开级文稿判为已声明偏离，残余风险无）
- [x] methods 表单披露（2026-10-03 核实：无需单独操作——该题要求记入 methods description
  即报告本体，§0 Recorded tools + Addendum 已覆盖且入 0372ffb/attestation 7eb6037a；
  xlsx 非提交物。注：GenAI 必填问在 T2 表页是 A9 行，报告 §4 已映射 "A9 → §0"）
- [x] 报告 §0 Recorded tools 追加（B1–B3 批次一并完成，0372ffb）
- [ ] YouTube 合成内容申报勾「是（合成语音）」（外部不可核，Studio 内确认）
- [x] 简介补 TTS 披露行（2026-10-03 用户补加，复验在位）

## 后续

- 10/15 占坑提交 #1 引用本链接；此后仅换终版链接
- **B2**：报告当前**无**视频链接占位（grep 无 video/YouTube 引用）——插入时需新增一行，
  与 B1（GitHub URL，报告 §5）、B3（数据集引用，报告 §8 末行）同批，一并重审签
- .srt 英文字幕待上传（YouTube → Subtitles → English；§5 模板按幕时间码，需按成片实时刻度校准）
- 提交前 §8 自检单剩余项：听感核「research hypotheses, not treatment proposals」可闻、术语发音
