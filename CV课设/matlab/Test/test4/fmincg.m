function [X, fX, i] = fmincg(f, X, options, P1, P2, P3, P4, P5)
% 最小化连续微分多元函数
% 起点由 "X"（D 乘 1）给出，以字符串 "f "命名的函数必须返回一个函数值和一个偏导数向量。
% 使用共轭梯度的 Polack- Ribiere flavour 计算搜索方向，使用二次多项式和三次多项式近似和 Wolfe-Powell 停止准则进行直线搜索，并使用斜率比方法猜测初始步长。
% 此外，还进行了一系列检查，以确保正在进行的探索和外推不会无限制地扩大。
% 长度 "给出了运行的长度：如果是正数，则给出了线性搜索的最大次数；如果是负数，则给出了函数求值的最大允许次数。
% 您还可以（选择性地）为 "length "添加第二个分量，它将显示第一次行搜索时函数值的预期减少量（默认值为 1.0）。
% 如果函数的长度已满，或者无法取得进一步的进展（即已达到最小值，或者由于数值问题已非常接近，无法再进一步），函数就会返回。
% 如果函数在迭代几次后就终止了，这可能表明函数值和导数不一致（即 "f "函数的实现可能存在错误）。
% 该函数返回找到的解决方案 "X"、函数值向量 "fX"（表示取得的进展）和迭代次数 "i"（行搜索或函数求值，取决于迭代次数）。

% Read options
if exist('options', 'var') && ~isempty(options) && isfield(options, 'MaxIter')
    length = options.MaxIter;
else
    length = 100;
end


RHO = 0.01; % 行搜索的一系列常数
SIG = 0.5; % RHO 和 SIG 是沃尔夫-鲍威尔条件中的常数
INT = 0.1; % 在当前括号极限的 0.1 范围内不重新评估
EXT = 3.0; % 外推最大值为当前括号的 3 倍
MAX = 20; % 每行搜索最多 20 次函数评估
RATIO = 100; % 最大允许坡比

argstr = ['feval(f, X']; % 缀合字符串
for i = 1:(nargin - 3)
  argstr = [argstr, ',P', int2str(i)];
end
argstr = [argstr, ')'];

if max(size(length)) == 2, red=length(2); length=length(1); else red=1; end
S=['Iteration '];

i = 0; % 将运行长度计数器清零
ls_failed = 0;  % 标志没有前一条线路搜索失败
fX = [];
[f1 df1] = eval(argstr); % 获取函数值和梯度
i = i + (length<0);
s = -df1; % 搜索最陡梯度
d1 = -s'*s;
z1 = red/(1-d1);

while i < abs(length) 
  i = i + (length>0); 

  X0 = X; f0 = f1; df0 = df1; % 复制当前值
  X = X + z1*s; % 开始行搜索
  [f2 df2] = eval(argstr);
  i = i + (length<0);
  d2 = df2'*s;
  f3 = f1; d3 = d1; z3 = -z1;
  if length>0, M = MAX; else M = min(MAX, -length-i); end
  success = 0; limit = -1; % 初始化
  while 1
    while ((f2 > f1+z1*RHO*d1) || (d2 > -SIG*d1)) && (M > 0) 
      limit = z1;
      if f2 > f1
        z2 = z3 - (0.5*d3*z3*z3)/(d3*z3+f2-f3); % 二次拟合
      else
        A = 6*(f2-f3)/z3+3*(d2+d3);
        B = 3*(f3-f2)-z3*(d3+2*d2);
        z2 = (sqrt(B*B-A*d2*z3*z3)-B)/A;
      end
      if isnan(z2) || isinf(z2)
        z2 = z3/2; 
      end
      z2 = max(min(z2, INT*z3),(1-INT)*z3); 
      z1 = z1 + z2; % 更新步骤
      X = X + z2*s;
      [f2 df2] = eval(argstr);
      M = M - 1; i = i + (length<0);
      d2 = df2'*s;
      z3 = z3-z2; % z3 现在相对于 z2 的位置
    end
    if f2 > f1+z1*RHO*d1 || d2 > -SIG*d1
      break;
    elseif d2 > SIG*d1
      success = 1; break;
    elseif M == 0
      break;
    end
    A = 6*(f2-f3)/z3+3*(d2+d3);
    B = 3*(f3-f2)-z3*(d3+2*d2);
    z2 = -d2*z3*z3/(B+sqrt(B*B-A*d2*z3*z3));
    if ~isreal(z2) || isnan(z2) || isinf(z2) || z2 < 0
      if limit < -0.5
        z2 = z1 * (EXT-1);
      else
        z2 = (limit-z1)/2;
      end
    elseif (limit > -0.5) && (z2+z1 > limit)
      z2 = (limit-z1)/2;
    elseif (limit < -0.5) && (z2+z1 > z1*EXT)
      z2 = z1*(EXT-1.0);
    elseif z2 < -z3*INT
      z2 = -z3*INT;
    elseif (limit > -0.5) && (z2 < (limit-z1)*(1.0-INT)) 
      z2 = (limit-z1)*(1.0-INT);
    end
    f3 = f2; d3 = d2; z3 = -z2; % 设置第 3 点等于第 2 点
    z1 = z1 + z2; X = X + z2*s; % 更新当前估计
    [f2 df2] = eval(argstr);
    M = M - 1; i = i + (length<0); 
    d2 = df2'*s;
  end

  if success % 如果行搜索成功
    f1 = f2; fX = [fX' f1]';
    fprintf('%s %4i | Cost: %4.6e\r', S, i, f1);
    s = (df2'*df2-df1'*df2)/(df1'*df1)*s - df2; 
    tmp = df1; df1 = df2; df2 = tmp;
    d2 = df1'*s;
    if d2 > 0 % 新斜率必须为负值
      s = -df1; %取负
      d2 = -s'*s;    
    end
    z1 = z1 * min(RATIO, d1/(d2-realmin)); % 最大坡度比
    d1 = d2;
    ls_failed = 0;
  else
    X = X0; f1 = f0; df1 = df0;
    if ls_failed || i > abs(length) % 行搜索连续两次失败
      break;
    end
    tmp = df1; df1 = df2; df2 = tmp;
    s = -df1;
    d1 = -s'*s;
    z1 = 1/(1-d1);                     
    ls_failed = 1;
  end
  if exist('OCTAVE_VERSION')
    fflush(stdout);
  end
end
fprintf('\n');
