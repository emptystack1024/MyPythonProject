function words = getting_chars_from_file(filename)

I_RGB = imread(filename);
% 彩转灰
I_GRAY = rgb2gray(I_RGB); 
I_THRESH = imbinarize(I_GRAY,0.9);

% 腐蚀膨胀处理，相对亮的区域来说
% 膨胀，使白色区域扩大；
% 腐蚀，使黑色区域扩大；
% Y方向腐蚀
Seed_Y= [1;1;1];
I_TEMP = imdilate(I_THRESH,Seed_Y);
I_TEMP = imerode(I_TEMP,Seed_Y);
% X方向腐蚀
Seed_X = [1 1 1];
I_TEMP = imdilate(I_TEMP,Seed_X);
I_TEMP = imerode(I_TEMP,Seed_X);

% 预处理结果
I_PRE = I_TEMP;

% 反色
I_REGION = (I_PRE ~= 1);

% 区域提取函数（和前面的功能重复了）
I_CUT = cutting(I_REGION);

% 提取字符

k=0; %Wmax: 字符集最大容量
while size(I_CUT,2) > 10
    [words{k+1},I_CUT] = getting(I_CUT);
    k = k+1;
end

% 大小标准化
cnt = k;
for j = 1:cnt    
    words{j} = imresize(words{j},[40,30]);
end

end
