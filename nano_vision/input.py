import logging
import re
import subprocess
import time
from tqdm import tqdm
from pathlib import Path

import cv2

logger = logging.getLogger(__name__)


class Video:
    def __init__(self, src_path=None):
        """Initialize the video instance."""
        self._path = self._validated_path(src_path)
        self._play = True
        self._save_last_frame = False
        self._start_time = 0.0
        self._frames_to_encode = []
        self._ts_frames = []

    def current_timestamp(self):
        """
        Return the current timestamp.
        """
        return time.perf_counter() - self._start_time

    def add_frame(self, frame):
        """
        Add the given frame to the list of frames to encode.
        """
        self._frames_to_encode.append(frame)
        self._ts_frames.append(self.current_timestamp())

    def init_timer(self):
        """Initializer a timer to time stamp frames."""
        self._start_time = time.perf_counter()

    @property
    def start_time(self):
        """Retrieve the start time."""
        return self._start_time

    @property
    def ts_frames(self):
        """Retrieve the list of timestamps of each frame."""
        return self._ts_frames

    @property
    def frames_to_encode(self):
        """Retrieve the frames to encode."""
        return self._frames_to_encode

    @property
    def save_last_frame(self):
        """
        Return the flag that indicates if last frame is saved.
        """
        return self._save_last_frame

    @save_last_frame.setter
    def save_last_frame(self, new_state):
        """
        Set the flag that indicates if last frame is saved.
        """
        self._save_last_frame = new_state

    @property
    def play(self):
        """
        Return the flag that indicates that video is playing.
        """
        return self._play

    @play.setter
    def play(self, new_state):
        """
        Set the flag that indicates that video is playing.
        """
        self._play = new_state

    def is_playing(self):
        """
        Return playing status.
        """
        return self._play

    @property
    def path(self):
        """
        Return the path of the video.
        """
        return self._path

    @path.setter
    def path(self, new_path):
        """
        Set the path for the video.
        """
        self._path = self._validated_path(new_path)

    def _validated_path(self, input_path):
        """If path exists assign it to instance."""
        if input_path:
            path = Path(input_path)
            if path.is_file:
                return path
        return None

    def resolution_code(self):
        """
        Return the resolution of the current video source.
        """
        print(self)
        if not self._path:
            try:
                proc = subprocess.Popen(
                    ["v4l2-ctl", "--all"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            except FileNotFoundError as e:
                logger.error(str(e))
            try:
                outs, errs = proc.communicate()
            except Exception as e:
                logger.error(str(e))
                exit(1)
            logger.debug("Captured output: {}".format(outs))
            logger.debug("Captured errors: {}".format(errs))
            m = re.search("\d+/\d+", outs.decode("utf-8"))
            if not m:
                logger.error("Unable to find video resolution values")
                exit(1)
            values = m.group(0).split("/")
            width = values[0]
            height = values[1]
        else:
            cap = cv2.VideoCapture(str(self._path.absolute()))
            ret, frame = cap.read()
            if not ret:
                msg = "Unable to read file: {0}".format(self._path.absolute())
                logger.error(msg)
                raise ValueError(msg)
            width = frame.shape[1]
            height = frame.shape[0]
        logger.debug("width found: {0}, height found: {1}".format(width, height))
        if int(width) == 640 and int(height) == 480:
            return 1
        if int(width) == 960 and int(height) == 720:
            return 2
        if int(width) == 1224 and int(height) == 720:
            return 3
        if int(width) == 1280 and int(height) == 720:
            return 4
        if int(width) == 1280 and int(height) == 960:
            return 5
        if int(width) == 1920 and int(height) == 1080:
            return 6
        return 0

    def setup_encoding(self, filepath, width, height, fps):
        logger.debug(
            "Received time string: {0} Width: {1} Height: {2}".format(
                filepath, width, height
            )
        )
        fourcc = cv2.VideoWriter_fourcc(*"x264")
        out = cv2.VideoWriter(
            filepath,
            fourcc,
            fps,
            (width, height),
        )

        return fourcc, out

    def save(self, screen, filepath, fps=None):
        """
        screen has the dimensions of the frame to save.
        filename is the name of the saved video.
        """
        num_frames = len(self._frames_to_encode)
        logger.info("Frames to encode: {0}".format(num_frames))
        if fps:
            fourcc, out = self.setup_encoding(
                filepath, screen.width, screen.height, fps
            )
        else:
            try:
                fps = float(num_frames) / self._ts_frames[-1]
            except Exception as e:
                logger.error("Unable for compute fps for encoding due to: {0}".format(str(e)))
                exit(1)
            logger.debug("FPS: {0:.3f} [{1}/{2:0.3f}]".format(fps, num_frames, self._ts_frames[-1]))
            fourcc, out = self.setup_encoding(filepath, screen.width, screen.height, fps)
        logger.info("Saving video...")
        for i in tqdm(range(num_frames), desc="Writing frames"):
            out.write(self._frames_to_encode[i])
        logger.info("Done!")
        out.release()
