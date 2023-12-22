% 读取图像
image = imread('C:\code\pythonProject\pythonProject\CV课设\matlab\Test\test4\test.png'); % 替换成你的图像路径

% 转为灰度图像
gray_image = rgb2gray(image);

% 二值化图像
binary_image = imbinarize(gray_image);

% 连通区域分析，获取数字的边界框
stats = regionprops(binary_image, 'BoundingBox');

% 初始化存储数字图像的单元数组
digit_images = cell(length(stats), 1);

% 循环处理每个数字的边界框
for i = 1:length(stats)
    % 获取当前数字的边界框
    bbox = stats(i).BoundingBox;

    % 裁剪数字图像
    digit = imcrop(gray_image, bbox);

    % 调整图像大小为 20x20 像素
    resized_digit = imresize(digit, [20, 20]);

    % 将图像转为列向量，并归一化到 [0, 1]
    flattened_digit = double(reshape(resized_digit, [], 1)) / 255.0;

    % 存储处理后的数字图像
    digit_images{i} = flattened_digit;
end

% 将数字图像存储为一个大矩阵（每一列是一个数字）
digits_matrix = cell2mat(digit_images);

% 显示结果
figure;
imshow(image); title('Original Image');

figure;
for i = 1:length(stats)
    subplot(1, length(stats), i);
    imshow(reshape(digits_matrix(:, i), 20, 20));
    title(['Digit ' num2str(i)]);
end
