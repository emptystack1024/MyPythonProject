% 所有代码作用：
%     lrCostFunction.m (逻辑回归的代价函数)
%     oneVsAll.m
%     predictOneVsAll.m
%     predict.m

%% 初始化
clear ; close all; clc

%% 设置参数
input_layer_size  = 400;  % 数字输入图像大小：20*20
hidden_layer_size = 25;   % 25个隐藏单元
num_labels = 10;          % 10个标签

%% =========== Part 1: 加载数据和表示数据 =============

% 加载数据
fprintf('加载和展示数据 ...\n')

load('ex3data1.mat');
m = size(X, 1);

% 随机选择 100 个数据点进行显示
sel = randperm(size(X, 1));
sel = sel(1:100);

displayData(X(sel, :));

fprintf('程序暂停。按回车键继续。\n');
pause;

%% ================ Part 2: 加载参数 ================
% 加载一些预初始化的神经网络参数

fprintf('\n加载已保存的神经网络参数 ...\n')

% 加载权重变量 Theta1 和 Theta2 
load('ex3weights.mat');

%% ================= Part 3: 预测 =================
%  训练完神经网络后，我们想用它来预测标签。
%  执行 "predict "函数，使用神经网络预测训练集的标签。
%  您就可以计算训练集的准确率。

pred = predict(Theta1, Theta2, X);

fprintf('\n训练集精度： %f\n', mean(double(pred == y)) * 100);

fprintf('程序暂停，按回车键继续。\n');
pause;

%  为了让您了解网络的输出结果，您还可以逐个运行示例，看看它预测了什么。

%  随机排列示例
rp = randperm(m);

for i = 1:m
    % Display 
    fprintf('\n展示实例。。。\n');
    displayData(X(rp(i), :));

    pred = predict(Theta1, Theta2, X(rp(i),:));
    fprintf('\n神经网络预测： %d (实际值：%d)\n', pred, mod(pred, 10));
    
    % Pause with quit option
    s = input('暂停中 - 按回车键继续，按 q 键退出：','s');
    if s == 'q'
      break
    end
end

