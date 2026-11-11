# Edge-to-Cloud Pipeline

Category: iot-electronics · Topic ID: edge-to-cloud-pipeline

## Sources

- [fetched] https://docs.aws.amazon.com/iot/latest/developerguide/what-is-aws-iot.html — AWS IoT overview: protocols, interfaces (SDKs, CLI, API, console). Short page; no architecture detail on broker/rules/shadow beyond links.
- [fetched] https://docs.influxdata.com/influxdb/v2/get-started/ — InfluxDB v2 get-started landing page: tools, auth, core data-model concepts. Write/query details live on linked sub-pages that were not read.

## Findings

**AWS IoT (source 1)**
- AWS IoT provides cloud services connecting devices to each other and to other AWS services, plus device-side software (Device SDKs) to integrate devices.
- AWS IoT Core protocols: MQTT, MQTT over WSS (WebSockets Secure), HTTPS, and LoRaWAN.
- The message broker supports publish/subscribe over MQTT and MQTT over WSS; HTTPS is publish-only.
- AWS IoT Core for LoRaWAN replaces the need to run your own LoRaWAN Network Server (LNS).
- Platform features named: rules, jobs, thing objects, certificates, policies. The page only names these and links out; their semantics were not read here.
- Access paths: Device SDKs, AWS CLI, AWS IoT API (HTTP/HTTPS), AWS SDKs, console.
- The page advises that if you don't need device communications, rules or jobs, AWS Messaging services may fit better.

**InfluxDB v2 (source 2)**
- Interfaces: web UI (localhost:8086), `influx` CLI (separate install), HTTP API.
- Auth is via API tokens, each belonging to a user with specific permissions. In OSS 2.9.0 tokens are hashed by default; existing tokens are hashed on first startup and unrecoverable, so save plaintext tokens before upgrading.
- Data model: bucket (named storage location holding multiple measurements), measurement (logical grouping; points should share tags), tags (rarely-changing metadata, e.g. host/location), fields (values that change over time), timestamp, point, series (same measurement + tag set).
- Ingestion options listed in navigation (not described on the page): Telegraf, scrapers, client libraries, `influx` CLI, HTTP API. Flux is the query language per the navigation.
- Not covered on this page: orgs, line protocol, Flux syntax.

**Synthesis (my inference, not stated by either source):** a typical pipeline is device -> MQTT -> AWS IoT Core broker -> rules/another consumer -> time-series store such as InfluxDB. Neither source describes this wiring or an AWS-to-Influx connector; that integration is unverified from these sources.

**Electrical claims:** none made; neither source covers voltage, current, LiPo or mains.

**Glossary:** consider adding terms: MQTT, message broker, time series / measurement / tag / field, bucket. (Not checked against GLOSSARY.md contents in depth.)

## Practitioner notes (you)

