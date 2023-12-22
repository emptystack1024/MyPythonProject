%% 初始化
clear ; close all; clc

% 加载数据
fprintf('加载和展示数据 ...\n')

load(['r_test.mat']);
m = size(myX, 1);

% 随机选择 100 个数据点进行显示
sel = randperm(size(myX, 1));
sel = sel(1:20);

displayData(myX(sel, :));

fprintf('程序暂停。按回车键继续。\n');
pause;

% 加载权重变量 Theta1 和 Theta2 
load('weights.mat');

%  执行 "predict "函数，使用神经网络预测训练集的标签。
%  计算训练集的准确率。

pred = predict(Theta1, Theta2, myX);

fprintf(['\n正确率： %f\n'], mean(double(pred == myY)) * 100);

fprintf('程序暂停，按回车键继续。\n');
pause;

%  为了让您了解网络的输出结果，您还可以逐个运行示例，看看它预测了什么。

%  随机排列示例
rp = randperm(m);

for i = 1:m
    % Display q
    result = myY(rp(i));
    displayData(myX(rp(i), :));

    pred = predict(Theta1, Theta2, myX(rp(i),:));
    fprintf('\n神经网络预测： %d (实际值：%d)\n', mod(pred,10), mod(result,10));
    
    % Pause with quit option
    s = input('暂停中 - 按回车键继续，按 q 键退出：','s');
    if s == 'q'
      break
    end
end

