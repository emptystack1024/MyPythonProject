function y=cutting(I)   % 获取图像的有效数据区域（多个字符或者单个字符均可使用）
[m,n] = size(I);
top = 1;
bottom = m;
left =1;
right = n;
while sum(I(top,:)) == 0 && top < m
    top = top+1;
end
while sum(I(bottom,:)) == 0 && bottom >= 1
    bottom = bottom - 1;
end
while sum(I(:,left)) == 0 &&  left<n
    left = left+1;
end
while sum(I(:,right)) == 0 && right >= 1
    right = right -1;
end
height = bottom - top;
width = right - 1;
y = imcrop(I,[left,top,width,height]);
end
