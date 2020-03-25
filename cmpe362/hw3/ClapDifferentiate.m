clearvars;
close all;

[sound,fs]=audioread('snap.wav');


sound = sound(:,1);


figure;
spectrogram(sound,[],[],[],fs,'yaxis')
%spectrogram(clap,'yaxis');


N_sound = size(sound,1);

sound_freq = fft(sound, N_sound)/N_sound; 
sound_freq_shifted = fftshift(sound_freq);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Wn = (17000/(fs/2));
[B,A] = butter(10,Wn,'high');

Y_sound = filter(B,A,sound);

figure;
spectrogram(Y_sound,[],[],[],fs,'yaxis');
%spectrogram(clap,'yaxis');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%

th_fr = 17000;

baseFreq = (2/ fs) * N_sound;

n_1 = int64(th_fr*baseFreq);



above_th_pow = abs(sound_freq);

max_above_th = max(above_th_pow(n_1:end));


if  max_above_th > 0.0006
    sprintf('clap sound detected')
else
    sprintf('Snap sound detected')
end





