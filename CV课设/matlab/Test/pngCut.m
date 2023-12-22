clear; close all;

% 读取图片
img = imread("C:\code\pythonProject\pythonProject\CV课设\matlab\Test\test4\test.png");
figure, imshow(img), title('Original Image');

% 转换为灰度图像
grayImg = rgb2gray(img);
% figure, imshow(grayImg), title('Grayscale Image');

% 手动设置阈值
thresholdValue = 0.4; % 示例阈值，您需要根据图像调整这个值
bwImg = imbinarize(grayImg, thresholdValue);
figure, imshow(bwImg), title(['Binary Image with threshold: ', num2str(thresholdValue)]);

% 反转图像，使得数字是白色，背景是黑色
bwImg = ~bwImg;
% figure, imshow(bwImg), title('Inverted Binary Image');

% 使用regionprops来找到连通区域，即手写数字
stats = regionprops(bwImg, 'BoundingBox', 'Area');
area = [stats.Area];
avgArea = mean(area);

% 初始化目标文件夹路径
targetFolderPath = 'C:\code\pythonProject\pythonProject\CV课设\matlab\Test\test4\分割图片目标文件夹\';
yasuoFolderPath = 'C:\code\pythonProject\pythonProject\CV课设\matlab\Test\test4\分割图片压缩后\';

% 显示带有边界框的图像
figure, imshow(bwImg), title('Labeled Image');
hold on;

% 初始化一个空矩阵用于存储提取的数据
myX = [];
myY = [];  % 初始化用于存储标签的向量

for i = 1:length(stats)
    % 获取边界框
    bbox = stats(i).BoundingBox;

    % 在原图上绘制边界框
    rectangle('Position', bbox, 'EdgeColor', 'r', 'LineWidth', 2);

    % 添加标记
    text(bbox(1),bbox(2), sprintf('%d', i), 'VerticalAlignment', 'top', 'Color', 'red');

    % 裁剪图像
    digitImg = imcrop(bwImg, bbox);
end

pause;

% 分割并保存每一个数字
for i = 1:length(stats)
    if stats(i).Area > avgArea / 2 % 处理面积大于平均值的一半的区域
        
        % 获取边界框
        bbox = stats(i).BoundingBox;

        % 在原图上绘制边界框
        rectangle('Position', bbox, 'EdgeColor', 'r', 'LineWidth', 2);

        % 添加标记
        text(bbox(1),bbox(2), sprintf('%d', i), 'VerticalAlignment', 'top', 'Color', 'red');

        % 裁剪图像
        digitImg = imcrop(bwImg, bbox);

        % 保存原始裁剪图像
        filename = sprintf('%sdigit_%d.png', targetFolderPath, i);
        imwrite(digitImg, filename);

        % 计算填充尺寸，使图像成为正方形
        [rows, cols] = size(digitImg);
        if cols > rows
            % 宽大于长，填充上下
            padSize = (cols - rows) / 2;
            verticalPadding = [floor(padSize), ceil(padSize)]; % 分别是上下填充
            paddedImg = padarray(digitImg, verticalPadding, 0, 'both');
        else
            % 长大于宽，填充左右
            padSize = (rows - cols) / 2;
            horizontalPadding = [floor(padSize), ceil(padSize)]; % 分别是左右填充
            paddedImg = padarray(digitImg, horizontalPadding, 0, 'both');
        end

        % 压缩图像为20x20
        resizedImg = imresize(paddedImg, [20 20]);

        x = resizedImg(:)';

        myX = [myX; x];

        % 显示填充后的图像
        figure; imshow(paddedImg), title(sprintf('Padded Image %d', i));
        
        y = input("正确值：")
        myY = [myY; y];

        % 保存压缩后的正方形图像
        squareFilename = sprintf('%sdigit_%d_square.png', yasuoFolderPath, i);
        imwrite(resizedImg, squareFilename);
    end
end

fprintf('完成，共有%d个数字。\n',length(stats));

% 指定保存路径
outputFilePath = 'C:\code\pythonProject\pythonProject\CV课设\matlab\Test\test4\result.mat';

% 保存数据到指定文件
save(outputFilePath, 'myX', 'myY');

hold off;
