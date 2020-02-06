import nixnet
from nixnet import constants

CAN_port= 'CAN5'

count = 5
print('Starting the Program')

try:

    with nixnet.FrameInStreamSession(CAN_port) as input_session:
        input_session.intf.can_term = constants.CanTerm.ON
        input_session.intf.baud_rate = 125000
        
        frames = input_session.frames.read(count)

        try:
            next_item = next(frames)
        except StopIteration:
            # exhausted, handle this case
            print('Emprty....')

        for frame in frames:
            print('Received frame:')
            if frame is not None:
                print(frame)
            else:
                print('Empty Frame detected')

except Exception as error:
    print('Error :', error)
