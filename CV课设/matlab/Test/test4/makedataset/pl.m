% 假设像素数据保存在变量 pixel_data 中，即一个长度为 400 的一维数组
load('ex3data1.mat')
data = X;


for i
    pixel_data = [你的数据]; % 请替换为你的实际数据
    
    % 将一维像素数据转为二维图像矩阵（假设是 20x20 的图像）
    image_matrix = reshape(pixel_data, 20, 20);
    
    % 显示图像
    imshow(image_matrix, []);
    
    % 如果需要保存图像为文件，可以使用 imwrite 函数
    imwrite(image_matrix, 'output_image.png');
