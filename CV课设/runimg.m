% 读取图像
% RGB = imread('C:\code\pythonProject\pythonProject\大创\result.png');

% 调用 createMask 函数获取二值掩码 BW 和涂为红色的图像 maskedRGBImage
[BW, maskedRGBImage] = createMask(RGB);

% 腐蚀和膨胀操作
se1 = strel('disk', 10);  % 创建半径为 5 的圆形结构元素
erodedBW = imerode(BW, se1);  % 腐蚀操作
se2 = strel('disk', 25);  % 创建半径为 5 的圆形结构元素
dilatedBW = imdilate(erodedBW, se2);  % 膨胀操作
dilatedBW = imdilate(dilatedBW, se2);  % 膨胀操作
dilatedBW = imdilate(dilatedBW, se2);  % 膨胀操作
dilatedBW = imdilate(dilatedBW, se2);  % 膨胀操作
dilatedBW = imdilate(dilatedBW, se2);  % 膨胀操作


% 将 BW 中为 true（好的部分）的区域设为红色 [255, 0, 0]
maskedRGBImage(repmat(BW, [1, 1, 3])) = repmat([255, 0, 0], [sum(BW(:)), 1]);

% 将 BW 中为 false（其余部分）的区域设为白色 [255, 255, 255]
maskedRGBImage(repmat(~BW, [1, 1, 3])) = repmat([255, 255, 255], [sum(~BW(:)), 1]);

% 显示结果图像
imshow(maskedRGBImage);
