# Prototyping and Debugging

Category: iot-electronics · Topic ID: prototyping-and-debugging

## Sources

- [fetched] https://learn.sparkfun.com/tutorials/how-to-use-a-multimeter — DMM ports, voltage/resistance/current/continuity, fuse and safety, basic troubleshooting order.
- [unverified] https://learn.sparkfun.com/tutorials/using-the-saleae-logic-analyzer — could not fetch: HTTP 404 Not Found (one attempt, no retry per instructions). Nothing from this page is used below.
- [fetched] https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/ota.html — ESP-IDF OTA process, partitions, otadata, rollback, secure OTA, API list.

## Findings

Multimeter (SparkFun tutorial; a vendor tutorial, not a datasheet):
- Parts: display, selector knob, ports. COM is the common probe (usually black, to ground); mAVOhm port for V/ohm/current up to 200 mA; separate 10 A port for larger current.
- Voltage: measure in parallel, DC setting for most electronics. Meter is not autoranging: pick a range above expected value; "1" means overload. Reversed probes give a negative reading, harmless. Example given: a 5 V circuit should read 4.5-5.5 V; an LED dropped 2.66 V of 5 V. These are tutorial examples: unverified - needs user/datasheet check.
- Resistance: pick a range above expected value; "1"/"OL" means overload, "0.00" means go lower. Typical resistor tolerance ~5% (tutorial). In-circuit readings are unreliable because other components interfere.
- Current: measure in series, so the circuit must be broken and the meter placed inline. Use the 200 mA port for small currents, 10 A port if unsure. Readings fluctuate and are averaged. Example: ~7-8 mA for a small 5 V breadboard project (unverified - needs user/datasheet check).
- Key failure mode: leaving the meter in current mode and probing across VCC/GND shorts the supply through the meter and blows the internal 200 mA fuse (fuse value from tutorial; unverified - needs user/datasheet check). A blown fuse reads 0.00 and the circuit will not power. Always return to voltage mode when done; replace the fuse with the same type, never a 10 A fuse in the 200 mA slot.
- Continuity: circuit must be off. A beep means low resistance (a few ohms or less); capacitors can cause a brief beep while charging.
- Suggested troubleshooting order: (1) powered: check VCC and GND voltages (the tutorial notes a 5 V system reading 4.2 V hints at a regulator problem or excess current draw; unverified - needs user/datasheet check); (2) unpowered: continuity between VCC and GND, a beep suggests a short; (3) verify VCC/GND wiring at every part; (4) if the microcontroller runs, move to serial debugging or a logic analyzer.
- Mains: the tutorial warns AC mains can be lethal and recommends a non-contact AC tester for outlets. No mains voltage figures were given; any mains figure: unverified - needs user/datasheet check.

Logic analyzer (Saleae): NOT READ (404). Do not rely on this file for capture settings, sample rates, or protocol analyzers. The multimeter page only points to it as the step after serial debugging.

ESP-IDF OTA (Espressif docs):
- Safe mode (app images): new image goes to the non-running OTA slot; otadata is updated only after validation, so power loss mid-update still boots the old app. Unsafe mode (bootloader, partition table, NVS, other data partitions): written to a temporary partition then copied, so power loss during the copy can brick the device.
- Partition table needs at least two OTA app slots (ota_0, ota_1) plus an otadata partition (type data, subtype ota). Factory app optional; with no otadata the bootloader boots factory, else the first OTA slot.
- otadata uses two flash sectors (0x2000 bytes total) with a sequence counter (ota_seq) so a torn write cannot corrupt it; it stores OTA state and next boot slot.
- Rollback is on by default (CONFIG_BOOTLOADER_APP_ROLLBACK); disabling it is discouraged in production. Automatic confirmation marks the app valid just before app_main; app-controlled confirmation leaves it pending until self-tests pass. A new app gets one attempt: reset, crash, or power loss before confirmation makes the bootloader mark it ABORTED and boot the previous app. Only OTA partitions roll back, not factory.
- States: NEW, PENDING_VERIFY, VALID, INVALID, ABORTED, UNDEFINED. Bootloader skips INVALID and ABORTED.
- Validation: esp_ota_end() validates the image (incl. signature with secure boot); esp_ota_check_image_validity() checks chip ID/revision. esp_ota_get_state_partition() detects first boot (PENDING_VERIFY).
- Secure OTA: signed updates possible without hardware secure boot (CONFIG_SECURE_SIGNED_APPS_NO_SECURE_BOOT, CONFIG_SECURE_SIGNED_ON_UPDATE_NO_SECURE_BOOT). Anti-rollback (CONFIG_BOOTLOADER_APP_ANTI_ROLLBACK) compares against an eFuse security version; 32-bit field so usable only 32 times; needs app-controlled confirmation. Signed data partitions use Secure Boot v2 (idf.py secure-sign-data).
- Core API: esp_ota_begin / write / end / abort, esp_ota_set_boot_partition, esp_ota_mark_app_valid_cancel_rollback, esp_ota_mark_app_invalid_rollback_and_reboot. otatool.py manipulates OTA partitions from the CLI. bulk_flash_erase in esp_https_ota_config_t can speed up updates.
- Practical takeaway for field deployments: make confirmation app-controlled and tie it to a real health check (network up, sensor read), so a bad remote update self-reverts without a site visit.
- No electrical figures (voltage, current, charging) appear in this page. LiPo charging figures: not covered by any source; unverified - needs user/datasheet check.

Glossary: not checked against GLOSSARY.md; candidates: "OTA (over-the-air update)", "rollback / app-controlled confirmation", "otadata", "continuity test".

## Practitioner notes (you)

