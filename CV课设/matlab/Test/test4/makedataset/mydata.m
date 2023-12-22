% 加载数据
load('ex3data1.mat');

% 初始化一个空矩阵用于存储提取的数据
myX = [];
myY = [];  % 初始化用于存储标签的向量

% 对每个500行的块进行操作
for i = 0:9
    % 计算当前块的起始行索引
    startIdx = i * 500 + 1;

    % 从当前块中随机选择20行
    indices = randperm(500, 20) + startIdx - 1;

    % 将选择的行添加到myX
    myX = [myX; X(indices, :)];

    % 为当前块创建相应的标签并添加到myY
    myY = [myY; repmat(i, 20, 1)];  % 每个块的20行都标记为当前块的索引i
end

% 指定保存路径
outputFilePath = 'C:\Users\user\Desktop\计算机视觉和模式识别\test\my.mat';

% 保存数据到指定文件
save(outputFilePath, 'myX', 'myY');
