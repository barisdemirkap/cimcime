# Product Discovery and Prioritization

Category: ui-product-development · Topic ID: product-discovery-and-prioritization

## Sources

- [unverified] https://www.atlassian.com/agile/product-management — fetched twice; only site navigation came back, body truncated. Nothing about the article's content could be read.
- [fetched] https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/ — Intercom's RICE prioritization framework.

## Findings

All findings below come from the Intercom article only. The Atlassian article's content is not covered.

RICE is a scoring system for ranking roadmap ideas, built by Intercom because existing cost-benefit approaches made ideas hard to compare consistently. Factors:

- Reach: number of people affected in a defined period (e.g. customers per quarter). Use real metrics, not guesses; estimating from your own usage biases toward features you like.
- Impact: effect per person. Scale: Massive 3, High 2, Medium 1, Low 0.5, Minimal 0.25. Intercom measured it as conversion effect; other teams may use adoption or delight.
- Confidence: how well-supported the estimates are; guards against overrating exciting but vague ideas. High 100%, Medium 80%, Low 50%, below 50% is a "moonshot".
- Effort: total person-months across product, design, engineering; rough whole numbers (0.5 for well under a month). The only factor that lowers the score.

Formula (the article shows it as an image; the text implies it): (Reach x Impact x Confidence) / Effort, i.e. impact per time worked. Article examples (450/3/100%/2, 2000/1/80%/4, 800/2/50%/1) work out to about 675, 400, 800 by my calculation (not stated in the article), so the small-effort project 3 ranks first despite low confidence.

Usage guidance: sort and sanity-check scores, revise suspicious estimates. Scores are not a hard rule; dependencies or table-stakes work may go first. The value is making deliberate out-of-order trade-offs visible and explainable. Intercom used a spreadsheet.

Gap: discovery (as opposed to prioritization) is not covered by anything I could actually read; needs a better source.

Glossary: nothing checked against GLOSSARY.md for this run; RICE could be a candidate term.

## Practitioner notes (you)

