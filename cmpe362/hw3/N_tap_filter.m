clearvars;
close all;

[mike,fs] = audioread('mike.wav');



n = size(mike,1);




x = mike;

sum1 = mike;

%% Constant N, K ;  a : 0 -> 1

N = 10;
K = 100;
delay = int64( K/1000 * fs);

snr_1 = [];

for a = 0 : 0.2 : 1
    
    sum1 = mike;
    
    for i = 1:N
    
        temp =  [zeros(delay * i,1) ; mike] * (a^i) ;

        
        %size([sum ; zeros(delay ,1)])
        %size(temp)
        %i
        sum1 = [sum1 ; zeros(delay ,1)] + temp;

    
    end
    
    sum_temp = sum1(1:n);
    snr_HandMade = 10*log10( sum(mike.^2) / sum((sum_temp-mike).^2) );
    
    snr_1 = [snr_1 snr_HandMade];

end

figure
plot(snr_1);
title('Constant N, K ;  a : 0 -> 1');


%% Constant K , a ; N : 1 -> 50


a = -0.5;
K = 100;
delay = int64( K/1000 * fs);

snr_2 = [];

for N = 1 : 50
    
    sum1 = mike;
    
    for i = 1:N
    
        temp =  [zeros(delay * i,1) ; mike] * (a^i) ;

        
        %size([sum ; zeros(delay ,1)])
        %size(temp)
        %i
        sum1 = [sum1 ; zeros(delay ,1)] + temp;

    
    end
    sum_temp =  sum1(1:n);
    snr_HandMade = 10*log10( sum(mike.^2) / sum((sum_temp-mike).^2) );
    snr_2 = [snr_2 snr_HandMade];

end

figure
plot(snr_2);
title('Constant K , a ; N : 1 -> 50');


%% Constatnt a , N ; K :  [100 200 300 400]

N = 10;
a = -0.5;


snr_3 = [];

for K = 100 : 100 : 400
    
    delay = int64( K/1000 * fs);
    
    sum1 = mike;
    K;
    
    for i = 1:N
    
        i;
        temp =  [zeros(delay * i,1) ; mike] * (a^i) ;

        sum1 = [sum1 ; zeros(delay ,1)] + temp;

    
    end
    
    %% have to calculate snr here
    sum_temp = sum1(1:n);
    snr_HandMade = 10*log10( sum(mike.^2) / sum((sum_temp-mike).^2) );
    snr_3 = [snr_3 snr_HandMade];

end

figure
plot(snr_3);
title('Constatnt a , N ; K :  [100 200 300 400]');



