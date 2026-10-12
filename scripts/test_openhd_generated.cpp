#include <cassert>
#include <cstddef>
#define MAVLINK_ASSERT assert
#include "openhd/mavlink.h"
#include "openhd/testsuite.h"
#include "mavlink_wire.hpp"

int main() {
    mavlink_message_t last{};
    mavlink_test_all(100, 191, &last);
    namespace wire = glide::openhd::generated;
    assert(wire::crc_extra(MAVLINK_MSG_ID_OPENHD_WIFBROADCAST_RADIO_SETTINGS) ==
           MAVLINK_MSG_ID_OPENHD_WIFBROADCAST_RADIO_SETTINGS_CRC);
    assert(!wire::crc_extra(0xffffff));
    assert(wire::openhd_core_status::fields::platform_type == 18);
}
