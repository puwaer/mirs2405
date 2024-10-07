import argparse
import time
import torch
import torch.backends.cudnn as cudnn
import cv2
from pathlib import Path
from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import check_img_size, non_max_suppression, scale_coords, set_logging, xyxy2xywh
from utils.plots import plot_one_box
from utils.torch_utils import select_device, time_synchronized
import numpy as np

def detect():
    source = 1  # USBカメラを使用するためのデフォルトデバイスID
    weights = 'yolov7.pt'  # ダウンロードした重みファイル
    imgsz = 640  # 画像サイズ
    conf_thres = 0.25  # 信頼度の閾値
    iou_thres = 0.45  # NMSのIOU閾値
    device = select_device('')
    half = device.type != 'cpu'  # FP16 half-precisionが可能な場合は使用

    # モデルのロード
    model = attempt_load(weights, map_location=device)
    stride = int(model.stride.max())
    imgsz = check_img_size(imgsz, s=stride)
    if half:
        model.half()

    cudnn.benchmark = True
    dataset = cv2.VideoCapture(source)
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[np.random.randint(0, 255) for _ in range(3)] for _ in names]

    while True:
        ret, img0 = dataset.read()
        if not ret:
            break

        img = letterbox(img0, imgsz, stride=stride)[0]
        img = img[:, :, ::-1].transpose(2, 0, 1)
        img = np.ascontiguousarray(img)

        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()
        img /= 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # 推論
        t1 = time_synchronized()
        pred = model(img, augment=False)[0]

        # NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes=None, agnostic=False)
        t2 = time_synchronized()

        for i, det in enumerate(pred):
            s = ''
            s += '%gx%g ' % img.shape[2:]

            gn = torch.tensor(img0.shape)[[1, 0, 1, 0]]
            if len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()

                for *xyxy, conf, cls in reversed(det):
                    label = f'{names[int(cls)]} {conf:.2f}'
                    plot_one_box(xyxy, img0, label=label, color=colors[int(cls)], line_thickness=3)

        cv2.imshow('YOLOv7', img0)
        if cv2.waitKey(1) == ord('q'):
            break

    dataset.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    detect()
