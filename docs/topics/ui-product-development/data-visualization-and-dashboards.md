# Data Visualization and Dashboards

Category: ui-product-development · Topic ID: data-visualization-and-dashboards

## Sources

- [fetched] https://www.storytellingwithdata.com/blog — blog index only; only post titles and teaser summaries were recoverable (newest posts dated Sep-Nov 2026), not the full articles.
- [fetched] https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/ — full Grafana dashboard best-practices doc.

## Findings

### Grafana best practices (Grafana docs)
- Purpose: a dashboard should answer a question or tell a story (e.g. "which servers are in trouble?"); with no goal it may not be needed. Move from general to specific. Reduce cognitive load: a new team member should be able to read each graph quickly.
- Pick and document an observability strategy first:
  - USE (Utilization, Saturation, Errors): for hardware resources (CPU, memory, network); reports on causes.
  - RED (Rate, Errors, Duration): for services/microservices; reflects user experience, suits alerting and SLAs.
  - Four Golden Signals (Latency, Traffic, Errors, Saturation): RED-like plus saturation.
  - Alert on symptoms rather than causes, so alerts typically build on RED dashboards.
- Maturity model:
  - Low: no strategy, anyone edits, copies and one-offs pile up, no version control.
  - Medium: template variables (instead of per-node dashboards, data source as a variable), hierarchical dashboards with drill-down, meaningful colors/thresholds, normalized axes, links, version-controlled JSON.
  - High: active sprawl reduction and regular review, approval before adding to a master list, usage tracking, generated dashboards (grafonnet, grafanalib), browser editing disallowed (viewers only change variables), testing in a separate instance before production.
- Building: meaningful names; `TEST`/`TMP` for temporary dashboards; owner in name or tag; delete temp ones. Split dashboards when magnitudes differ so aggregates don't hide detail; order rows by data flow; use left/right Y-axes for different units. Normalize metrics (CPU as % of cores); color meaningfully (blue good, red bad); be cautious with stacked graphs (misleading, hide data), usually disable. Match refresh rate to data change rate. Add a Text panel (purpose, links, usage) and panel descriptions. Document design guidelines.
- Managing: avoid copying dashboards (copies miss upstream fixes); link to the master with URL parameters/variables instead. If copying, rename and drop tags (copied tags cause false search matches). Cross-link related dashboards (dashboard/panel/data links, Dashboard list panels, "dashboard of dashboards"). Link dashboards from alerts for directed navigation.

### Storytelling with Data blog (index teasers only)
Per teaser summaries, not full articles:
- Layer visual cues (preattentive attributes: color, motion, enclosure) because audiences respond differently; combine cues so the message lands for everyone.
- Words matter: titles, labels, annotations should each do a specific job.
- "Give each point its own view": cramming detail into one chart doesn't build understanding; separate views can be clearer.
- Data storytelling means guiding the audience with perspective, not just "showing the data"; don't try to eliminate bias, bring perspective without harmful bias.
- Unwelcome stories are often just unexpected; framing and preparation turn resistance into discussion. Rehearse aloud and anticipate hard questions.
- AI can help choose chart types and prototype graphs/slides (SWD + AI series).

Caveat: the blog claims rest on teasers; the deeper reasoning of each post was not read.

### Glossary
No new terms obviously needed. Possible candidates: "USE/RED methods", "preattentive attributes".

## Practitioner notes (you)

