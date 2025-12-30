import logging
import time

import cv2

from nano_vision import Screen
from nano_vision import Video
from nano_vision import Overlays

logger = logging.getLogger(__name__)

video = Video()
screen = Screen()
overlay = Overlays()

res_code = video.resolution_code()
screen.set_resolution(res_code)

cap = cv2.VideoCapture(0)
if not (cap.isOpened()):
    print("Could not open video device")


cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen.width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen.height)

start = time.perf_counter()
while(True):
    timer = cv2.getTickCount()
    ret, frame = cap.read()
    frame_ts = time.perf_counter()-start
    logger.debug("Frame timestamp: {0}".format(frame_ts))
    overlay.elapsed_time(frame, frame_ts)
    cv2.imshow("preview",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite("outputImage-{0}x{1}.jpg".format(screen.width, screen.height), frame)
        break
cap.release()
cv2.destroyAllWindows()
