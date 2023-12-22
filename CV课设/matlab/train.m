% 画图
figure;

% 绘制输入层到隐藏层的箭头
for i = 1:size(Theta1, 1)
    for j = 1:size(Theta1, 2)
        weight = Theta1(i, j);
        quiver(0, i, 1, j-i, 'MaxHeadSize', 0.5, 'LineWidth', abs(weight)*5, 'Color', 'b');
        text(0, i, sprintf('X%d', i), 'HorizontalAlignment', 'right');
        text(1, j, sprintf('A%d', j), 'HorizontalAlignment', 'left');
    end
end

% 绘制隐藏层到输出层的箭头
for i = 1:size(Theta2, 1)
    for j = 1:size(Theta2, 2)
        weight = Theta2(i, j);
        quiver(2, i, 3, j-i, 'MaxHeadSize', 0.5, 'LineWidth', abs(weight)*5, 'Color', 'r');
        text(2, i, sprintf('A%d', i), 'HorizontalAlignment', 'right');
        text(3, j, sprintf('O%d', j), 'HorizontalAlignment', 'left');
    end
end

axis off;
