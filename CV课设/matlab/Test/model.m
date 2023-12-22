clear;
clc

data = load("data.mat");
images = data.gTruth.DataSource;
images = images.Source;

size(images)

bbox = data.gTruth.LabelData;
bbox = bbox.word;

for i = 1:size(images)
    image_path = images{i};
    Matrix = imread(image_path);

    typecheck = bbox{i};

    single = bbox{i,1};
    
    for j = 1:size(single)
        single_m{j} = single(j,:);
    end

    figure;

    FirstImage = insertShape(Matrix,"polygon",single_m{1},"LineWidth",3);
    for j = 2:size(single)
        FirstImage = insertShape(FirstImage,"polygon",single_m{j},"LineWidth",3);
    end
    imshow(FirstImage);
end