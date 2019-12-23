#!/bin/bash

export PYTHONPATH=$PWD:$PYTHONPATH

python -m pymavlink.tools.mavgen --lang=C --wire-protocol=2.0 --output=../mavlink_generated/include/mavlink/v2.0 ./message_definitions/v1.0/openhd.xml

