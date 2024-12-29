import cv2
# RTSP流的地址

rtsp_url = ''
# 创建VideoCapture对象

cap = cv2.VideoCapture(rtsp_url)
# 检查是否成功打开RTSP流

if not cap.isOpened():
    print('无法打开RTSP流')
    exit()
# 循环读取每一帧图像并进行处理

while True:
# 读取一帧图像

    ret, frame = cap.read()
    # 如果读取成功，ret为True，否则为False

    if not ret:
    print(‘无法读取帧’)
    break
    # 对帧进行处理（例如显示、分析等）

cv2.imshow(‘Video’, frame)
key = cv2.waitKey(1) & 0xFF
# 按’q’键退出循环

if key == ord(‘q’):
break
# 释放VideoCapture对象并关闭窗口

cap.release()
cv2.destroyAllWindows()