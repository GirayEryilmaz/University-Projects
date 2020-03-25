%close all

m = input('');
threshold = 0.225678;
i = 1;
while i <= m
    for j = 1:2
        fileName = strcat(num2str(i),strcat('-',strcat(num2str(j),'.wav')));
        
        clear y Fs;       
        [y, Fs] = audioread(fileName);
        
        
        y_1 = y(:,1);
        number_Of_Peeks = 0;
        radius = 0.2*(Fs);
        for k = 1:numel(y_1)
            if y_1(k) > threshold
                number_Of_Peeks = number_Of_Peeks + 1;
                y_1(k+1:k+radius) = 0;
            end
        end   
        
        if number_Of_Peeks == 1 
            sprintf('one clap')
        elseif number_Of_Peeks == 2
            sprintf('two claps')
        else
            number_Of_Peeks
        end
        
    end
    i = i + 1;
end