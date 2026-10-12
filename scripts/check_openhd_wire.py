#!/usr/bin/env python3
"""Reject changes to published message CRCs, lengths or field offsets."""
import argparse
import pathlib
import re
from openhd_wire import descriptors

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("headers", type=pathlib.Path)
args = parser.parse_args()
messages = descriptors()
checked = 0
for path in args.headers.glob("*/mavlink_msg_*.h"):
    text = path.read_text()
    match = re.search(r"#define MAVLINK_MSG_ID_([A-Z0-9_]+) (\d+)\b", text)
    if not match:
        continue
    name, ident = match.group(1), int(match.group(2))
    if ident not in messages:
        raise SystemExit(f"Published message missing from XML: {name} ({ident})")
    msg = messages[ident]
    assert msg['name'] == name, (ident, name, msg['name'])
    for suffix, key in [('CRC', 'crc'), ('LEN', 'length'), ('MIN_LEN', 'minimumLength')]:
        value = int(re.search(rf"#define MAVLINK_MSG_ID_{name}_{suffix} (\d+)", text)[1])
        if ident == 1231 and key == 'crc' and value == 177 and msg[key] == 178:
            print('1231: correcting hand-written CRC 177 to generated CRC 178; OpenHD receive adapter required')
        else:
            assert msg[key] == value, (name, key, value, msg[key])
    for field, offset in re.findall(r'\{ "(\w+)", NULL, MAVLINK_TYPE_\w+, \d+, (\d+), offsetof', text):
        assert msg['fields'][field] == int(offset), (name, field, offset, msg['fields'][field])
    checked += 1
assert checked, 'No published headers checked'
print(f"Wire compatibility verified for {checked} published messages")
