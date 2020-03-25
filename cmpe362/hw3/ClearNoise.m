clearvars;
close all;

[mike,fs] = audioread('mike.wav');

[street,fs_2] = audioread('street.wav');

%note that fs = fs_2, so i will use fs for both, whenever needed.

mixed = mike + street;

figure
spectrogram(mike,[],[],[],fs,'yaxis')
title('mike')

figure
spectrogram(street,[],[],[],fs,'yaxis')
title('street')

N = size(mike,1);

%% 1-)Frequency Domain Representation of Mike.wav, Street.wav, Mike+Street.wav
df = fs / N;
w = (-(N/2):(N/2)-1)*df;

mike_freq = fft(mike, N)/N; 
mike_freq_shifted = fftshift(mike_freq);


street_freq = fft(street, N)/N; 
street_freq_shifted = fftshift(street_freq);


mixed_freq = fft(mixed, N)/N; 
mixed_freq_shifted = fftshift(mixed_freq);


figure;
subplot(1,3,1);
plot(w,abs(mike_freq_shifted));
title('mike');


subplot(1,3,2);
plot(w,abs(street_freq_shifted));
title('street')

subplot(1,3,3);
plot(w,abs(mixed_freq_shifted));
title('mike+street');

%% 2-)Time Domain Representation of Mike.wav, Street.wav, Mike+Street.wav

figure;

subplot(3,1,1);
plot(w,abs(mike));
title('mike');

subplot(3,1,2);
plot(w,abs(street));
title('street');

subplot(3,1,3);
plot(w,abs(mixed));
title('mike+street');


%% Filter

n = 1;
beginFreq = 300 / (fs/2); %300Hz 
endFreq = 5000 / (fs/2);  %5000Hz
[b,a] = butter(n, [beginFreq, endFreq], 'bandpass');


filtered_mixed_freq = filter(b, a, mixed_freq);
filtered_mixed = ifft(filtered_mixed_freq);
%filtered_mixed = filter(b, a, mixed);

filtered_mixed = real((filtered_mixed))*N;
%sound(filtered_mixed,fs)





%% 3-)Frequency Domain Representation of Mike.wav, Filtered Mike+Street.wav

figure;
subplot(1,2,1);
plot(w,abs(mike_freq_shifted));
title('3-mike');


filtered_mixed_freq_shifted = fftshift(filtered_mixed_freq);
subplot(1,2,2);
plot(w,abs(filtered_mixed_freq_shifted));
title('3-mike+street filtered');

%filtered_mixed_freq = fft(filtered_mixed, N)/N; 
%filtered_mixed_freq_shifted = fftshift(filtered_mixed_freq);

%subplot(1,2,2);
%plot(w,abs(filtered_mixed_freq_shifted));
%title('3-mike+street filtered');



%% 4-)Time Domain Representation of Mike.wav, Filtered Mike+Street.wav

figure;
subplot(1,2,1);
plot(w,abs(mike));
title('mike');



subplot(1,2,2);
plot(w,abs(filtered_mixed));
title('mike+street filtered');


%% SNR
%temp = fft(mike);
snr_HandMade = 10*log10( sum(mike.^2) / sum((filtered_mixed-mike).^2) )

%10*log10( sum(mike.^2) / sum((mixed-mike).^2) )

%snr_Matlab =  snr(mike,mixed-street)


    
   
