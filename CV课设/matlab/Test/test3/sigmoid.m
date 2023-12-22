function g = sigmoid(z)
% 计算 sigmoid 函数
g=zeros(size(z));
g = 1.0 ./ (1.0 + exp(-z));
end
