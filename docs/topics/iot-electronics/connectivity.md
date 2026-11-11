# Connectivity

Category: iot-electronics · Topic ID: connectivity

## Sources

- [fetched] https://www.thethingsnetwork.org/docs/lorawan/ — course index only (chapter titles, no body). Supplemented with one sub-page: https://www.thethingsnetwork.org/docs/lorawan/architecture/ [fetched].
- [fetched] https://learn.adafruit.com/lora-and-lorawan-radio-for-raspberry-pi — overview page only (hardware list, bands, ranges); wiring/software pages are separate and were not read.
- [fetched, redirect/index only] https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/wifi.html — returned a "moved to wifi-driver/index.html" notice; the new URL returned only a table of contents. No technical body text was read.

## Findings

LoRaWAN architecture (TTN architecture page):
- Star-of-stars topology with five components: end devices (battery-powered sensors/actuators), gateways, Network Server, Application Server, Join Server.
- Gateways forward uplinks to the Network Server over a backhaul (cellular, Wi-Fi, Ethernet, fiber, 2.4 GHz radio).
- Devices are not bound to a gateway; every gateway in range may hear a message, and the Network Server deduplicates, keeping one copy.
- Network Server: authenticity/security checks, deduplication, gateway selection for downlinks, ADR commands, routing of join messages and payloads.
- Join Server: secure activation, stores root keys, derives session keys; NwkSKey goes to the Network Server, AppSKey to the Application Server.
- TTN index lists further chapters (device classes, regional parameters, security, limitations, spreading factors, ADR, duty cycle, antennas) whose content was NOT read.

Adafruit LoRa on Raspberry Pi (overview page):
- Hardware: LoRa Radio Bonnet (RFM95W, 915 MHz, OLED + 3 buttons) or bare RFM95W (868/915 MHz) / RFM96W (433 MHz) breakouts, used with a Pi 3B+ or Pi Zero, headless over SSH.
- Range claims on the page: RFM69 up to ~50 m, RFM9x LoRa up to ~2 km, LoRaWAN further via gateways; Wi-Fi/BLE shorter range but faster data rates (a useful trade-off framing: range vs data rate vs power).
- Band rules differ by region (433 MHz ISM vs amateur limits in the Americas).
- Electrical: the page only says the bundled supply is 5 V 2.5 A, "designed to provide 5.25V, not 5V" (as stated by the page; vendor page, not a datasheet). No radio module voltage/current figures given. Any radio TX current, 3.3 V logic levels, or LiPo claims: unverified - needs user/datasheet check.

ESP-IDF Wi-Fi driver (table of contents only): the guide covers station scenarios (scan, connect, auto-reconnect, beacon timeout), AP/sniffer/NAN modes, MAC protocol features, security modes (incl. DPP, WPS), performance/throughput and power-save modes, and ESP-WIFI-MESH. Substantive details were not retrievable; do not rely on this for specifics. Power-save current figures: unverified - needs user/datasheet check.

Glossary: no new terms checked against GLOSSARY.md; candidates: "star-of-stars", "backhaul", "ADR (adaptive data rate)".

## Practitioner notes (you)

