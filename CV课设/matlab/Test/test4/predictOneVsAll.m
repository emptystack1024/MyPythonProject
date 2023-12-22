function p = predictOneVsAll(all_theta, X)
% 为训练有素的单一分类器预测标签。标签范围为 1...K，其中 K = size(all_theta,1)。

m = size(X, 1);

% 输入矩阵 X 的第一列添加一列全为 1 的偏置项
X = [ones(m, 1) X];

% 使用 max 函数可以将这些代码全部矢量化。
% 特别是，max 函数还可以返回最大元素的索引。   
h=all_theta*X'; % 计算每个类别的预测概率
[~,t]=max(h);  % 使用 max 函数找到每列中的最大值及其索引，即找到每个样本最可能的类别。
p=t';

end
