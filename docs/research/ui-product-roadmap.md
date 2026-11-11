# UI & Product Development Roadmap (approved 2026-11-11)

- **Origin**: user-requested extension (Telegram, 2026-11-11), board-reviewed (ADR-0013). Order agreed: IoT & Electronics first, then UI/UX. Not part of the roadmap.sh FDE roadmap.
- **Status**: APPROVED by user (Telegram msg 220). Wired into `roadmap.py` as an extension doc.
- **Purpose**: UI/UX and product-development foundations for farmwatch-style projects (a field-monitoring dashboard on top of the IoT pipeline).
- **Success check**: a built artifact — a farmwatch dashboard prototype (live sensor readings, history chart, alert state) designed and implemented against mock data.
- **Constraints**: learning only, one research pass per topic, no loops. No hardware or paid-service spend (user decision 2026-11-11: no hardware purchases except for farmwatch itself). URLs below are UNVERIFIED seeds; unreachable ones mark the topic `fde:needs-better-sources` (ADR-0007).

---

## 1. UI & Product Development

### UX Fundamentals
User research basics, information hierarchy, usability heuristics.
- [@article@Nielsen Norman Group: 10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)
- [@article@Laws of UX](https://lawsofux.com/)

### Visual Design and Design Systems
Typography, color, spacing, components, tokens.
- [@article@Refactoring UI](https://www.refactoringui.com/)
- [@article@Material Design 3](https://m3.material.io/)

### Accessibility
WCAG basics, contrast, keyboard use, semantic markup.
- [@article@WCAG 2 Overview (W3C)](https://www.w3.org/WAI/standards-guidelines/wcag/)
- [@article@web.dev: Learn Accessibility](https://web.dev/learn/accessibility)

### Frontend Implementation
Component-based UI, responsive layout, state management.
- [@article@React Documentation](https://react.dev/learn)
- [@article@web.dev: Learn Responsive Design](https://web.dev/learn/design)

### Data Visualization and Dashboards
Charts for time series, status indicators, alert design.
- [@article@Storytelling with Data (blog)](https://www.storytellingwithdata.com/blog)
- [@article@Grafana: Dashboard Best Practices](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/)

### Prototyping and Usability Testing
Wireframes, clickable prototypes, testing with real users.
- [@article@Figma Learn](https://help.figma.com/hc/en-us/categories/360002051613-Get-started)
- [@article@Nielsen Norman Group: Usability Testing 101](https://www.nngroup.com/articles/usability-testing-101/)

### Product Discovery and Prioritization
Problem validation, MVP scoping, prioritization frameworks.
- [@article@Atlassian: Product Discovery](https://www.atlassian.com/agile/product-management)
- [@article@Intercom: RICE Prioritization](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/)

### Mobile and Offline-Friendly UI
Field use on phones, poor connectivity, glanceable status.
- [@article@web.dev: Progressive Web Apps](https://web.dev/learn/pwa)
- [@article@Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
