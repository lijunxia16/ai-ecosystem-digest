# AI Ecosystem Daily Digest | AI 生态每日报告 · 2026-07-01

**English** — Daily curated signals across CLI tools, agents, the open web, trending repos, and Hacker News. Each item includes a one-line bilingual takeaway and a primary link.

**中文** — 每日汇总 CLI 工具、智能体生态、公开网络信号、仓库趋势与 Hacker News 热点；每条含中英一句要点与原文链接。

**Today | 今日** — 314 item(s) in this run.

## 0) At a glance | 今日速览

- **CLI / 命令行工具**: 85
- **Agents / 智能体**: 96
- **Web / 官网与资讯**: 17
- **Trending / 趋势**: 86
- **HN / 社区**: 30

## 1) AI CLI | AI CLI 工具动态

*EN — release/pr/issue updates.*
*中文 — 围绕发布、PR 和 Issue 的活跃变化。*

### Highlights | 重点速览
1. **[BUG] Opus 4.8 (1M) stream hangs after first chunk since 2.1.154; 2.1.153 is last known good**  
   - **EN:** GitHub activity: [BUG] Opus 4.8 (1M) stream hangs after first chunk since 2.1.154; 2.1.153 is last known good  
   - **中文：** GitHub 动态：[BUG] Opus 4.8 (1M) stream hangs after first chunk since 2.1.154; 2.1.153 is last known good  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/72639](https://github.com/anthropics/claude-code/issues/72639)  
   - **Tone | 语气:** Critical / cautious / 偏谨慎 / 批评

2. **[BUG] Interactive session refuses to prompt for trust for projects with settings.json saying the ses**  
   - **EN:** GitHub activity: [BUG] Interactive session refuses to prompt for trust for projects with settings.json saying the session is not interactive  
   - **中文：** GitHub 动态：[BUG] Interactive session refuses to prompt for trust for projects with settings.json saying the session is not interactive  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/72547](https://github.com/anthropics/claude-code/issues/72547)  
   - **Tone | 语气:** Critical / cautious / 偏谨慎 / 批评

3. **[BUG] Claude Code v2.1.187 TUI periodic PTY writes prevent SageMaker Code Editor idle shutdown**  
   - **EN:** GitHub activity: [BUG] Claude Code v2.1.187 TUI periodic PTY writes prevent SageMaker Code Editor idle shutdown  
   - **中文：** GitHub 动态：[BUG] Claude Code v2.1.187 TUI periodic PTY writes prevent SageMaker Code Editor idle shutdown  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/72642](https://github.com/anthropics/claude-code/issues/72642)  
   - **Tone | 语气:** Critical / cautious / 偏谨慎 / 批评

4. **Streaming tool_use leaks raw invoke syntax ('court' + <invoke>) into chat and hangs on 'invoking' (D**  
   - **EN:** GitHub activity: Streaming tool_use leaks raw invoke syntax ('court' + <invoke>) into chat and hangs on 'invoking' (Desktop app, macOS, v2.1.193)  
   - **中文：** GitHub 动态：Streaming tool_use leaks raw invoke syntax ('court' + <invoke>) into chat and hangs on 'invoking' (Desktop app, macOS, v2.1.193)  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/72641](https://github.com/anthropics/claude-code/issues/72641)  
   - **Tone | 语气:** Critical / cautious / 偏谨慎 / 批评

5. **[BUG]  Trust store uses literal path-string matching without normalization — same directory re-promp**  
   - **EN:** GitHub activity: [BUG]  Trust store uses literal path-string matching without normalization — same directory re-prompts trust across path-separator/case variants and version upg  
   - **中文：** GitHub 动态：[BUG]  Trust store uses literal path-string matching without normalization — same directory re-prompts trust across path-separator/case variants and version upg  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/72640](https://github.com/anthropics/claude-code/issues/72640)  
   - **Tone | 语气:** Critical / cautious / 偏谨慎 / 批评

### More | 更多条目
- [[BUG] Anthropic embedded spyware in Claude Code](https://github.com/anthropics/claude-code/issues/72518) — *GitHub 动态：[BUG] Anthropic embedded spyware in Claude Code* / *GitHub activity: [BUG] Anthropic embedded spyware in Claude Code*
- [[Bug] /clean_gone skill uses incorrect git branch flags and broken awk](https://github.com/anthropics/claude-code/issues/72638) — *GitHub 动态：[Bug] /clean_gone skill uses incorrect git branch flags and broken awk* / *GitHub activity: [Bug] /clean_gone skill uses incorrect git branch flags and bro*
- [[BUG] Routine creation fails with HTTP 400: job_config translate rejec](https://github.com/anthropics/claude-code/issues/72635) — *GitHub 动态：[BUG] Routine creation fails with HTTP 400: job_config translate rejec* / *GitHub activity: [BUG] Routine creation fails with HTTP 400: job_config translat*
- [[BUG] Windows: Claude Code never executes configured hook commands — h](https://github.com/anthropics/claude-code/issues/72636) — *GitHub 动态：[BUG] Windows: Claude Code never executes configured hook commands — h* / *GitHub activity: [BUG] Windows: Claude Code never executes configured hook comma*
- [[BUG] policyHelper in /etc/claude-code/managed-settings.json is ignore](https://github.com/anthropics/claude-code/issues/72634) — *GitHub 动态：[BUG] policyHelper in /etc/claude-code/managed-settings.json is ignore* / *GitHub activity: [BUG] policyHelper in /etc/claude-code/managed-settings.json is*
- [[BUG] Claude Science Linux installer serves x86-64 build on ARM64 (aar](https://github.com/anthropics/claude-code/issues/72633) — *GitHub 动态：[BUG] Claude Science Linux installer serves x86-64 build on ARM64 (aar* / *GitHub activity: [BUG] Claude Science Linux installer serves x86-64 build on ARM*
- [Grep/Glob tools become unavailable for entire session (incl. subagents](https://github.com/anthropics/claude-code/issues/72632) — *GitHub 动态：Grep/Glob tools become unavailable for entire session (incl. subagents* / *GitHub activity: Grep/Glob tools become unavailable for entire session (incl. su*

## 2) AI Agents | 智能体与 OpenClaw 赛道

*EN — ecosystem collaboration and skills.*
*中文 — 关注生态协作、项目演进与 Skills 热度。*

### Highlights | 重点速览
1. **Feature Request: Document sub-agent hook inheritance semantics**  
   - **EN:** GitHub activity: Feature Request: Document sub-agent hook inheritance semantics  
   - **中文：** GitHub 动态：Feature Request: Document sub-agent hook inheritance semantics  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/72645](https://github.com/anthropics/claude-code/issues/72645)  
   - **Tone | 语气:** Neutral / 中性

2. **Feature Request: Document sub-agent hook inheritance semantics**  
   - **EN:** GitHub activity: Feature Request: Document sub-agent hook inheritance semantics  
   - **中文：** GitHub 动态：Feature Request: Document sub-agent hook inheritance semantics  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/72647](https://github.com/anthropics/claude-code/issues/72647)  
   - **Tone | 语气:** Neutral / 中性

3. **[BUG] Global --dangerously-skip-permissions before a subcommand is parsed as a prompt, breaking daem**  
   - **EN:** GitHub activity: [BUG] Global --dangerously-skip-permissions before a subcommand is parsed as a prompt, breaking daemon (re)spawn for 'claude agents' after auto-update  
   - **中文：** GitHub 动态：[BUG] Global --dangerously-skip-permissions before a subcommand is parsed as a prompt, breaking daemon (re)spawn for 'claude agents' after auto-update  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/72643](https://github.com/anthropics/claude-code/issues/72643)  
   - **Tone | 语气:** Critical / cautious / 偏谨慎 / 批评

4. **IDE slash-command palette doesn't index newly-added symlinked skills until window reload**  
   - **EN:** GitHub activity: IDE slash-command palette doesn't index newly-added symlinked skills until window reload  
   - **中文：** GitHub 动态：IDE slash-command palette doesn't index newly-added symlinked skills until window reload  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/72631](https://github.com/anthropics/claude-code/issues/72631)  
   - **Tone | 语气:** Neutral / 中性

5. **Unguarded `rm -rf` after a silently-failed `mv` causes irreversible data loss on a cloud-sync (file-**  
   - **EN:** GitHub activity: Unguarded `rm -rf` after a silently-failed `mv` causes irreversible data loss on a cloud-sync (file-provider) mount  
   - **中文：** GitHub 动态：Unguarded `rm -rf` after a silently-failed `mv` causes irreversible data loss on a cloud-sync (file-provider) mount  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/72625](https://github.com/anthropics/claude-code/issues/72625)  
   - **Tone | 语气:** Positive tone / 偏积极

### More | 更多条目
- [Orphaned background --fork-session worker runs for hours and is respaw](https://github.com/anthropics/claude-code/issues/72623) — *GitHub 动态：Orphaned background --fork-session worker runs for hours and is respaw* / *GitHub activity: Orphaned background --fork-session worker runs for hours and is*
- [Codex app setting to open external links without switching focus](https://github.com/openai/codex/issues/30773) — *GitHub 动态：Codex app setting to open external links without switching focus* / *GitHub activity: Codex app setting to open external links without switching focu*
- [Code review setup can pass stale merge-base, causing reviewers to insp](https://github.com/openai/codex/issues/30741) — *GitHub 动态：Code review setup can pass stale merge-base, causing reviewers to insp* / *GitHub activity: Code review setup can pass stale merge-base, causing reviewers *
- [perf(core): avoid duplicate first-turn filesystem discovery](https://github.com/openai/codex/pull/30670) — *GitHub 动态：perf(core): avoid duplicate first-turn filesystem discovery* / *GitHub activity: perf(core): avoid duplicate first-turn filesystem discovery*
- [fix(app): show unread for pending questions](https://github.com/anomalyco/opencode/pull/34684) — *GitHub 动态：fix(app): show unread for pending questions* / *GitHub activity: fix(app): show unread for pending questions*
- [fix(app): show unread for pending questions](https://github.com/anomalyco/opencode/pull/34684) — *GitHub 动态：fix(app): show unread for pending questions* / *GitHub activity: fix(app): show unread for pending questions*
- [docs(ecosystem): add Loop Engineering to Projects](https://github.com/anomalyco/opencode/pull/34679) — *GitHub 动态：docs(ecosystem): add Loop Engineering to Projects* / *GitHub activity: docs(ecosystem): add Loop Engineering to Projects*

## 3) AI Web | 官网资讯与研究更新

*EN — official websites and research.*
*中文 — 聚合官网公告、研究和产品页面更新。*

### Highlights | 重点速览
1. **fix: remove statsig.anthropic.com from init-firewall.sh**  
   - **EN:** GitHub activity: fix: remove statsig.anthropic.com from init-firewall.sh  
   - **中文：** GitHub 动态：fix: remove statsig.anthropic.com from init-firewall.sh  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/pull/72451](https://github.com/anthropics/claude-code/pull/72451)  
   - **Tone | 语气:** Neutral / 中性

2. **fix(core) Remove full text websocket trace**  
   - **EN:** GitHub activity: fix(core) Remove full text websocket trace  
   - **中文：** GitHub 动态：fix(core) Remove full text websocket trace  
   - **Link | 原文：** [https://github.com/openai/codex/pull/30757](https://github.com/openai/codex/pull/30757)  
   - **Tone | 语气:** Neutral / 中性

3. **support LiteLLM /model/info for provider model discovery**  
   - **EN:** GitHub activity: support LiteLLM /model/info for provider model discovery  
   - **中文：** GitHub 动态：support LiteLLM /model/info for provider model discovery  
   - **Link | 原文：** [https://github.com/openai/codex/issues/30760](https://github.com/openai/codex/issues/30760)  
   - **Tone | 语气:** Neutral / 中性

4. **[codex] Add configurable reasoning summary delivery**  
   - **EN:** GitHub activity: [codex] Add configurable reasoning summary delivery  
   - **中文：** GitHub 动态：[codex] Add configurable reasoning summary delivery  
   - **Link | 原文：** [https://github.com/openai/codex/pull/30752](https://github.com/openai/codex/pull/30752)  
   - **Tone | 语气:** Neutral / 中性

5. **fix(core) Remove full text websocket trace**  
   - **EN:** GitHub activity: fix(core) Remove full text websocket trace  
   - **中文：** GitHub 动态：fix(core) Remove full text websocket trace  
   - **Link | 原文：** [https://github.com/openai/codex/pull/30757](https://github.com/openai/codex/pull/30757)  
   - **Tone | 语气:** Neutral / 中性

### More | 更多条目
- [[codex] Add configurable reasoning summary delivery](https://github.com/openai/codex/pull/30752) — *GitHub 动态：[codex] Add configurable reasoning summary delivery* / *GitHub activity: [codex] Add configurable reasoning summary delivery*
- [[codex] retry compressed requests uncompressed](https://github.com/openai/codex/pull/30690) — *GitHub 动态：[codex] retry compressed requests uncompressed* / *GitHub activity: [codex] retry compressed requests uncompressed*
- [fix(llm): suppress lone `</think>` chunk at reasoning→tool boundary](https://github.com/anomalyco/opencode/pull/34698) — *GitHub 动态：fix(llm): suppress lone `</think>` chunk at reasoning→tool boundary* / *GitHub activity: fix(llm): suppress lone `</think>` chunk at reasoning→tool boun*
- [opencode acp mode ignores OPENCODE_CONFIG_CONTENT and OPENCODE_CONFIG_](https://github.com/anomalyco/opencode/issues/34638) — *GitHub 动态：opencode acp mode ignores OPENCODE_CONFIG_CONTENT and OPENCODE_CONFIG_* / *GitHub activity: opencode acp mode ignores OPENCODE_CONFIG_CONTENT and OPENCODE_*
- [fix(core): stop replaying stale GitHub Copilot Responses item IDs](https://github.com/anomalyco/opencode/pull/34686) — *GitHub 动态：fix(core): stop replaying stale GitHub Copilot Responses item IDs* / *GitHub activity: fix(core): stop replaying stale GitHub Copilot Responses item I*
- [feat(provider): use models.dev reasoning options](https://github.com/anomalyco/opencode/pull/34680) — *GitHub 动态：feat(provider): use models.dev reasoning options* / *GitHub activity: feat(provider): use models.dev reasoning options*
- [fix(llm): suppress lone `</think>` chunk at reasoning→tool boundary](https://github.com/anomalyco/opencode/pull/34698) — *GitHub 动态：fix(llm): suppress lone `</think>` chunk at reasoning→tool boundary* / *GitHub activity: fix(llm): suppress lone `</think>` chunk at reasoning→tool boun*

## 4) AI Trending | 趋势信号与主题标签

*EN — GitHub trending and topics.*
*中文 — 结合 Trending 与主题标签提炼信号。*

### Highlights | 重点速览
1. **Feature Request: Support mcp__* wildcard in PreToolUse hook matchers**  
   - **EN:** GitHub activity: Feature Request: Support mcp__* wildcard in PreToolUse hook matchers  
   - **中文：** GitHub 动态：Feature Request: Support mcp__* wildcard in PreToolUse hook matchers  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/72646](https://github.com/anthropics/claude-code/issues/72646)  
   - **Tone | 语气:** Critical / cautious / 偏谨慎 / 批评

2. **Feature Request: Support mcp__* wildcard in PreToolUse hook matchers**  
   - **EN:** GitHub activity: Feature Request: Support mcp__* wildcard in PreToolUse hook matchers  
   - **中文：** GitHub 动态：Feature Request: Support mcp__* wildcard in PreToolUse hook matchers  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/72644](https://github.com/anthropics/claude-code/issues/72644)  
   - **Tone | 语气:** Neutral / 中性

3. **Claude built unauthorized AWS compute infrastructure, deviating from approved architecture**  
   - **EN:** GitHub activity: Claude built unauthorized AWS compute infrastructure, deviating from approved architecture  
   - **中文：** GitHub 动态：Claude built unauthorized AWS compute infrastructure, deviating from approved architecture  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/72637](https://github.com/anthropics/claude-code/issues/72637)  
   - **Tone | 语气:** Neutral / 中性

4. **AskUserQuestion CJK text misalignment in terminal UI**  
   - **EN:** GitHub activity: AskUserQuestion CJK text misalignment in terminal UI  
   - **中文：** GitHub 动态：AskUserQuestion CJK text misalignment in terminal UI  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/72629](https://github.com/anthropics/claude-code/issues/72629)  
   - **Tone | 语气:** Critical / cautious / 偏谨慎 / 批评

5. **Session auto-archive should respect pending work**  
   - **EN:** GitHub activity: Session auto-archive should respect pending work  
   - **中文：** GitHub 动态：Session auto-archive should respect pending work  
   - **Link | 原文：** [https://github.com/anthropics/claude-code/issues/72630](https://github.com/anthropics/claude-code/issues/72630)  
   - **Tone | 语气:** Neutral / 中性

### More | 更多条目
- [Feature request: lightweight session archive for `claude --resume` (no](https://github.com/anthropics/claude-code/issues/72627) — *GitHub 动态：Feature request: lightweight session archive for `claude --resume` (no* / *GitHub activity: Feature request: lightweight session archive for `claude --resu*
- [Stop button unresponsive during long model output — needs force-interr](https://github.com/anthropics/claude-code/issues/72626) — *GitHub 动态：Stop button unresponsive during long model output — needs force-interr* / *GitHub activity: Stop button unresponsive during long model output — needs force*
- [Create Cha](https://github.com/anthropics/claude-code/pull/72543) — *GitHub 动态：Create Cha* / *GitHub activity: Create Cha*
- [Chrome Store unavailable from a Hong Kong IP address; this Chrome brow](https://github.com/openai/codex/issues/30762) — *GitHub 动态：Chrome Store unavailable from a Hong Kong IP address; this Chrome brow* / *GitHub activity: Chrome Store unavailable from a Hong Kong IP address; this Chro*
- [Codex app/CLI fail to reconnect after Wi-Fi switch on macOS, possibly ](https://github.com/openai/codex/issues/30777) — *GitHub 动态：Codex app/CLI fail to reconnect after Wi-Fi switch on macOS, possibly * / *GitHub activity: Codex app/CLI fail to reconnect after Wi-Fi switch on macOS, po*
- [bug(core) websockets metadata equivalence issue](https://github.com/openai/codex/pull/30770) — *GitHub 动态：bug(core) websockets metadata equivalence issue* / *GitHub activity: bug(core) websockets metadata equivalence issue*
- [[codex] Enable tool search for fallback models](https://github.com/openai/codex/pull/30765) — *GitHub 动态：[codex] Enable tool search for fallback models* / *GitHub activity: [codex] Enable tool search for fallback models*

## 5) AI HN | Hacker News 社区脉搏

*EN — community hot discussions.*
*中文 — 提取社区高热讨论并观察情绪。*

### Highlights | 重点速览
1. **From brain waves to words: a new path to communication without surgery**  
   - **EN:** HN discussion: From brain waves to words: a new path to communication without surgery  
   - **中文：** Hacker News 热议：From brain waves to words: a new path to communication without surgery  
   - **Link | 原文：** [https://ai.meta.com/blog/brain2qwerty-brain-ai-human-communication/?_fb_noscript=1](https://ai.meta.com/blog/brain2qwerty-brain-ai-human-communication/?_fb_noscript=1)  
   - **Tone | 语气:** Neutral / 中性

2. **Leanstral 1.5**  
   - **EN:** HN discussion: Leanstral 1.5  
   - **中文：** Hacker News 热议：Leanstral 1.5  
   - **Link | 原文：** [https://docs.mistral.ai/models/model-cards/leanstral-1-5-26-06](https://docs.mistral.ai/models/model-cards/leanstral-1-5-26-06)  
   - **Tone | 语气:** Neutral / 中性

3. **Show HN: My 13-year-old built an ant colony tracker**  
   - **EN:** HN discussion: Show HN: My 13-year-old built an ant colony tracker  
   - **中文：** Hacker News 热议：Show HN: My 13-year-old built an ant colony tracker  
   - **Link | 原文：** [https://formicarium.es/](https://formicarium.es/)  
   - **Tone | 语气:** Neutral / 中性

4. **Claude Sonnet 5 – benchmark results**  
   - **EN:** HN discussion: Claude Sonnet 5 – benchmark results  
   - **中文：** Hacker News 热议：Claude Sonnet 5 – benchmark results  
   - **Link | 原文：** [https://artificialanalysis.ai/models/claude-sonnet-5](https://artificialanalysis.ai/models/claude-sonnet-5)  
   - **Tone | 语气:** Neutral / 中性

5. **Godot will no longer accept AI-authored code contributions**  
   - **EN:** HN discussion: Godot will no longer accept AI-authored code contributions  
   - **中文：** Hacker News 热议：Godot will no longer accept AI-authored code contributions  
   - **Link | 原文：** [https://www.pcgamer.com/gaming-industry/open-source-game-engine-godot-will-no-longer-accept-ai-authored-code-contributions-we-cant-trust-heavy-users-of-ai-to-understand-their-code-enough-to-fix-it/](https://www.pcgamer.com/gaming-industry/open-source-game-engine-godot-will-no-longer-accept-ai-authored-code-contributions-we-cant-trust-heavy-users-of-ai-to-understand-their-code-enough-to-fix-it/)  
   - **Tone | 语气:** Neutral / 中性

### More | 更多条目
- [Panasonic's new residential CO₂ air-to-water heat pump:coeff of perfor](https://www.pv-magazine.com/2026/06/29/panasonic-launches-co%E2%82%82-air-to-water-heat-pump-with-coefficient-of-performance-of-6-1/) — *Hacker News 热议：Panasonic's new residential CO₂ air-to-water heat pump:coeff of p* / *HN discussion: Panasonic's new residential CO₂ air-to-water heat pump:coeff of p*
- [Trump's plan to redesign every .gov website leads to AI-designed horro](https://arstechnica.com/tech-policy/2026/06/trumps-plan-to-redesign-every-gov-website-leads-to-ai-designed-horrors/) — *Hacker News 热议：Trump's plan to redesign every .gov website leads to AI-designed * / *HN discussion: Trump's plan to redesign every .gov website leads to AI-designed *
- [AI Could Be the Railroad of the 21st Century. Brace Yourself](https://www.derekthompson.org/p/artificial-intelligence-could-be) — *Hacker News 热议：AI Could Be the Railroad of the 21st Century. Brace Yourself* / *HN discussion: AI Could Be the Railroad of the 21st Century. Brace Yourself*
- [The AI Mirage or Why I Think the Hype Can't Sustain Itself](https://louwrentius.com/the-ai-mirage-or-why-i-think-the-hype-cant-sustain-itself.html) — *Hacker News 热议：The AI Mirage or Why I Think the Hype Can't Sustain Itself* / *HN discussion: The AI Mirage or Why I Think the Hype Can't Sustain Itself*
- [How the AI bubble could pop and take down the global economy according](https://www.theregister.com/ai-and-ml/2026/06/29/how-the-ai-bubble-could-pop-and-take-down-the-global-economy-according-to-the-bis/5263793) — *Hacker News 热议：How the AI bubble could pop and take down the global economy acco* / *HN discussion: How the AI bubble could pop and take down the global economy acco*
- [AWS puts $1B into new AI unit to embed engineers with customers](https://www.cnbc.com/2026/06/30/aws-amazon-ai-forward-deployed-engineers.html) — *Hacker News 热议：AWS puts $1B into new AI unit to embed engineers with customers* / *HN discussion: AWS puts $1B into new AI unit to embed engineers with customers*
- [What kinds of bugs does AI generate?](https://blog.detail.dev/posts/ai-bug-types/) — *Hacker News 热议：What kinds of bugs does AI generate?* / *HN discussion: What kinds of bugs does AI generate?*


---
*— End of digest | 报告结束 —*
