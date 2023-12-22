I_RGB = imread("ABC.png");
figure;imshow(I_RGB);title("原始图片");
% 彩转灰
I_GRAY = rgb2gray(I_RGB);  
figure;imshow(I_GRAY);title("灰度图片");
% 阈值分割,使用 Otsu 方法计算全局图像阈值，最大类间方差法
% thresh = graythresh(I_GRAY);
% I_THRESH = im2bw(I_GRAY,thresh);
% I_THRESH = imbinarize(I_GRAY);  %默认使用Otsu方法,有字符被去除
% I_THRESH = imbinarize(I_GRAY,'adaptive','Sensitivity',0.62);
I_THRESH = imbinarize(I_GRAY,0.9);

figure;imshow(I_THRESH);title("阈值处理，二值化");
% 腐蚀膨胀处理，相对亮的区域来说
% 膨胀，使白色区域扩大；
% 腐蚀，使黑色区域扩大；
% Y方向腐蚀
Seed_Y= [1;1;1];
I_TEMP = imdilate(I_THRESH,Seed_Y);
figure;imshow(I_TEMP);title("Y膨胀");
I_TEMP = imerode(I_TEMP,Seed_Y);
figure;imshow(I_TEMP);title("Y腐蚀");

% X方向腐蚀
Seed_X = [1 1 1];
I_TEMP = imdilate(I_TEMP,Seed_X);
figure;imshow(I_TEMP);title("X膨胀");
I_TEMP = imerode(I_TEMP,Seed_X);
figure;imshow(I_TEMP);title("X腐蚀");
% 预处理结果
I_PRE = I_TEMP;

% 反色
I_REGION = (I_PRE ~= 1);
figure;imshow(I_REGION);title("反色");

% 区域提取函数（和前面的功能重复了）
I_CUT = cutting(I_REGION);
figure;imshow(I_CUT);title("完整有效区域截取");
% 提取字符
k=0; 
while size(I_CUT,2) > 10
    [word{k+1},I_CUT] = getting(I_CUT);
    k = k+1;
end
cnt = k;

for j = 1:cnt    
    set(gcf,'color',[0.9 0.4 0.2]);%任意RGB色 如果背景是白色的话，会和字符的颜色掺和在一起
    figure(5);subplot(10,5,j);imshow(word{j});title(int2str(j));
    word{j} = imresize(word{j},[40,30]);
    set(gcf,'color',[0.9 0.4 0.2]);%任意RGB色 如果背景是白色的话，会和字符的颜色掺和在一起
    figure(6),subplot(10,5,j);imshow(word{j});title(int2str(j));
end

chars = getting_chars_from_file("characters.png");
for i = 1 : size(chars,2)
    name = sprintf("C:/code/pythonProject/pythonProject/CV课设/matlab/Test/test/characters/%c.png",i+64);
    %name = strcat(int2str(i+64),".png");
    imwrite(chars{i},name);
end

