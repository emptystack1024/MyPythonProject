% ld = load("labels.mat");
% gTruth = ld.gTruth;
% 
% DataSource = gTruth.DataSource;
% LabelDefinitions = gTruth.LabelDefinitions;
% LabelData = gTruth.LabelData;
% 
% Source = DataSource.Source;
% TimesStamps = DataSource.TimeStamps;
% 

% 指定文件夹路径
folderPath = './your_folder_path/';

% 获取文件夹中的图像文件列表
imageFiles = dir(fullfile(folderPath, '*.png'));  % 或者其他图像格式，如 '*.jpg'

% 初始化 cell 数组来存储图像
imageData = cell(1, numel(imageFiles));

% 循环读取每个图像并存储在 cell 数组中
for i = 1:numel(imageFiles)
    % 生成完整的文件路径
    imagePath = fullfile(folderPath, imageFiles(i).name);
    
    % 读取图像
    img = imread(imagePath);
    
    % 存储图像到 cell 数组中
    imageData{i} = img;
end

% 现在，imageData 中包含了整个文件夹中的图像
