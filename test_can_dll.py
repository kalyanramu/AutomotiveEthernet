from ctypes import *
import struct
import sys

nxFrameCAN_t = struct.Struct('QIBBBB8s') 
print(nxFrameCAN_t.size)
#Verify:
# a) Static Implementation for Session Reference

#typedef i32 nxStatus_t
#typedef u32 nxSessionRef_t

NUM_FRAMES = 2
nxFrameCAN_t = 8

CAN_port        = 'CAN5'
CAN_database    = "NIXNET_example"
CAN_cluster     = "CAN_Cluster"
CAN_frames      = "CANEventFrame1,CANEventFrame2"
# Declare all variables for the function
i = c_uint(0)
l_NumBytes = c_uint(0)
l_pSelectedInterface = c_char_p(CAN_port.encode('utf-8'))
l_pSelectedDatabase = c_char_p(CAN_database.encode('utf-8'))
l_pSelectedCluster = c_char_p(CAN_cluster.encode('utf-8'))
l_pSelectedFrameList = c_char_p(CAN_frames.encode('utf-8'))
l_Buffer= create_string_buffer(NUM_FRAMES * nxFrameCAN_t)
l_Status = c_int(0)
nxMode_FrameInSinglePoint = c_uint(8)
#Session Reference Declaration
m_SessionRef = c_uint(0)
m_SessionRef_ptr = pointer(m_SessionRef)

#Frame Variables
#nxFrameVar_t *l_pFrame = NULL

try:
    mydll = cdll.LoadLibrary(r"C:\Windows\System32\nixnet.dll")
    print("Loaded the library")


    l_Status = mydll.nxCreateSession(
        l_pSelectedDatabase,            # Database Name
        l_pSelectedCluster,             # Cluster Name
        l_pSelectedFrameList,           # List
        l_pSelectedInterface,           # Interface
        nxMode_FrameInSinglePoint,      # Mode
        m_SessionRef_ptr)               # 

    print(l_Status)

except Exception as e:
    print("Error : ", e)
