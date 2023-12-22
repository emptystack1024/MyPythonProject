%% 初始化
clear ; close all; clc

num_labels = 10;          % 10个标签

% 加载数据
fprintf('加载和展示数据 ...\n')

load('data.mat');
m = size(X, 1);

% Randomly select 100 data points to display
rand_indices = randperm(m);
sel = X(rand_indices(1:100), :);

displayData(sel);

fprintf('程序暂停。按回车键继续。\n');
pause;

% 加载一些预初始化的神经网络参数

fprintf('\n使用正则化测试lrCostFunction()\n');

theta_t = [-2; -1; 1; 2];
X_t = [ones(5,1) reshape(1:15,5,3)/10];
y_t = ([1;0;1;0;1] >= 0.5);
lambda_t = 3;
[J grad] = lrCostFunction(theta_t, X_t, y_t, lambda_t);

fprintf('代价：%f\n', J);
fprintf('梯度:\n');
fprintf(' %f \n', grad);

fprintf('程序暂停。按回车键继续。\n');
pause;

fprintf('\n训练一对多逻辑回归...\n')

lambda = 0.1;
[all_theta] = oneVsAll(X, y, num_labels, lambda);

fprintf('程序暂停。按回车键继续。\n');
pause;

load('result.mat')

pred = predictOneVsAll(all_theta, myX);

fprintf('\n训练集精度: %f\n', mean(double(pred == myY)) * 100);

