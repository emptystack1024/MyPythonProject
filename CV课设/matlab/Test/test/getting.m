function [word,result] = getting(I)
word = [];
flag = 0;
y1 = 8;
y2 = 0.5;
% word:字符矩阵、flag：标志位、y1/y2:字符大小阈值
while flag == 0
    [m,n] = size(I);
    wide = 0;
    
    if m==0 | n==0  % 无空余字符，提取完毕
        break;
    end
    % 从左至右寻找为0的列作为分割线，由于前面的处理左侧肯定不为零
    while  (sum(I(:,wide+1)) ~= 0  && wide <= n-2 ) 
        wide = wide + 1;
    end
    
    % 裁剪出第一个字符区域
    temp = cutting(imcrop(I,[1,1,wide,m]));
    [m1,n1] = size(temp);
    if wide < y1 && n1/m1 > y2  %判断是否是一个字符
        I(:,1:wide) = 0;        %判定为无效字符，清零，下面肯定是零
        if sum(sum(I)) ~= 0     %不为零，说明还有字符
            I = cutting(I);
            flag = 1;
        else                    %为零，说明没有字符
            word = []; 
            flag = 1;
        end
    else
        word = cutting(imcrop(I,[1,1,wide,m]));     %有效字符，提取
        I(:,1:wide) = 0;
        if sum(sum(I)) ~= 0
            I = cutting(I);
            flag =  1;
        else
            I = [];
        end
    end
end
result = I;
end
