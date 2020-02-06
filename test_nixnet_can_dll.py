from nixnet_custom import nixnet
from importlib import reload
#reload(nixnet)
nxMode_FrameInStream = 6 
IntfBaudRate    = 0x00000016

CAN_port        = 'CAN5'
CAN_database    = ":memory:"
CAN_cluster     = ""
CAN_frames      = ""
CAN_mode        = nxMode_FrameInStream

baud_rate       = 125000
can_session = nixnet()

can_session.create_frame_session(CAN_port, CAN_database, CAN_cluster,CAN_frames, nxMode_FrameInStream)
can_session.set_property_int64(IntfBaudRate, baud_rate)
can_data = can_session.read_frame(2, timeout = 20)
print("Frame 0: ",can_data)
can_data = can_session.read_frame(2, timeout = 20)
print("Frame 1 :", can_data)

