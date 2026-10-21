# Codex

Category: ai-coding-tools · Topic ID: codex

## Sources

- [fetched] https://developers.openai.com/codex — redirected (308) to https://learn.chatgpt.com/docs, real content fetched from there.
- [fetched] https://roadmap.sh/claude-code/vs-codex — real comparison content.
- [could not fetch] https://www.youtube.com/playlist?list=PL4cUxeGkcC9iDBeA8IyR1IE1kl4w5IDEG — only a page-header title fragment, no playlist/video list content.

## Findings

**What it is**: OpenAI's AI development assistant, integrated into ChatGPT rather than a separate
product — available across desktop, mobile, web, CLI, IDE extensions, and cloud. Beyond coding:
computer use, voice, web search, image generation, scheduled/long-running tasks, and enterprise
features (security scanning, compliance, workspace analytics, role-based admin controls).

**vs. Claude Code, concrete differences** (roadmap.sh comparison): Codex supports both local
execution and async cloud task delegation to isolated environments; Codex is open source (Apache
2.0) vs. Claude Code's proprietary client; Codex supports multiple model providers (OpenAI,
Azure, Amazon Bedrock) vs. Claude Code's Anthropic-only models; context windows are comparable
(Claude Code 1M with auto-compaction at 200K, Codex 1.05M). **Session limits differ meaningfully**:
Claude Code enforces a 5-hour session limit on both Pro and Max plans; Codex Pro has no 5-hour
limit, though both have weekly caps.

**Direct relevance to this system — not abstract**: this session itself hit exactly this
limitation mid-task (a subagent spawned for a code review failed with a rate-limit error citing a
session-limit reset time). The roadmap.sh comparison's claim that "Codex Pro plans have no 5-hour
limit" is therefore a concrete, verified-relevant fact for anyone deciding which tool Cimcime (or
its subagents) should run on for long autonomous sessions — not just trivia.

**Use-case framing**: Claude Code is positioned for hands-on, step-by-step refactoring within one
long session on a large codebase; Codex for parallel task execution and teams wanting OpenAI
model flexibility across providers.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
