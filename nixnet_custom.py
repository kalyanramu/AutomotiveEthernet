from ctypes import *
import struct
import sys
#define nxPrptype_u64                     (u32)0x09000000
#define nxClass_Session                   (u32)0x00100000 

from Enet_params import nxEptRxFilter_Element_t

nxClass_Session         = 0x00100000
nxPrptype_u64           = 0x09000000
nxPrptype_struct        = 0x0C000000 
nxMode_FrameInStream    = 6
nxMode_FrameOutStream   = 9  
class nixnet:
    DLL_PATH = ''

    def __init__(self, intf_type = 'CAN'):
        self.XNET_dll = cdll.LoadLibrary(r"C:\Windows\System32\nixnet.dll")
        self.session_ptr = None
        self.nxFrameCAN_t = struct.Struct('QIBBBB8s')  # NOQA: N801
        self.nxFrameEnet_t = struct.Struct('QIBBBB8s')  # NOQA: N801
        self.IntfEnetEptReceiveFilter = 0x000000BC
        self.EnetNumFramesReceived = 0x000000EF
        self.int_type = intf_type
        self.EnetBufferSize = 20000

        self.number_of_frames_received = 0

        if intf_type == 'CAN':
            self.frame_t = self.nxFrameCAN_t
        elif intf_type == 'ENET':
            self.frame_t = self.nxFrameEnet_t
        else:
            raise Exception('Unknown Interface Type : Allowed Modes are CAN, ENET')


    def create_frame_input_session(self, intf_port, intf_database = ":memory:", intf_cluster = '', intf_frames = ''):
    
        try:

            l_pSelectedInterface    = c_char_p(intf_port.encode('utf-8'))
            l_pSelectedDatabase     = c_char_p(intf_database.encode('utf-8'))
            l_pSelectedCluster      = c_char_p(intf_cluster.encode('utf-8'))
            l_pSelectedFrameList    = c_char_p(intf_frames.encode('utf-8'))
            nxMode                  = c_uint(nxMode_FrameInStream)
            m_SessionRef            = c_uint(0)
            m_SessionRef_ptr        = pointer(m_SessionRef)
    
            
            l_Status = self.XNET_dll.nxCreateSession(
                l_pSelectedDatabase,            # Database Name
                l_pSelectedCluster,             # Cluster Name
                l_pSelectedFrameList,           # List
                l_pSelectedInterface,           # Interface
                nxMode,                         # Mode
                m_SessionRef_ptr)               # 

            self.session_ptr = m_SessionRef
            status = l_Status

            if status < 0:
                raise Exception('XNET Session Error :  {}'.format(status))

            #print('session :', self.session_ptr)
            return status

        except Exception as error:
            print(error)
            return None

    def create_frame_output_session(self, intf_port, intf_database = ":memory:", intf_cluster = '', intf_frames = '' ):
        
        try:
            l_pSelectedInterface    = c_char_p(intf_port.encode('utf-8'))
            l_pSelectedDatabase     = c_char_p(intf_database.encode('utf-8'))
            l_pSelectedCluster      = c_char_p(intf_cluster.encode('utf-8'))
            l_pSelectedFrameList    = c_char_p(intf_frames.encode('utf-8'))
            nxMode                  = c_uint(nxMode_FrameOutStream)
            m_SessionRef            = c_uint(0)
            m_SessionRef_ptr        = pointer(m_SessionRef)
    
            
            l_Status = self.XNET_dll.nxCreateSession(
                l_pSelectedDatabase,            # Database Name
                l_pSelectedCluster,             # Cluster Name
                l_pSelectedFrameList,           # List
                l_pSelectedInterface,           # Interface
                nxMode,                         # Mode
                m_SessionRef_ptr)               # 

            self.session_ptr = m_SessionRef
            status = l_Status

            if status < 0:
                raise Exception('XNET Session Error :  {}'.format(status))

            return status

        except Exception as error:
            print(error)
            return None        

    def read_bytes(self, number_of_bytes, timeout = 0):

        try:
            if self.int_type == 'CAN':
                bufferSize              = number_of_bytes
            else:
                bufferSize              = self.EnetBufferSize
            
            Buffer                      = create_string_buffer(bufferSize)
            SizeOfBuffer                = c_uint32(bufferSize)
            nxTimeout_None              = c_double(timeout)
            NumberOfBytesReturned       = c_uint32(0)
            NumberOfBytesReturned_ptr   = pointer(NumberOfBytesReturned)

            #print('session :', self.session_ptr)
            status = self.XNET_dll.nxReadFrame (self.session_ptr,Buffer,SizeOfBuffer, nxTimeout_None, NumberOfBytesReturned_ptr)
            #print("Detected number of bytes :", NumberOfBytesReturned.value)
            if status < 0:
                raise Exception('XNET Session Error :  {}'.format(status))

            if NumberOfBytesReturned.value == 0:
                return []
            else:
                #print(type(Buffer))
                out =[Buffer[i] for i in range(NumberOfBytesReturned.value)]   
            return out
        except Exception as error:
            print(error)
            return None
        
    def read_enet_frames(self, number_of_frames, timeout = 2):
        try:
            bytes_read = self.read_bytes(-1, timeout= timeout )
            frames = self.bytes_to_enet_frames(bytes_read)
            return frames

        except Exception as error:
            print('Error in get_enet_frames:', error)
            return None


    def write_bytes(self, buffer, timeout = 10):

        try:
            buffer_ptr                  = (c_byte * len(buffer))(*buffer)
            nxTimeout                   = c_double(timeout)
            NumberOfBytestoTx           = c_uint32(len(buffer))

            status = self.XNET_dll.nxWriteFrame (self.session_ptr,buffer_ptr,NumberOfBytestoTx, nxTimeout)
            #print("Detected number of bytes :", NumberOfBytesReturned.value)
            if status < 0:
                raise Exception('XNET Session Error :  {}'.format(status))
            return status

        except Exception as error:
            print(error)
            return None


    def write_enet_frames(self,enet_frames, timeout = 10):
        try:
            data_bytes = self.enet_frames_to_bytes(enet_frames)

            status = self.write_bytes(data_bytes)
        
            if status < 0:
                raise Exception('XNET Session Error :  {}'.format(status))
            return status

        except Exception as error:
            print(error)
            return None

    def enet_frames_to_bytes(self,enet_frames):
        try:
            if len(enet_frames) <=0:
                return None
            else:
                return None
        
        except Exception as error:
            return None


    def set_property_int64(self, propertyID, propertyValue):

        try:
            property_id     = c_uint32(propertyID | nxClass_Session | nxPrptype_u64)
            property_value  = c_uint64(propertyValue)
            status          = self.XNET_dll.nxSetProperty(self.session_ptr, property_id, c_uint32(8), pointer(property_value))
            if status < 0:
                raise Exception('XNET Session Error :  {}'.format(status))
                
        except Exception as error:
            print(error)
            return None


    def close_frame_session(self):
        self.XNET_dll.nxClear(self.session_ptr)

    def __del__(self):
        self.close_frame_session()




    def set_rx_filter(self, VID:int = None, priority:int = None):
    
        try:
            

            RxFilter_array = (nxEptRxFilter_Element_t *1) ()

            if VID is not None:
                RxFilter_array[0].VID = c_uint16(VID)

            if priority is not None:
                RxFilter_array[0].priority = c_uint8(priority)
            
            RxFilter_size = c_uint32(sizeof(nxEptRxFilter_Element_t)*1)
            RxFilter_array[0].UseFlags = c_uint32(3)
            STRUCT_ARRAY = pointer(RxFilter_array)
            
            IntfEnetEptReceiveFilter_id = c_uint32(self.IntfEnetEptReceiveFilter | nxClass_Session | nxPrptype_struct)
            self.XNET_dll.nxSetProperty(self.session_ptr, IntfEnetEptReceiveFilter_id, RxFilter_size ,STRUCT_ARRAY)

            print('Successfully Set Rx Filter...')
            return 'Success'
        except Exception as error:
            print(error)
            return None

    def get_rx_filter(self):
        try:
            RxFilter_array = (nxEptRxFilter_Element_t *2) ()
            RxFilter_size = c_uint32(sizeof(nxEptRxFilter_Element_t)*2)

            STRUCT_ARRAY = pointer(RxFilter_array)
            IntfEnetEptReceiveFilter_id = c_uint32(self.IntfEnetEptReceiveFilter | nxClass_Session | nxPrptype_struct)
            status = self.XNET_dll.nxGetProperty(self.session_ptr, IntfEnetEptReceiveFilter_id, RxFilter_size ,STRUCT_ARRAY)

            if status < 0:
                raise Exception('XNET Session Error :  {}'.format(status))

            VID         = RxFilter_array[0].VID
            priority    = RxFilter_array[0].priority
            return VID, priority

        except Exception as error:
            print (error)
            return None, None

        except Exception as error:
            print('Error in accessing the property get_rx_filter :', error)
            return None

    def get_num_enet_frames_received(self):
        try:

            EnetNumFramesReceived_id = c_uint32(self.EnetNumFramesReceived | nxClass_Session | nxPrptype_u64)
            num_frames_received = c_uint64(0)
            status = self.XNET_dll.nxGetProperty(self.session_ptr, EnetNumFramesReceived_id, c_uint32(8), pointer(num_frames_received))    
            if status < 0:
                raise Exception('XNET Session Error :  {}'.format(status))  
            return num_frames_received.value

        except Exception as error:
            print('Error in Num_Enet_Frames_Received :', error)
            return None

    def bytes_to_enet_frames(self,bytes_array):
        
        try:
            if len(bytes_array) == 0:
                return []
            
            current_start_ptr = 0
            frames = []
            while current_start_ptr != len(bytes_array):
                next_frame_size = int.from_bytes(bytes_array[current_start_ptr], byteorder = 'big')
                #print(next_frame_size)
                
                current_end_ptr = current_start_ptr + next_frame_size
                current_frame = bytes_array[current_start_ptr : current_end_ptr]
                frames.append(current_frame)

                current_start_ptr = current_end_ptr
                #print(current_frame)
            return frames

        except Exception as error:
            print('Error in bytes_to_enet_frames :', error)
            return None
