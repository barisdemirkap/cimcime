# Power Design

Category: iot-electronics · Topic ID: power-design

## Sources

- [fetched] https://batteryuniversity.com/article/bu-808-how-to-prolong-lithium-based-batteries — Li-ion lifespan: charge voltage, depth of discharge, temperature, storage.
- [fetched, intro only] https://learn.adafruit.com/li-ion-and-lipoly-batteries — only the introductory page was read: compares alkaline, NiMH and Li-ion/LiPoly in qualitative terms. No voltage, charge-rate or safety figures were on it; the detailed sub-pages were not read.
- [fetched] https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/sleep_modes.html — ESP-IDF sleep modes, wakeup sources, RTC memory, power domains, API.

Note: BatteryUniversity is a vendor-education site, not a datasheet. All figures below are as stated by the page and are unverified - needs user/datasheet check against the actual cell's datasheet.

## Findings

Li-ion longevity (BatteryUniversity BU-808; unverified - needs user/datasheet check for all numbers):
- Most Li-ion cells charge to 4.20 V/cell; above 4.10 V/cell is treated as "high voltage".
- Each 0.10 V reduction in peak charge voltage roughly doubles cycle life but lowers stored capacity (about 10% per 70 mV). The page's table lists ~300-500 cycles at 4.20 V, up to 2,400-4,000 at 3.85 V, and names 3.92 V/cell as optimal for longevity. The page's text and table disagree in places, so treat as estimates.
- Charge at 1C or less; avoid chargers claiming a full charge in under an hour.
- Depth of discharge dominates cycle life (NMC, cycles to 70% capacity: ~300 at 100% DoD, ~2,000 at 20% DoD). No memory effect; partial discharge is fine.
- Heat is the main enemy: above 30 C is "elevated". One-year storage at 40% charge keeps ~96% at 25 C versus ~80% at 100% charge. A full cell kept hot is the worst case.
- Design implication: a device that sits on external power could cap charge near 4.05 V/cell (~80% SoC, page's "Long Life" suggestion, not a standard feature), trading runtime for lifetime.

Adafruit Li-ion/LiPoly guide (intro page only):
- Positions alkaline as the easy beginner choice, NiMH as a rechargeable drop-in, and Li-ion/LiPoly as the "shiniest" upgrade. Nominal/cutoff voltage, charge current and safety claims for LiPo: unverified - needs user/datasheet check (not on the page read).

ESP-IDF sleep modes (ESP32 doc page):
- Light-sleep: CPUs and digital peripherals are clock-gated with reduced supply voltage; internal state is preserved and execution resumes. Deep-sleep: CPUs, most RAM and APB-clocked peripherals are powered off; only the RTC controller, ULP coprocessor and RTC FAST/SLOW memory remain; the program restarts on wake (a wake stub runs first).
- Wi-Fi/Bluetooth are powered down in both; connections drop unless stopped cleanly. To keep a connection, use Modem-sleep with automatic Light-sleep instead.
- Wakeup sources: timer (both modes), touchpad, EXT0 (single RTC GPIO), EXT1 (multiple RTC GPIOs, any-high or all-low), ULP coprocessor, GPIO (any pin in light sleep; only VDD3P3_RTC-domain pads in deep sleep), UART (light sleep only).
- State across deep sleep: RTC SLOW memory variables (`RTC_DATA_ATTR`) persist by default; configurable via `esp_sleep_pd_config()`, which controls domains (RTC peripherals, RTC memories, XTAL, RC_FAST, VDDSDIO, MODEM) with ON/OFF/AUTO.
- Key APIs: `esp_deep_sleep_start()`, `esp_light_sleep_start()`, `esp_sleep_enable_timer_wakeup()`, `esp_sleep_enable_ext1_wakeup_io()`, `esp_sleep_get_wakeup_cause()`.
- Current figures on the page are limited to SPI flash: deep power-down "often below 1 uA", standby typically below 30 uA (also cited 10-30 uA), power-down time possibly over 300 ms. These are the ESP-IDF doc's statements, not a chip datasheet. The page gives NO chip active/sleep current: unverified - needs user/datasheet check (ESP32 datasheet).

Cross-cutting design takeaway: battery life is set by duty cycle (time in deep sleep vs awake plus radio), so combining a conservative Li-ion charge/temperature policy with deep-sleep wake-on-timer/GPIO is the lever; real numbers need the cell and SoC datasheets.

Glossary: not checked against GLOSSARY.md; candidates: "deep sleep / light sleep", "duty cycle (power)", "DoD (depth of discharge)", "RTC memory", "wake stub".

## Practitioner notes (you)

