% 读取图像文件
img = imread('your_image.png');  % 替换为你的图像文件名

% 将图像大小调整为 20x20
resizedImg = imresize(img, [20, 20]);

% 将图像数据保存到 mat 文件
save('imageData.mat', 'resizedImg');
