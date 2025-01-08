 /bin/python3 /home/mirs/Documents/zed_i2/zed_hight_image.py
[2025-01-08 08:12:24 UTC][ZED][INFO] Logging level INFO
[2025-01-08 08:12:24 UTC][ZED][INFO] Logging level INFO
[2025-01-08 08:12:24 UTC][ZED][INFO] Logging level INFO
[2025-01-08 08:12:26 UTC][ZED][INFO] [Init]  Depth mode: ULTRA
[2025-01-08 08:12:26 UTC][ZED][INFO] [Init]  Camera successfully opened.
[2025-01-08 08:12:26 UTC][ZED][INFO] [Init]  Camera FW version: 1523
[2025-01-08 08:12:26 UTC][ZED][INFO] [Init]  Video mode: HD720@60
[2025-01-08 08:12:26 UTC][ZED][INFO] [Init]  Serial Number: S/N 39772731
Traceback (most recent call last):
  File "/home/mirs/Documents/zed_i2/zed_hight_image.py", line 88, in <module>
    main()
  File "/home/mirs/Documents/zed_i2/zed_hight_image.py", line 19, in main
    width = camera_info.camera_resolution.width
AttributeError: 'pyzed.sl.CameraInformation' object has no attribute 'camera_resolution'