# FarmWatch electronics cart - DRAFT (not approved, nothing bought)

Status: draft for user review. Every electrical value below marked (V) is UNVERIFIED and must be checked against the datasheet before purchase (iot-electronics safety rule). Vendors: Robotistan, Direnc.net first. No prices are listed because none were verified.

## Confirmed requirements (user, 2026-11-11)
- 3 independent nodes, hot standby: 2 ESP32 with Ethernet per node = 6 boards, all nodes installed.
- Per node: 1 water temperature probe (standard waterproof DS18B20 type) + 1 pump-drive fault signal (fault yes/no only, no current measurement).
- Pumps are 380 V (Delta VFD-EL-W drive); nodes have 220 V mains available. ESP32s are powered from 220 V via a 5 V DC supply and never touch the pumps.
- Ethernet only (WiFi possible later). Very humid, enclosed fish-farm room, ambient about 5-40 C, splash/liquid-protected enclosures.
- No UPS/battery (user decision); power loss is detected server-side by missing heartbeat.
- Heat pump / chiller monitoring is a later stage: leave spare I/O, buy nothing for it now.

## Open blockers
1. VFD side label photo (exact model, rated current).
2. Multimeter check of RA-RC (dry contact or voltage? AC/DC?) by a qualified person. The input-interface parts below stay provisional until then.
3. Distance from each panel to the Ethernet switch (decides cable and whether a switch is needed).
4. Are the 3 panels identical?

## Per node (quantity x3 nodes)
| # | Part | Qty/node | Total | Notes |
|---|------|----------|-------|-------|
| 1 | ESP32 board with Ethernet (candidates: Olimex ESP32-POE-ISO, WT32-ETH01, Waveshare ESP32-S3-ETH) | 2 | 6 | Check stock at Robotistan/Direnc.net (V). Prefer a board with isolated or well-documented Ethernet PHY; WT32-ETH01 is cheapest but has few GPIOs and no USB programming |
| 2 | DS18B20 waterproof stainless probe, cable length TBD | 2 | 6 | One probe per ESP32 (two masters must not share one 1-Wire bus); rated -55..125 C, +-0.5 C (V) |
| 3 | 4.7 kOhm resistor, 1/4 W (1-Wire pull-up) | 2 | 6 (+spares) | Between data and 3.3 V, one per probe bus (V) |
| 4 | 5 V DIN-rail or enclosed supply, 220 V in (e.g. Mean Well HDR-15-5 class) | 2 | 6 | Separate supply per ESP32 so one failure does not take both down; check current vs board consumption (V) |
| 5 | Fault-input interface (optocoupler module or relay) | 2 | 6 | PROVISIONAL. Dry contact: optocoupler driven from a safe low-voltage source. If RA-RC carries a voltage, design changes |
| 6 | Series resistor for optocoupler LED and 10 kOhm pull-up/pull-down | per interface | - | Values computed after step 2 of blockers |
| 7 | Fuse + DIN fuse holder on 220 V input (e.g. 1-2 A slow-blow) | 1 | 3 | (V) |
| 8 | Surge protection: MOV or surge protection device on 220 V, TVS diode on 5 V rail | 1 | 3 | Fish-farm mains are noisy (V) |
| 9 | IP65/IP66 enclosure, DIN rail, with cable glands | 1 | 3 | Size to fit 2 boards + 2 supplies + terminals; add breathable vent or silica for condensation |
| 10 | Cable glands (M16/M20), waterproof | 4-6 | 12-18 | Mains in, Ethernet, probe(s), signal |
| 11 | DIN terminal blocks + end caps | 12-16 | 36-48 | Mains (L, N, PE) and signal separated |
| 12 | Ferrules (assorted), wire 0.75 mm2 and 1.5 mm2 | - | 1 set | Colour-code mains vs low voltage |
| 13 | Ethernet patch cable Cat5e/Cat6, shielded | 2 | 6 | Length TBD |
| 14 | RJ45 Ethernet surge protector (inline) | 1 | 3 | Optional, recommended for long runs |
| 15 | Unmanaged Ethernet switch (5-8 port), DIN or small | 0-1 | 1-3 | Only if not already present |
| 16 | Heat-shrink, cable ties, labels | - | 1 set | |

## Hot standby note
Two ESP32 per node need a takeover rule (for example a second board watches the first via the network/heartbeat and takes over reporting). This is firmware/design work, not parts; both boards read the same drive fault contact through separate isolated inputs.

## Tools (if you don't have them)
Multimeter (also needed for blocker 2), wire stripper/crimper for ferrules, small screwdrivers, soldering iron, heat gun/lighter for heat-shrink.

## Not in the cart
Pump/VFD wiring, 380 V work, and any change to the existing panel: licensed electrician only. Heat-pump monitoring parts: next stage.
