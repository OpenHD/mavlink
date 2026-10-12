# OpenHD dialect and upstream review

`message_definitions/v1.0/openhd.xml` owns message IDs, fields, CRCs and command
definitions. Never edit generated headers or client CRC/offset tables.
The redundant common.xml include was removed (ardupilotmega includes it).
Commands now extend MAV_CMD. C++ consumers use MAV_CMD_OPENHD_*; the duplicate
OPENHD_CMD enum and unused dummy commands were removed. Command numbers stay unchanged.
Settings use standard PARAM_EXT, FILE_TRANSFER_PROTOCOL and component metadata.

## Reproduce

```sh
git submodule update --init --recursive
python3 -m pip install future lxml
bash scripts/generate_openhd_headers.sh
python3 scripts/check_openhd_wire.py /path/to/published/mavlink/v2.0
python3 scripts/sync_openhd_wire.py --fleet /path/to/FleetControl \
  --webui /path/to/WebUI --glide /path/to/openhd-glide
python3 scripts/sync_openhd_wire.py --openhd /path/to/OpenHD
```

The pymavlink submodule pins the generator, including its XML include-parser
fix. Generated headers and descriptors are published together in
OpenHD/mavlink-headers with XML/generator commits in source.json. C++ consumers
pin that repository; other clients check in generated descriptors. Synchronize
all consumers before release; use sync_openhd_wire.py --check to detect drift.
OpenHD's internal statistics fields and telemetry conversions are generated as
plain data plus a separate encoding adapter. Application-only state stays in
OpenHD; the common/interface libraries have no MAVLink transport dependency.

## Compatibility and release order

The compatibility check verifies all published CRCs, lengths and field offsets.
Do not renumber messages, rename/reorder base fields or delete reserved fields.
New fields belong after extensions.

Historical message 1231's manually maintained header specified CRC 177, but the
MAVLink generator calculates 178. Its six fields and their offsets stay the
same. OpenHD's receiver verifies unsigned legacy CRC-177 packets for this
message only and normalizes their checksum before forwarding. New senders use
178. Deploy the new OpenHD receiver BEFORE upgrading QOpenHD: old receivers
cannot accept CRC 178. The adapter belongs in OpenHD, outside generated code.

## Upstream contribution

OpenHD is absent from current upstream MAVLink. Deployed message IDs 1211–1231
and commands 11200–11203 lie in upstream's common range. No current collision
does NOT establish an allocated vendor range. Obtain maintainer approval for
these deployed IDs before submitting; otherwise plan a versioned transition.

Submit only the dialect and an all.xml include, using canonical
MAV_CMD_OPENHD_* entries. The upstream patch omits OpenHD build tooling and runtime compatibility adapters. Retain reserved fields for wire compatibility;
review descriptions/units and work-in-progress tags with maintainers.
Prefer common messages for new functionality (storage, cameras and power).
Validate against current upstream all.xml, not just this fork.
Keep client scripts and OpenHD adapters outside the upstream patch. The string
component-metadata schema proposal is a separate contribution. Neither upstream
acceptance nor ID allocation is claimed by this cleanup.

References: https://mavlink.io/en/messages/all.html and
https://mavlink.io/en/guide/define_xml_element.html.
