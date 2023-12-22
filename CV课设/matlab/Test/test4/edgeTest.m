% 读取图片
img = imread('C:\code\pythonProject\pythonProject\CV课设\matlab\Test\test4\第三照片.png');
figure, imshow(img), title('Original Image');

% 转换为灰度图像
grayImg = rgb2gray(img);
figure, imshow(grayImg), title('Grayscale Image');

% 手动设置Sobel算法的阈值
sobelThreshold = 0.06; % 阈值，可以在0到1之间调整

% 使用Sobel算法进行边缘检测
bwEdges = edge(grayImg, 'Sobel', sobelThreshold);
figure, imshow(bwEdges), title(['Sobel Edges with threshold: ', num2str(sobelThreshold)]);

% % 填充边缘内部，使字符成为封闭区域
bwFilled = imfill(bwEdges, 'holes');
% figure, imshow(bwFilled), title('Filled Characters');

% 对边缘检测结果进行膨胀操作
se = strel('square', 3);
bwDilated = imdilate(bwEdges, se);
figure, imshow(bwDilated), title('Dilated Edges');

% 使用regionprops来找到连通区域，即字符
stats = regionprops(bwDilated, 'BoundingBox', 'Area');
area = [stats.Area];
avgArea = mean(area);

% 初始化目标文件夹路径
targetFolderPath = 'C:\code\pythonProject\pythonProject\CV课设\matlab\Test\test4\分割图片目标文件夹\';

% 显示带有边界框的图像
figure, imshow(img), title('Detected Characters');
hold on;

% 分割并保存每一个字符
for i = 1:length(stats)
    if stats(i).Area > avgArea / 2 % 处理面积大于平均值的一半的区域
        
        % 获取边界框
        bbox = stats(i).BoundingBox;

        % 绘制边界框
        rectangle('Position', bbox, 'EdgeColor', 'r', 'LineWidth', 2);

        % 裁剪图像
        characterImg = imcrop(img, bbox);

        % 保存字符图像
        filename = sprintf('%scharacter_%d.png', targetFolderPath, i);
        imwrite(characterImg, filename);
    end
end

hold off;
