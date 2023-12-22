function  final = character_recognition(filename)
codecollection = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
word = getting_chars_from_file(filename);
cnt = size(word,2);
for p=1:cnt
    alarm = zeros(1,26);
    for o = 1:26
        char_name = sprintf("C:/code/pythonProject/pythonProject/CV课设/matlab/Test/test/characters/%c.png",o+'A'-1);
        refer = imread(char_name);
        %refer = im2bw(refer);
        for i=1:40
            for j = 1:30
                if(word{p}(i,j)) == refer(i,j)
                    alarm(1,o) = alarm(1,o)+1;
                end
            end
        end

        number = 1;
        for q = 1:26
            if alarm(1,q) > alarm(1,number)
                number = q;
            end
        end
        final(1,p) = codecollection(number);
    end
end
end
