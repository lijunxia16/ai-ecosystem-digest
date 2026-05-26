# AI Ecosystem Daily Digest | AI 生态每日报告 · 2026-05-26

**English** — Daily curated signals across CLI tools, agents, the open web, trending repos, and Hacker News. Each item includes a one-line bilingual takeaway and a primary link.

**中文** — 每日汇总 CLI 工具、智能体生态、公开网络信号、仓库趋势与 Hacker News 热点；每条含中英一句要点与原文链接。

**Today | 今日** — 318 item(s) in this run.

## 0) At a glance | 今日速览

- **CLI / 命令行工具**: 106
- **Agents / 智能体**: 74
- **Web / 官网与资讯**: 14
- **Trending / 趋势**: 94
- **HN / 社区**: 30

## 1) AI CLI | AI CLI 工具动态

*EN — release/pr/issue updates.*
*中文 — 围绕发布、PR 和 Issue 的活跃变化。*

### Highlights | 重点速览
1. **[BUG] --resume normalizes model ID, breaking custom API endpoints that require the original model na**  
   - **EN:** GitHub activity: [BUG] --resume normalizes model ID, breaking custom API endpoints that require the original model name  
   - **中文：** GitHub 动态：[BUG] --resume normalizes model ID, breaking custom API endpoints that require the original model name  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/62353](https://github.com/anthropics/claude-code/issues/62353)  
   - **Tone | 语气:** Critical / cautious / 偏谨慎 / 批评

2. **[Feature Request] Add command to manually mark task as finished in agents view**  
   - **EN:** GitHub activity: [Feature Request] Add command to manually mark task as finished in agents view  
   - **中文：** GitHub 动态：[Feature Request] Add command to manually mark task as finished in agents view  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/62351](https://github.com/anthropics/claude-code/issues/62351)  
   - **Tone | 语气:** Critical / cautious / 偏谨慎 / 批评

3. **[BUG] /copy in `claude agents` (FleetView) silently fails — toast shows success but OS clipboard is **  
   - **EN:** GitHub activity: [BUG] /copy in `claude agents` (FleetView) silently fails — toast shows success but OS clipboard is not updated (tmux + VS Code Remote SSH)  
   - **中文：** GitHub 动态：[BUG] /copy in `claude agents` (FleetView) silently fails — toast shows success but OS clipboard is not updated (tmux + VS Code Remote SSH)  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/62350](https://github.com/anthropics/claude-code/issues/62350)  
   - **Tone | 语气:** Critical / cautious / 偏谨慎 / 批评

4. **[BUG] Claude Code `-EncodedCommand` PowerShell Execution Blocked by EDR/AV — No Opt-Out Available**  
   - **EN:** GitHub activity: [BUG] Claude Code `-EncodedCommand` PowerShell Execution Blocked by EDR/AV — No Opt-Out Available  
   - **中文：** GitHub 动态：[BUG] Claude Code `-EncodedCommand` PowerShell Execution Blocked by EDR/AV — No Opt-Out Available  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/62348](https://github.com/anthropics/claude-code/issues/62348)  
   - **Tone | 语气:** Critical / cautious / 偏谨慎 / 批评

5. **[Bug Report] Unable to process request**  
   - **EN:** GitHub activity: [Bug Report] Unable to process request  
   - **中文：** GitHub 动态：[Bug Report] Unable to process request  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/62347](https://github.com/anthropics/claude-code/issues/62347)  
   - **Tone | 语气:** Critical / cautious / 偏谨慎 / 批评

### More | 更多条目
- [[Bug] Claude Code (Opus) repeatedly violated locked memory rules, caus](https://github.com/anthropics/claude-code/issues/62343) — *GitHub 动态：[Bug] Claude Code (Opus) repeatedly violated locked memory rules, caus* / *GitHub activity: [Bug] Claude Code (Opus) repeatedly violated locked memory rule*
- [[BUG] /goal stop hook "Prompt is too long" in long-conversation sessio](https://github.com/anthropics/claude-code/issues/62345) — *GitHub 动态：[BUG] /goal stop hook "Prompt is too long" in long-conversation sessio* / *GitHub activity: [BUG] /goal stop hook "Prompt is too long" in long-conversation*
- [Memory file duplication causes excessive token consumption](https://github.com/anthropics/claude-code/issues/62325) — *GitHub 动态：Memory file duplication causes excessive token consumption* / *GitHub activity: Memory file duplication causes excessive token consumption*
- [[BUG] Desktop app appears in dock but never opens on macOS Tahoe 26.2](https://github.com/anthropics/claude-code/issues/62333) — *GitHub 动态：[BUG] Desktop app appears in dock but never opens on macOS Tahoe 26.2* / *GitHub activity: [BUG] Desktop app appears in dock but never opens on macOS Taho*
- [[BUG] claude mcp add -e <KEY=VAL> <name> -- <cmd> still fails in 2.1.1](https://github.com/anthropics/claude-code/issues/62332) — *GitHub 动态：[BUG] claude mcp add -e <KEY=VAL> <name> -- <cmd> still fails in 2.1.1* / *GitHub activity: [BUG] claude mcp add -e <KEY=VAL> <name> -- <cmd> still fails i*
- [[BUG] Paste (Ctrl+Shift+V) broken in GNOME Terminal on Linux/Wayland —](https://github.com/anthropics/claude-code/issues/62340) — *GitHub 动态：[BUG] Paste (Ctrl+Shift+V) broken in GNOME Terminal on Linux/Wayland —* / *GitHub activity: [BUG] Paste (Ctrl+Shift+V) broken in GNOME Terminal on Linux/Wa*
- [[BUG] Desktop app crashes (exit code 3221225477) with Sonnet but not O](https://github.com/anthropics/claude-code/issues/62326) — *GitHub 动态：[BUG] Desktop app crashes (exit code 3221225477) with Sonnet but not O* / *GitHub activity: [BUG] Desktop app crashes (exit code 3221225477) with Sonnet bu*

## 2) AI Agents | 智能体与 OpenClaw 赛道

*EN — ecosystem collaboration and skills.*
*中文 — 关注生态协作、项目演进与 Skills 热度。*

### Highlights | 重点速览
1. **[Bug] Malformed tool calls in long sessions due to in-context few-shot poisoning**  
   - **EN:** GitHub activity: [Bug] Malformed tool calls in long sessions due to in-context few-shot poisoning  
   - **中文：** GitHub 动态：[Bug] Malformed tool calls in long sessions due to in-context few-shot poisoning  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/62344](https://github.com/anthropics/claude-code/issues/62344)  
   - **Tone | 语气:** Critical / cautious / 偏谨慎 / 批评

2. **Feature: Allow existing Claude sessions to communicate with each other**  
   - **EN:** GitHub activity: Feature: Allow existing Claude sessions to communicate with each other  
   - **中文：** GitHub 动态：Feature: Allow existing Claude sessions to communicate with each other  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/62334](https://github.com/anthropics/claude-code/issues/62334)  
   - **Tone | 语气:** Neutral / 中性

3. **feat: add sandbox filesystem example settings with allowSkillsWrites**  
   - **EN:** GitHub activity: feat: add sandbox filesystem example settings with allowSkillsWrites  
   - **中文：** GitHub 动态：feat: add sandbox filesystem example settings with allowSkillsWrites  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/pull/62261](https://github.com/anthropics/claude-code/pull/62261)  
   - **Tone | 语气:** Critical / cautious / 偏谨慎 / 批评

4. **tui: include exec sessions in resume list**  
   - **EN:** GitHub activity: tui: include exec sessions in resume list  
   - **中文：** GitHub 动态：tui: include exec sessions in resume list  
   - **Link | 原文：** [https://github.com/openai/codex/pull/24503](https://github.com/openai/codex/pull/24503)  
   - **Tone | 语气:** Neutral / 中性

5. **`.agents/` writes blocked even when added via `--add-dir` or in `writable_roots`**  
   - **EN:** GitHub activity: `.agents/` writes blocked even when added via `--add-dir` or in `writable_roots`  
   - **中文：** GitHub 动态：`.agents/` writes blocked even when added via `--add-dir` or in `writable_roots`  
   - **Link | 原文：** [https://github.com/openai/codex/issues/24461](https://github.com/openai/codex/issues/24461)  
   - **Tone | 语气:** Critical / cautious / 偏谨慎 / 批评

### More | 更多条目
- [tui: include exec sessions in resume list](https://github.com/openai/codex/pull/24503) — *GitHub 动态：tui: include exec sessions in resume list* / *GitHub activity: tui: include exec sessions in resume list*
- [fix(tui): prevent macos stderr from corrupting composer](https://github.com/openai/codex/pull/24459) — *GitHub 动态：fix(tui): prevent macos stderr from corrupting composer* / *GitHub activity: fix(tui): prevent macos stderr from corrupting composer*
- [feat(core): add configurable per-tool-call timeout (tools.callTimeout)](https://github.com/google-gemini/gemini-cli/pull/27423) — *GitHub 动态：feat(core): add configurable per-tool-call timeout (tools.callTimeout)* / *GitHub activity: feat(core): add configurable per-tool-call timeout (tools.callT*
- [feat(skill): add `hidden` frontmatter field to skills](https://github.com/anomalyco/opencode/pull/29193) — *GitHub 动态：feat(skill): add `hidden` frontmatter field to skills* / *GitHub activity: feat(skill): add `hidden` frontmatter field to skills*
- [Question: review queue summary for issue-focused PRs](https://github.com/anomalyco/opencode/issues/29298) — *GitHub 动态：Question: review queue summary for issue-focused PRs* / *GitHub activity: Question: review queue summary for issue-focused PRs*
- [fix(config): catch parse errors gracefully during startup](https://github.com/anomalyco/opencode/pull/29208) — *GitHub 动态：fix(config): catch parse errors gracefully during startup* / *GitHub activity: fix(config): catch parse errors gracefully during startup*
- [feat: add simplify built-in skill](https://github.com/anomalyco/opencode/pull/29280) — *GitHub 动态：feat: add simplify built-in skill* / *GitHub activity: feat: add simplify built-in skill*

## 3) AI Web | 官网资讯与研究更新

*EN — official websites and research.*
*中文 — 聚合官网公告、研究和产品页面更新。*

### Highlights | 重点速览
1. **docs: Document CLAUDE_CODE_ATTRIBUTION_HEADER for custom base URL setups**  
   - **EN:** GitHub activity: docs: Document CLAUDE_CODE_ATTRIBUTION_HEADER for custom base URL setups  
   - **中文：** GitHub 动态：docs: Document CLAUDE_CODE_ATTRIBUTION_HEADER for custom base URL setups  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/pull/62346](https://github.com/anthropics/claude-code/pull/62346)  
   - **Tone | 语气:** Neutral / 中性

2. **Auto-memory subsystem writes to MEMORY.md mid-turn, invalidating Edit-tool read snapshots**  
   - **EN:** GitHub activity: Auto-memory subsystem writes to MEMORY.md mid-turn, invalidating Edit-tool read snapshots  
   - **中文：** GitHub 动态：Auto-memory subsystem writes to MEMORY.md mid-turn, invalidating Edit-tool read snapshots  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/62336](https://github.com/anthropics/claude-code/issues/62336)  
   - **Tone | 语气:** Critical / cautious / 偏谨慎 / 批评

3. **docs: Document CLAUDE_CODE_ATTRIBUTION_HEADER for custom base URL setups**  
   - **EN:** GitHub activity: docs: Document CLAUDE_CODE_ATTRIBUTION_HEADER for custom base URL setups  
   - **中文：** GitHub 动态：docs: Document CLAUDE_CODE_ATTRIBUTION_HEADER for custom base URL setups  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/pull/62346](https://github.com/anthropics/claude-code/pull/62346)  
   - **Tone | 语气:** Neutral / 中性

4. **feat(tui): add OSC 8 web links to rich content**  
   - **EN:** GitHub activity: feat(tui): add OSC 8 web links to rich content  
   - **中文：** GitHub 动态：feat(tui): add OSC 8 web links to rich content  
   - **Link | 原文：** [https://github.com/openai/codex/pull/24472](https://github.com/openai/codex/pull/24472)  
   - **Tone | 语气:** Neutral / 中性

5. **fix(provider): inline openai-compatible tool refs**  
   - **EN:** GitHub activity: fix(provider): inline openai-compatible tool refs  
   - **中文：** GitHub 动态：fix(provider): inline openai-compatible tool refs  
   - **Link | 原文：** [https://github.com/anomalyco/opencode/pull/29295](https://github.com/anomalyco/opencode/pull/29295)  
   - **Tone | 语气:** Critical / cautious / 偏谨慎 / 批评

### More | 更多条目
- [fix(provider): inline openai-compatible tool refs](https://github.com/anomalyco/opencode/pull/29295) — *GitHub 动态：fix(provider): inline openai-compatible tool refs* / *GitHub activity: fix(provider): inline openai-compatible tool refs*
- [fix(models): refresh raw model-derived defaults](https://github.com/QwenLM/qwen-code/pull/4517) — *GitHub 动态：fix(models): refresh raw model-derived defaults* / *GitHub activity: fix(models): refresh raw model-derived defaults*
- [fix(core): emit enable_thinking on DashScope when reasoning is disable](https://github.com/QwenLM/qwen-code/pull/4505) — *GitHub 动态：fix(core): emit enable_thinking on DashScope when reasoning is disable* / *GitHub activity: fix(core): emit enable_thinking on DashScope when reasoning is *
- [fix(core): stabilize DeepSeek tool cache prefix](https://github.com/QwenLM/qwen-code/pull/4518) — *GitHub 动态：fix(core): stabilize DeepSeek tool cache prefix* / *GitHub activity: fix(core): stabilize DeepSeek tool cache prefix*
- [fix(core): stabilize DeepSeek tool cache prefix](https://github.com/QwenLM/qwen-code/pull/4518) — *GitHub 动态：fix(core): stabilize DeepSeek tool cache prefix* / *GitHub activity: fix(core): stabilize DeepSeek tool cache prefix*
- [fix(models): refresh raw model-derived defaults](https://github.com/QwenLM/qwen-code/pull/4517) — *GitHub 动态：fix(models): refresh raw model-derived defaults* / *GitHub activity: fix(models): refresh raw model-derived defaults*
- [fix(core): emit enable_thinking on DashScope when reasoning is disable](https://github.com/QwenLM/qwen-code/pull/4505) — *GitHub 动态：fix(core): emit enable_thinking on DashScope when reasoning is disable* / *GitHub activity: fix(core): emit enable_thinking on DashScope when reasoning is *

## 4) AI Trending | 趋势信号与主题标签

*EN — GitHub trending and topics.*
*中文 — 结合 Trending 与主题标签提炼信号。*

### Highlights | 重点速览
1. **VSCode extension: /goal preview text fills the chat panel and pushes assistant responses out of view**  
   - **EN:** GitHub activity: VSCode extension: /goal preview text fills the chat panel and pushes assistant responses out of view until user types  
   - **中文：** GitHub 动态：VSCode extension: /goal preview text fills the chat panel and pushes assistant responses out of view until user types  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/62352](https://github.com/anthropics/claude-code/issues/62352)  
   - **Tone | 语气:** Neutral / 中性

2. **Add /cancel to clear queued messages without interrupting the running task**  
   - **EN:** GitHub activity: Add /cancel to clear queued messages without interrupting the running task  
   - **中文：** GitHub 动态：Add /cancel to clear queued messages without interrupting the running task  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/62349](https://github.com/anthropics/claude-code/issues/62349)  
   - **Tone | 语气:** Neutral / 中性

3. **Context compaction silently destroys terminal scroll history**  
   - **EN:** GitHub activity: Context compaction silently destroys terminal scroll history  
   - **中文：** GitHub 动态：Context compaction silently destroys terminal scroll history  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/62316](https://github.com/anthropics/claude-code/issues/62316)  
   - **Tone | 语气:** Neutral / 中性

4. **`/terminal-setup` claims "Switched to visual bell" but leaves Terminal.app with no bell at all**  
   - **EN:** GitHub activity: `/terminal-setup` claims "Switched to visual bell" but leaves Terminal.app with no bell at all  
   - **中文：** GitHub 动态：`/terminal-setup` claims "Switched to visual bell" but leaves Terminal.app with no bell at all  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/62342](https://github.com/anthropics/claude-code/issues/62342)  
   - **Tone | 语气:** Neutral / 中性

5. **ccd_session_mgmt archive_session: bulk archive forces per-session prompts**  
   - **EN:** GitHub activity: ccd_session_mgmt archive_session: bulk archive forces per-session prompts  
   - **中文：** GitHub 动态：ccd_session_mgmt archive_session: bulk archive forces per-session prompts  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/62154](https://github.com/anthropics/claude-code/issues/62154)  
   - **Tone | 语气:** Neutral / 中性

### More | 更多条目
- [Fix hookify event filtering in pre/post hooks](https://github.com/anthropics/claude-code/pull/62315) — *GitHub 动态：Fix hookify event filtering in pre/post hooks* / *GitHub activity: Fix hookify event filtering in pre/post hooks*
- [fix: prevent dedupe from suggesting or auto-closing as duplicate of cl](https://github.com/anthropics/claude-code/pull/62262) — *GitHub 动态：fix: prevent dedupe from suggesting or auto-closing as duplicate of cl* / *GitHub activity: fix: prevent dedupe from suggesting or auto-closing as duplicat*
- [feat: add block-build-commands hook example for hard execution guardra](https://github.com/anthropics/claude-code/pull/62264) — *GitHub 动态：feat: add block-build-commands hook example for hard execution guardra* / *GitHub activity: feat: add block-build-commands hook example for hard execution *
- [Pr test](https://github.com/anthropics/claude-code/pull/62252) — *GitHub 动态：Pr test* / *GitHub activity: Pr test*
- [Website](https://github.com/openai/codex/issues/24509) — *GitHub 动态：Website* / *GitHub activity: Website*
- [[codex-analytics] Add analytics for rejected turn/start requests](https://github.com/openai/codex/pull/24488) — *GitHub 动态：[codex-analytics] Add analytics for rejected turn/start requests* / *GitHub activity: [codex-analytics] Add analytics for rejected turn/start request*
- [[codex-analytics] Add analytics for rejected turn/start requests](https://github.com/openai/codex/pull/24488) — *GitHub 动态：[codex-analytics] Add analytics for rejected turn/start requests* / *GitHub activity: [codex-analytics] Add analytics for rejected turn/start request*

## 5) AI HN | Hacker News 社区脉搏

*EN — community hot discussions.*
*中文 — 提取社区高热讨论并观察情绪。*

### Highlights | 重点速览
1. **Uber’s COO says it’s getting harder to justify money spent on tokenmaxxing**  
   - **EN:** HN discussion: Uber’s COO says it’s getting harder to justify money spent on tokenmaxxing  
   - **中文：** Hacker News 热议：Uber’s COO says it’s getting harder to justify money spent on tokenmaxxing  
   - **Link | 原文：** [https://www.businessinsider.com/uber-coo-andrew-macdonald-ai-token-spending-harder-justify-2026-5](https://www.businessinsider.com/uber-coo-andrew-macdonald-ai-token-spending-harder-justify-2026-5)  
   - **Tone | 语气:** Neutral / 中性

2. **Using AI to write better code more slowly**  
   - **EN:** HN discussion: Using AI to write better code more slowly  
   - **中文：** Hacker News 热议：Using AI to write better code more slowly  
   - **Link | 原文：** [https://nolanlawson.com/2026/05/25/using-ai-to-write-better-code-more-slowly/](https://nolanlawson.com/2026/05/25/using-ai-to-write-better-code-more-slowly/)  
   - **Tone | 语气:** Neutral / 中性

3. **A successful Japanese trial of a ramjet engine designed for Mach‑5 aircraft**  
   - **EN:** HN discussion: A successful Japanese trial of a ramjet engine designed for Mach‑5 aircraft  
   - **中文：** Hacker News 热议：A successful Japanese trial of a ramjet engine designed for Mach‑5 aircraft  
   - **Link | 原文：** [https://www.bgr.com/2178211/japan-hypersonic-engine-ramjet-2-hour-flights-to-us/](https://www.bgr.com/2178211/japan-hypersonic-engine-ramjet-2-hour-flights-to-us/)  
   - **Tone | 语气:** Neutral / 中性

4. **Show HN: OpenBrief – Local-first video downloader/summarizer**  
   - **EN:** HN discussion: Show HN: OpenBrief – Local-first video downloader/summarizer  
   - **中文：** Hacker News 热议：Show HN: OpenBrief – Local-first video downloader/summarizer  
   - **Link | 原文：** [https://github.com/tantara/openbrief](https://github.com/tantara/openbrief)  
   - **Tone | 语气:** Neutral / 中性

5. **I'm the CEO of Goldman Sachs. The AI Job Apocalypse Is Overblown**  
   - **EN:** HN discussion: I'm the CEO of Goldman Sachs. The AI Job Apocalypse Is Overblown  
   - **中文：** Hacker News 热议：I'm the CEO of Goldman Sachs. The AI Job Apocalypse Is Overblown  
   - **Link | 原文：** [https://www.nytimes.com/2026/05/22/opinion/ai-job-crisis-goldman-sachs.html](https://www.nytimes.com/2026/05/22/opinion/ai-job-crisis-goldman-sachs.html)  
   - **Tone | 语气:** Neutral / 中性

### More | 更多条目
- [Every Frontier AI Is INTJ](https://zonted.com/posts/every-ai-is-intj/) — *Hacker News 热议：Every Frontier AI Is INTJ* / *HN discussion: Every Frontier AI Is INTJ*
- [Linus Torvalds Is Unhappy About the AI Influence in Linux Kernel Devel](https://ostechnix.com/linus-torvalds-ai-influence-linux-kernel-development/) — *Hacker News 热议：Linus Torvalds Is Unhappy About the AI Influence in Linux Kernel * / *HN discussion: Linus Torvalds Is Unhappy About the AI Influence in Linux Kernel *
- [Agentic Patterns](https://veso.ai/research/agentic-patterns/) — *Hacker News 热议：Agentic Patterns* / *HN discussion: Agentic Patterns*
- [Citing Gandalf, Pope Leo says we must "disarm" AI](https://arstechnica.com/tech-policy/2026/05/citing-gandalf-pope-leo-says-we-must-disarm-ai/) — *Hacker News 热议：Citing Gandalf, Pope Leo says we must "disarm" AI* / *HN discussion: Citing Gandalf, Pope Leo says we must "disarm" AI*
- [Cox Media fined after bragging it spied on users through their phones](https://www.theverge.com/policy/937027/cox-media-marketing-ai-powered-phone-spying-ads-ftc-fine) — *Hacker News 热议：Cox Media fined after bragging it spied on users through their ph* / *HN discussion: Cox Media fined after bragging it spied on users through their ph*
- [Show HN: PhoneDiffusion – Local AI image generation for iOS](https://apps.apple.com/us/app/phonediffusion/id6762061991) — *Hacker News 热议：Show HN: PhoneDiffusion – Local AI image generation for iOS* / *HN discussion: Show HN: PhoneDiffusion – Local AI image generation for iOS*
- [AI scans 400k Reddit posts and finds hidden Ozempic side effects](https://www.sciencedaily.com/releases/2026/05/260523103914.htm) — *Hacker News 热议：AI scans 400k Reddit posts and finds hidden Ozempic side effects* / *HN discussion: AI scans 400k Reddit posts and finds hidden Ozempic side effects*


---
*— End of digest | 报告结束 —*
