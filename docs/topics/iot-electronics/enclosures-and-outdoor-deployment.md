# Enclosures and Outdoor Deployment

Category: iot-electronics · Topic ID: enclosures-and-outdoor-deployment

## Sources

- [fetched] https://en.wikipedia.org/wiki/IP_Code — IP rating structure, digit meanings, testing, caveats (read via WebFetch summary).
- [fetched, thin] https://learn.adafruit.com/ — Adafruit Learning System homepage only. Lists titles/previews; no guide on waterproofing, outdoor deployment, solar or batteries was shown. Content is a hub, not study material; a site search / specific guide is needed (not done: one research pass).

## Findings

IP Code (Wikipedia):
- Format: "IP" + first digit (solids, 0-6 or X) + second digit (liquids, 0-9 or X) + optional letters. X means "not rated/no data". "IPX-8" style hyphenated codes are invalid.
- Solids: 5 = dust protected (some ingress allowed if not harmful); 6 = dust-tight.
- Liquids: 1-2 dripping; 3-4 spray/splash; 5-6 water jets (6 stronger); 7 = immersion up to 1 m for 30 min; 8 = deeper/continuous immersion, conditions set by the manufacturer (generally up to 3 m per the article); 9 = high-pressure, high-temperature spray.
- IP65 = dust-tight + jets; IP67 = dust-tight + temporary immersion to 1 m; IP68 = dust-tight + manufacturer-specified longer immersion (the article gives no explicit IP68 definition; the above is inferred from level 8).
- Water ratings are NOT cumulative beyond IPX6: IPX7 does not imply IPX5/IPX6. Dual ratings are written like IPX5/IPX7.
- IPx9K/IP69K: 80 C water, 8-10 MPa, 14-16 L/min, four angles x 30 s on a turntable (washdown use). The article is somewhat self-contradictory on whether ISO 20653 "superseded" IPx9K.
- Caveats: tests use fresh water only; salt water, oils, solvents need separate chemical-resistance testing (relevant to coastal/industrial sites). IP is not equivalent to NEMA types. "Waterproof" is a marketing term.
- Article-quality flags: supplementary letter table appears to list G and F both as "oil resistant"; the nozzle/impact-force figure is sourced only to a vendor news piece.

Adafruit: no usable content beyond homepage listing (e.g. an ESP32-P4 case guide, an unrelated sensor guide). Nothing about outdoor deployment can be claimed from it.

Practical implications (derived from the IP material, not from a source beyond it): an IP rating applies to the enclosure as tested, so cable glands, vents, connectors, and lid seals determine real-world rating; ask whether a vendor's "IP67" covers the whole assembled unit.

Electrical claims (LiPo charging, solar, voltage/current limits, mains): none made. Anything on these remains "unverified - needs user/datasheet check".

Glossary candidate: "IP rating" (and possibly "ingress protection") if the project does not define it. Not checked against GLOSSARY.md beyond the task prompt.

## Practitioner notes (you)

