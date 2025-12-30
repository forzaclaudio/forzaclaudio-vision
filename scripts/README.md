# Helper scripts

## How to setup resolution of the v2lsrc module

The resolution of the video from the droidcam app can be modified to the desired resolution as follows:

```bash
$ ./set_resolution <desired-resolution>
```
where `<desired-resolution>` can be any of the following:

1. 640 x 480 pixels
2. 960 x 720 pixels
3. 1280 x 720 pixels
4. 1920 x 1080 pixels

It is important to perform this step before launching the cam in order to the changes in resolution to be applied.

## How to launch the droidcam

Set the IP and Port variables in the `lauch_cam.sh` script to the desired values and run as follows:
```bash
$ ./launch_cam.sh
```


## Troubleshooting
```bash
ffplay -f video4linux2 /dev/video0
```
to test is video can be read
