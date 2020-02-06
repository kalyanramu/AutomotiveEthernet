import ctypes
class nxEptRxFilter_Element_t(ctypes.Structure):
      _fields_ = [('UseFlags', ctypes.c_uint32),
                  ('VID', ctypes.c_uint16),
                  ('priority', ctypes.c_uint8),
                  ('nxMACAddress_t', ctypes.c_char * 18)
      ]
