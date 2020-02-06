from nixnet_custom import nixnet
from Enet_params import nxEptRxFilter_Element_t
from ctypes import *
import time


Eth_port        = 'ENET3'
VID             = 2
priority        = 3

enet_session = nixnet('ENET')
status = enet_session.create_frame_output_session(Eth_port)

buffer = [i for i in range(1000)]
status = enet_session.write_bytes(buffer)



