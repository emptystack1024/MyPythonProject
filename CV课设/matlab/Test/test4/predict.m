function p = predict(Theta1, Theta2, X)
% 给定训练有素的神经网络，预测输入的标签 p = PREDICT(Theta1, Theta2, X) 输出给定神经网络的权重 (Theta1, Theta2)
% X 是输入的特征矩阵，每行对应一个样本，每列对应一个特征

m = size(X, 1);
num_labels = size(Theta2, 1);

p = zeros(size(X, 1), 1);

X=[ones(m,1),X];

% 首先计算第二层（隐藏层）的输入 z_2 和激活值 a_2
z_2=X*Theta1';
a_2=sigmoid(z_2);

% 在激活值中添加偏置单元
z_2=[ones(size(a_2,1),1),a_2];

% 然后计算输出层的输入 z_3 和激活值 a_3
z_3=z_2*Theta2';
a_3=sigmoid(z_3);

% 获取每个样本的预测标签
[~,p]=max(a_3,[],2);

end
