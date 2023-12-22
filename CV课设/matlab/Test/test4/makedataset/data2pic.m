% 假设 pixelData 是你的一维像素数据
pixelData = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8.56059679589129e-06,1.94035947712170e-06,-0.000737438725490234,-0.00813403799019628,-0.0186104473039219,-0.0187412865354045,-0.0187572508169938,-0.0190963541666670,-0.0164039011437912,-0.00378191380718963,0.000330347315641443,1.27655228758175e-05,0,0,0,0,0,0,0,0.000116421568627451,0.000120052178875718,-0.0140444580610022,-0.0284542483660131,0.0803826593137254,0.266540339052287,0.273853746280217,0.278729541122004,0.274293607026144,0.224676402505447,0.0277562976579520,-0.00706315478374306,0.000234715413943356,0,0,0,0,0,0,1.28335523036485e-17,-0.000326286764705943,-0.0138651604092787,0.0815651552287582,0.382800381263617,0.857849775326799,1.00109761369826,0.969710638240051,0.930928598175382,1.00383757148693,0.964157356345316,0.449256552968409,-0.00560408258937712,-0.00378319035947713,0,0,0,0,5.10620915032699e-06,0.000436410675381265,-0.00395509940087153,-0.0268537241285404,0.100755014063837,0.642031709558823,1.03136837894880,0.850968613834423,0.543122378812637,0.342599737746797,0.268918777233116,0.668374642565360,1.01256958061002,0.903795598447711,0.104481574334515,-0.0166424972766885,0,0,0,0,2.59875259875275e-05,-0.00310606987077575,0.00752456075985418,0.177539830554536,0.792890119684788,0.965626503200032,0.463166078974902,0.0691720679955970,-0.00364100525865266,-0.0412180404598166,-0.0501900656312421,0.156102907205848,0.901762650659709,1.04748345630699,0.151055251825705,-0.0216044664574077,0,0,0,5.87012351718199e-05,-0.000640931372549019,-0.0323305249183003,0.278203465413944,0.936720162717865,1.04320956137133,0.598003216911763,-0.00359409041394353,-0.0216751770152506,-0.00481021922657953,6.16566793037421e-05,-0.0123773318355117,0.155477481617648,0.914867476851852,0.920401348039215,0.109173902409196,-0.0171058006535948,0,0,0.000156250000000000,-0.000427724104194688,-0.0251466503267976,0.130532560593682,0.781664862472768,1.02836582584423,0.757137601402307,0.284667194308278,0.00486865127995647,-0.00318688725490196,0,0.000836492601198491,-0.0370751123366011,0.452644165305011,1.03180133442266,0.539028101171023,-0.00243742611389710,-0.00480290032679740,0,0,-0.000703635620915023,-0.0127262443438917,0.161706648284313,0.779865383306100,1.03676705473856,0.804490400326797,0.160586723601429,-0.0138173338779958,0.00214879493464051,-0.000212622549019606,0.000204248366013082,-0.00685907627084111,0.000431712962962512,0.720680947031591,0.848136063453160,0.151383408224400,-0.0228404365904368,0.000198971949891070,0,0,-0.00940410539215690,0.0374520504667561,0.694389110157952,1.02844844430828,1.01648066448802,0.880488425925927,0.392123945212181,-0.0174122412854031,-0.000120098039215678,5.55215141612253e-05,-0.00223907271241832,-0.0276068376068379,0.368645492919390,0.936411168981481,0.459006723175382,-0.0424701797385617,0.00117356610003670,1.88929738562079e-05,0,0,-0.0193511950864893,0.129999794057517,0.979821705189353,0.941862388406506,0.775147704265351,0.873632240838124,0.212778349698981,-0.0172353348823938,0,0.00109937426113894,-0.0261793750764341,0.122872878993705,0.830812662209721,0.726501773266479,0.0524441862677157,-0.00618971913089534,0,0,0,0,-0.00936563861655777,0.0368349741143856,0.699079299428105,1.00293583197168,0.605704401552287,0.327299223856210,-0.0322099248569838,-0.0483053002450979,-0.0434069138071894,-0.0575151143790854,0.0955674189814816,0.726512626880274,0.695366966230938,0.147114481209151,-0.0120048679193900,-0.000302798202614329,0,0,0,0,-0.000676572712418302,-0.00651415555827330,0.117339358660130,0.421948410266884,0.993210937500000,0.882013973992375,0.745758733846969,0.723874268110022,0.723341724537038,0.720020339733116,0.845324959150327,0.831859738697974,0.0688831869553380,-0.0277765012254901,0.000359136710239646,7.14869281045701e-05,0,0,0,0,0.000153186274509804,0.000317353552647685,-0.0229167177287582,-0.00414402913943351,0.387038449754902,0.504583435457516,0.774885875694699,0.990037445533770,1.00769478485839,1.00851439950980,0.737905041530501,0.215455291264115,-0.0269624863834423,0.00132506127450980,0,0,0,0,0,0,0,0,0.000236366421568628,-0.00226031454248359,-0.0251994485294116,-0.0373889910130717,0.0662121227562403,0.291134497549019,0.323055725762527,0.306260314542483,0.0876070942265792,-0.0250581916758386,0.000237438725490189,0,0,0,0,0,0,0,0,0,0,0,6.20939215598928e-18,0.000672618319677154,-0.0113151410693297,-0.0354641066405776,-0.0388214911744327,-0.0371077412253886,-0.0133524927642576,0.000990964718493173,4.89176959765201e-05,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];  % 你的数据

% 图像大小
imageSize = [20, 20];

% 将一维数据转换为二维矩阵
imageMatrix = reshape(pixelData, imageSize);

% 显示图像
imshow(imageMatrix, []);

% 如果你想要更好的可视化，你可以添加一些选项，例如 colormap
colormap(gray);  % 使用灰度颜色映射

% 添加标题
title('显示图像');
