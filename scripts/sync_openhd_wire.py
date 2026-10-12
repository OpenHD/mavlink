#!/usr/bin/env python3
"""Copy reproducible XML-derived wire descriptors into explicitly named clients."""
import argparse
import pathlib
from openhd_wire import products

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--fleet', type=pathlib.Path)
p.add_argument('--webui', type=pathlib.Path)
p.add_argument('--glide', type=pathlib.Path)
p.add_argument('--check', action='store_true')
a = p.parse_args()
files = products()
targets = []
if a.fleet:
    targets.append((a.fleet / 'server/mavlink-wire.ts', 'mavlink-wire.ts'))
if a.webui:
    targets.append((a.webui / 'src/OpenHdWebUi.Server/Services/Settings/MavlinkWire.g.cs', 'MavlinkWire.g.cs'))
if a.glide:
    targets.append((a.glide / 'src/common/mavlink_wire.hpp', 'mavlink_wire.hpp'))
if not targets:
    p.error('Specify at least one client checkout')
for path, name in targets:
    if a.check:
        if not path.exists() or path.read_text() != files[name]:
            raise SystemExit(f'Stale generated binding: {path}')
    else:
        path.write_text(files[name], encoding='utf-8', newline='\n')
