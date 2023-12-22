function [J, grad] = lrCostFunction(theta, X, y, lambda)
% 计算使用 theta 作为参数进行正则化逻辑回归的成本，以及成本与参数相关的梯度。

m = length(y); % 训练实例数

% 返回值
J = 0; % 初始化成本
grad = zeros(size(theta)); % 初始化梯度

% 计算成本
theta_1=[0;theta(2:end,1)]; % 排除第一个元素，用于正则化
% lambda 控制正则化的强度
J=1/m*(-y'*log(sigmoid(X*theta))-(1-y)'*log(1-sigmoid(X*theta)))+lambda/(2*m)*(theta_1'*theta_1);
grad=1/m*X'*(sigmoid(X*theta)-y)+lambda/m*theta_1; % 计算成本函数相对于参数的梯度。同样包括正则化项。

grad = grad(:);

end
