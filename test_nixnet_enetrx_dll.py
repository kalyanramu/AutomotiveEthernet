from nixnet_custom import nixnet
from Enet_params import nxEptRxFilter_Element_t
from ctypes import *
import time


Eth_port        = 'ENET3'
VID             = 2
priority        = 3

enet_session = nixnet('ENET')
enet_session.create_frame_input_session(Eth_port)
enet_session.set_rx_filter(VID, priority)


status = 0
while status == 0:
    try:
        enet_frames = enet_session.read_enet_frames(1, timeout = 0)
        print("New Enet Frames Detected :", len(enet_frames))
        if len(enet_frames) > 0:
            for index, frame in enumerate(enet_frames):
                print("Frame {} ".format(index))
                print(frame)
        time.sleep(2)

    except Exception as error:
        print(error)
        status = 1


