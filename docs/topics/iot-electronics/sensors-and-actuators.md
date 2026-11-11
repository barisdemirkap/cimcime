# Sensors and Actuators

Category: iot-electronics · Topic ID: sensors-and-actuators

## Sources

- [fetched] https://learn.sparkfun.com/tutorials/analog-to-digital-conversion — ADC resolution, reference voltage, conversion math, Arduino analogRead example. (Read via WebFetch summarizer; formula equations are images on the page, so forms below are inferred from its worked examples.)
- [fetched] https://learn.adafruit.com/dht — DHT11 vs DHT22/AM2302 comparison table. Page has no wiring diagram, pull-up, or code; those are on a linked next page that was NOT read.
- [fetched] https://learn.adafruit.com/adafruit-stemma-soil-sensor-i2c-capacitive-moisture-sensor — overview of the capacitive I2C soil sensor. Page text gave no I2C address and no code.

Note: all three are vendor tutorials, not datasheets. No datasheet was consulted, so every electrical figure below is marked unverified.

## Findings

### Sensors vs actuators
Not defined by any of the three sources (they cover only sensors). Standard framing, not from sources: sensors turn physical quantities into electrical signals; actuators turn electrical signals into physical action. Actuators are not covered by these resources, a gap in this topic's source list.

### Analog-to-digital conversion (SparkFun)
- An ADC maps a pin voltage to an integer. Arduino's is 10-bit: 1024 levels, values 0-1023. 8-bit gives 256 levels, 16-bit gives 65,536.
- The reading is ratiometric against the reference voltage: ADC ≈ (V / Vref) × 1023, and V ≈ ADC × (Vref / 1023). Use 3.3 V as Vref on a 3.3 V system.
- Worked examples: 3.3 V system, reading 512 is about 1.65 V; 5 V system, 2.12 V is about 434; reading 334 is about 1.63 V.
- Common ADC method described: charge an internal capacitor, time its discharge through a resistor, count clock cycles.
- `analogRead()` does one conversion per call; use an `int`, not a `byte`.
- Pitfall: `analogRead` on a digital-only pin compiles but returns meaningless values. A digital sensor on an analog pin reads near 0 or near 1023.
- Sampling rate/theory is not covered by the page.
- Electrical claims (5 V / 3.3 V references, 10-bit Arduino ADC): unverified - needs user/datasheet check (board/MCU dependent).

### DHT11 vs DHT22 (Adafruit)
| Spec | DHT11 | DHT22/AM2302 |
|---|---|---|
| Supply/IO | 3-5 V | 3-5 V |
| Max current in conversion | 2.5 mA | 2.5 mA |
| Humidity | 20-80%, ~5% | 0-100%, 2-5% |
| Temp | 0-50 °C, ±2 °C | -40-80 °C, ±0.5 °C |
| Max sample rate | 1 Hz | 0.5 Hz |
- DHT22 is more accurate and wider range but slower; DHT11 is cheaper and faster. Both are "sluggish": do not poll faster than 1-2 s.
- Single digital data pin, 4 pins at 0.1" spacing. The wired AM2302 is noted as discontinued; the page recommends AM2301B (AHT20-based).
- Voltage and current figures: unverified - needs user/datasheet check (vendor page only; DHT datasheets not read).
- Pull-up resistor and library usage: not on this page; not researched.

### STEMMA soil sensor (Adafruit)
- Measures moisture using the capacitive touch feature of the on-board ATSAMD10 MCU; reports moisture and ambient temperature over I2C.
- Capacitive (single probe, no exposed metal) resists corrosion/drift; resistive two-prong probes oxidize, drift, need recalibration, and pass DC current into soil.
- Moisture output roughly 200 (very dry) to 2000 (very wet). Temperature from the MCU's internal sensor, about ±2 °C, not high precision.
- Powered at 3-5 V per the page (unverified - needs user/datasheet check). Connects by 4-pin JST-PH (power, GND, SDA, SCL); cable sold separately.
- I2C address: not stated on the page fetched. Not researched.

### Cross-cutting takeaways
- Sensor interface types seen: analog (needs ADC), proprietary single-wire digital (DHT), I2C digital (soil sensor).
- Accuracy and sample rate trade off (DHT11 vs DHT22).
- Mains and LiPo charging: not covered by any source; no claims made.

### Possible glossary terms
Check GLOSSARY.md; candidates it may lack: ADC, ratiometric reading, capacitive vs resistive sensing, I2C.

## Practitioner notes (you)

