#include <cassert>
#include <cstddef>
#define MAVLINK_ASSERT assert
#include "openhd/mavlink.h"
#include "mavlink_wire.hpp"

int main() {
    mavlink_message_t sent{}, received{};
    mavlink_status_t status{};
    mavlink_msg_openhd_wifbroadcast_radio_settings_pack(255, 190, &sent, 100, 191, 1, 5, 6, 7);
    uint8_t bytes[MAVLINK_MAX_PACKET_LEN];
    auto length = mavlink_msg_to_send_buffer(bytes, &sent);
    unsigned count = 0;
    for (unsigned i = 0; i < length; ++i)
        count += mavlink_parse_char(0, bytes[i], &received, &status);
    assert(count == 1);
    mavlink_openhd_wifbroadcast_radio_settings_t settings{};
    mavlink_msg_openhd_wifbroadcast_radio_settings_decode(&received, &settings);
    assert(settings.target_system == 100 && settings.mcs_via_rc_channel == 5);
    namespace wire = glide::openhd::generated;
    assert(wire::crc_extra(MAVLINK_MSG_ID_OPENHD_WIFBROADCAST_RADIO_SETTINGS) ==
           MAVLINK_MSG_ID_OPENHD_WIFBROADCAST_RADIO_SETTINGS_CRC);
    assert(!wire::crc_extra(0xffffff));
    assert(wire::openhd_core_status::fields::platform_type == 18);
}
