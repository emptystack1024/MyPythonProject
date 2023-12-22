function [all_theta] = oneVsAll(X, y, num_labels, lambda)
% 训练num_labels逻辑回归分类器，并在矩阵all_theta中返回每个分类器，其中all_theta的第i行对应标签i的分类器。

m = size(X, 1); % 获取样本数量
n = size(X, 2); % 获取特征数量

all_theta = zeros(num_labels, n + 1);

X = [ones(m, 1) X]; % 输入矩阵 X 的第一列添加一列全为 1 的偏置项

for c=1:num_labels % 执行多次逻辑回归模型训练
    initial_theta = zeros(n + 1, 1); % 初始化逻辑回归的参数，包括偏置项
    options = optimset('GradObj', 'on', 'MaxIter', 100); % 设置优化选项
                % 其中 'GradObj' 表示使用梯度，'MaxIter' 表示最大迭代次数。
    [theta] = fmincg (@(t)(lrCostFunction(t, X, (y == c), lambda)), ... % 成本函数
        initial_theta, options);
    all_theta(c,:)=theta'; % 将训练得到的参数存储在矩阵 all_theta 中，其中每一行对应一个类别的参数。

end
