# IoT & Electronics Roadmap — Extension Notes

- **Origin**: user-requested extension (Telegram, 2026-11-11), approved after a board review (ADR-0013). Not part of the roadmap.sh FDE roadmap; the original 97-topic Learning Phase is closed and unchanged.
- **Purpose**: foundations for farmwatch-style IoT projects. Success check = a built artifact: a bench sensor node that sends readings to the cloud.
- **Safety rule**: every electrical claim (voltage, current, charging, mains) must be verified against a datasheet or by the user before it informs a build. Hardware purchases need user approval (ADR-0001).
- **Resource status**: URLs below are UNVERIFIED seeds chosen from well-known sources; a topic-agent that cannot fetch one marks the topic `fde:needs-better-sources` (ADR-0007).
- **Cap**: one research pass per topic, no loops.

---

## 1. IoT & Electronics

### Electronics Fundamentals
Voltage, current, resistance, Ohm's law, reading schematics, and basic components.
- [@article@All About Circuits: Volume I - DC](https://www.allaboutcircuits.com/textbook/direct-current/)
- [@article@SparkFun: Voltage, Current, Resistance, and Ohm's Law](https://learn.sparkfun.com/tutorials/voltage-current-resistance-and-ohms-law)
- [@article@SparkFun: How to Read a Schematic](https://learn.sparkfun.com/tutorials/how-to-read-a-schematic)

### Microcontrollers
ESP32 and Arduino basics, GPIO, and the firmware workflow.
- [@article@ESP-IDF Programming Guide](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/)
- [@article@Arduino Documentation](https://docs.arduino.cc/)
- [@article@Random Nerd Tutorials: ESP32](https://randomnerdtutorials.com/projects-esp32/)

### Sensors and Actuators
Soil moisture, temperature/humidity, relays, and ADC readings.
- [@article@SparkFun: Analog to Digital Conversion](https://learn.sparkfun.com/tutorials/analog-to-digital-conversion)
- [@article@Adafruit: DHT Humidity and Temperature Sensors](https://learn.adafruit.com/dht)
- [@article@Adafruit: Capacitive Soil Moisture Sensor](https://learn.adafruit.com/adafruit-stemma-soil-sensor-i2c-capacitive-moisture-sensor)

### Power Design
Batteries, LiPo charging safety, solar, and low-power sleep modes.
- [@article@Battery University: Lithium-based Batteries](https://batteryuniversity.com/article/bu-808-how-to-prolong-lithium-based-batteries)
- [@article@Adafruit: Li-Ion and LiPoly Batteries](https://learn.adafruit.com/li-ion-and-lipoly-batteries)
- [@article@ESP-IDF: Sleep Modes](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/sleep_modes.html)

### Connectivity
WiFi, BLE, and LoRa/LoRaWAN for remote fields.
- [@article@The Things Network: LoRaWAN Introduction](https://www.thethingsnetwork.org/docs/lorawan/)
- [@article@Adafruit: LoRa and LoRaWAN Radio for Beginners](https://learn.adafruit.com/lora-and-lorawan-radio-for-raspberry-pi)
- [@article@ESP-IDF: Wi-Fi](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/wifi.html)

### Device Protocols
MQTT, HTTP, and device-to-cloud data flow.
- [@article@MQTT Essentials (HiveMQ)](https://www.hivemq.com/mqtt/mqtt-essentials/)
- [@article@MQTT.org](https://mqtt.org/)

### Edge-to-Cloud Pipeline
Ingestion, storage, and alerting for sensor data.
- [@article@AWS IoT Core Developer Guide](https://docs.aws.amazon.com/iot/latest/developerguide/what-is-aws-iot.html)
- [@article@InfluxDB: Time Series Data](https://docs.influxdata.com/influxdb/v2/get-started/)

### Enclosures and Outdoor Deployment
Waterproofing, ingress-protection ratings, and field reliability.
- [@article@IP Code (Ingress Protection) - Wikipedia](https://en.wikipedia.org/wiki/IP_Code)
- [@article@Adafruit: Waterproof Enclosures and Cable Glands](https://learn.adafruit.com/)

### Prototyping and Debugging
Breadboard to PCB, multimeter and logic analyzer use, and OTA updates.
- [@article@SparkFun: How to Use a Multimeter](https://learn.sparkfun.com/tutorials/how-to-use-a-multimeter)
- [@article@SparkFun: Logic Analyzers](https://learn.sparkfun.com/tutorials/using-the-saleae-logic-analyzer)
- [@article@ESP-IDF: OTA Updates](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/ota.html)
