# Microcontrollers

Category: iot-electronics · Topic ID: microcontrollers

## Sources

- [fetched] https://docs.espressif.com/projects/esp-idf/en/latest/esp32/ — ESP-IDF Programming Guide landing page (index only; sub-pages not read)
- [fetched] https://docs.arduino.cc/ — Arduino docs landing page (index only; sub-pages not read)
- [fetched] https://randomnerdtutorials.com/projects-esp32/ — index of 250+ ESP32 tutorials (index only; individual tutorials not read)

All three fetched successfully, but all are hub/index pages, so findings are structural, not deep.

## Findings

- ESP-IDF (Espressif docs): official framework for the ESP32 family (ESP32, -S, -C, -H, -P series). Sections: Get Started, API Reference, Hardware Reference, API Guides, Security Guides, Migration Guides, Libraries and Frameworks, Versions. A chip/version selector switches the docs per target. The landing page itself has no setup steps; those live under Get Started (not read).
- Arduino docs: sections Hardware, Software (IDEs, Web Editor, CLI), Cloud (Arduino Cloud for IoT), Programming (language reference, libraries, built-in examples), Learn, Tutorials, plus a Legacy section for retired boards.
- Random Nerd Tutorials: practical ESP32 index grouped by Learn ESP32 (pinout, digital I/O, PWM, ADC, interrupts/timers, deep sleep), Protocols (Wi-Fi, BLE, MQTT, ESP-NOW, LoRa, HTTP), Web Servers, DIY Cloud, Firebase, Modules and Sensors (relay, motors, microSD, PIR, DHT, BME280, MPU-6050), Displays, ESP32 Features, Useful Guides (OTA, solar power, deep sleep, fixed IP), and newer posts (Matter, FreeRTOS, chip selection guide). The page lists peripherals (touch, ADC, DAC, I2C, SPI, UART, I2S, PWM) and describes the ESP32 as dual-core with Wi-Fi and Bluetooth.
- Takeaway: two programming routes for ESP32-class MCUs: Arduino-style (simple, library-rich) vs ESP-IDF (native, FreeRTOS-based, full control, security/OTA features). The tutorial site mostly uses the Arduino route.
- Electrical specs: none of the fetched pages gave voltages, currents, LiPo charging, or mains information. Any such claim (GPIO logic level, current limits, LiPo charging, relay/mains switching) is: unverified - needs user/datasheet check. Mains work in particular needs the relay/module datasheet and proper safety review.
- Glossary: no new term identified.

## Practitioner notes (you)

