# Electronics Fundamentals

Category: iot-electronics · Topic ID: electronics-fundamentals

## Sources

- [unverified] https://www.allaboutcircuits.com/textbook/direct-current/ — could not fetch: HTTP 403 Forbidden. Nothing from it is used below.
- [fetched] https://learn.sparkfun.com/tutorials/voltage-current-resistance-and-ohms-law — voltage/current/resistance, Ohm's law, LED resistor example.
- [fetched] https://learn.sparkfun.com/tutorials/how-to-read-a-schematic — symbols, naming, nets, reading strategy.

Note: the page content came back via WebFetch's summarizing model, so it is a summary of the page, not verbatim text.

## Findings

Electrical figures below come from SparkFun tutorials, not datasheets. Every numeric claim is marked "unverified - needs user/datasheet check" until checked against the actual part datasheet.

### Voltage, current, resistance (SparkFun V/I/R)
- Voltage (V, volts) is the charge difference between two points (water analogy: pressure). Current (I, amps) is the rate of charge flow, 1 A = 1 coulomb/second (flow). Resistance (R, ohms) is opposition to current (hose width).
- Ohm's law: V = I x R, so I = V/R and R = V/I. Know two, solve the third.
- Examples: 1 V across 1 ohm gives 1 A; across 2 ohm gives 0.5 A.
- LED example: 9 V battery, LED suggested 18 mA, so R = 9/0.018 = 500 ohm; nearest common value 560 ohm gives about 16 mA, under a stated 20 mA maximum. Unverified - needs user/datasheet check (the LED's real ratings are in its datasheet).
- Caveat from the tutorial: LEDs are non-ohmic and have a forward voltage drop, so the simple calculation ignores the drop. The resistor works the same before or after the LED in series (tied to Kirchhoff's Voltage Law). Practical consequence: real resistor sizing should subtract the LED forward voltage, taken from its datasheet. Unverified - needs datasheet check.

### Reading schematics (SparkFun)
- Symbols: resistor (zig-zag or rectangle), capacitor (two plates, curved plate marks polarized), inductor (coil), diode (triangle against bar; bar = cathode), LED (diode plus outward arrows), BJT (collector/emitter/base; emitter arrow gives NPN/PNP), MOSFET (source/drain/gate), logic gates (bubble = negation), ICs as labeled rectangles with numbered pins.
- Battery symbol: longer line is positive.
- Reference designators: letter prefix plus unique number (R1, C2, D1, Q1, U1, Y1); prefixes are not universal.
- Nets: a dot marks a real junction; crossing wires without a dot are not connected; same-named nets are connected even with no drawn wire (VCC, GND, RX, TX).
- Strategy: split into functional blocks, trace input to output, use voltage/ground nodes to see shared potentials, start from the central IC and consult its datasheet.

### Not covered by readable sources
- LiPo charging and mains electricity: not covered by any fetched source. No claims made. Any such claim needs a datasheet or is "unverified - needs user/datasheet check". Mains work should not be inferred from this topic.
- The All About Circuits DC textbook (series/parallel, Kirchhoff, power, etc.) was not read.

### Glossary
No new terms proposed beyond general electronics vocabulary; "net" and "reference designator" could be added if the project's GLOSSARY.md ever covers hardware.

## Practitioner notes (you)

