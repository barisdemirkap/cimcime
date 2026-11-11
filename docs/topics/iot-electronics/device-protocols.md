# Device Protocols

Category: iot-electronics · Topic ID: device-protocols

## Sources

- [fetched] https://mqtt.org/ — landing page: what MQTT is and its headline features
- [could not fetch] https://www.hivemq.com/mqtt/mqtt-essentials/ — HTTP 404 on two attempts (URL may have moved); nothing read. [unverified]

## Findings

All from https://mqtt.org/ only (thin: a landing page, not a deep tutorial):

- MQTT is an OASIS standard messaging protocol for IoT, using a publish/subscribe model aimed at remote devices with small code footprints and low bandwidth.
- Lightweight: clients small enough for tiny microcontrollers; compact message headers.
- Bidirectional: device-to-cloud and cloud-to-device, including broadcast to groups of devices.
- Scales to millions of devices.
- Three QoS levels: at most once, at least once, exactly once.
- Persistent sessions shorten reconnect time on unreliable networks.
- Security: TLS encryption; modern client authentication such as OAuth.
- The page gives no history or timeline, and no detail on topics, wildcards, retained messages, last will, keep-alive, broker design, or MQTT 5 vs 3.1.1. Those are NOT covered here; the HiveMQ resource that would have covered them was unreadable. [unverified]

No electrical claims (voltage, current, LiPo, mains) were made or sourced.

Glossary candidates: "broker", "QoS level", "persistent session" (not checked against GLOSSARY.md).

## Practitioner notes (you)

