#https://stackoverflow.com/questions/54951492/issue-using-struct-pack-and-struct-unpack

import struct
class EnetFrame():
    destination_addr   = ''
    has_VLAN_tag       = False
    priority           = 0
    VID                = 0
    EtherType          = 0
    payload            = ''


    def pack(self):
        out = struct.pack()

        return out



# typedef struct _nxFrameEnet_t {
#       u16 Length;
#       u16 Type;
#       nxTimestamp1ns_t DeviceTimestamp;
#       nxTimestamp1ns_t NetworkTimestamp;
#       u32 Flags;
#       u8 FrameData[1];
#    } nxFrameEnet_t;

#typedef char nxMACAddress_t[18];
