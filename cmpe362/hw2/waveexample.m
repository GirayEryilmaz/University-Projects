%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   CMPE 362 Homework II-b   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%

                                                % Fs is the frequency = number of samples per second
                                                % y is the actual sound data 
hfile = 'laughter.wav';                         % This is a string, corresponding to the filename
clear y Fs                                      % Clear unneded variables

%% PLAYING A WAVE FILE

[y, Fs] = audioread(hfile);      % Read the data back into MATLAB, and listen to audio.
                                                % nbits is number of bits per sample
sound(y, Fs);                                   % Play the sound & wait until it finishes

duration = numel(y) / Fs;                       % Calculate the duration
pause(duration + 2)                             % Wait that much + 2 seconds

%% CHANGE THE PITCH

sound(y(1:2:end), Fs);                          % Get rid of even numbered samples and play the file

duration = numel(y) / (Fs*2);                     
pause(duration + 2)                            
%% EXERCISE I
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   Re-arrange the data so that   %
%   the frequency is quadrupled and play the file   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


sound(y(1:4:end),Fs);                                   

duration = numel(y) / (4*Fs);                     
pause(duration + 2)                    
                                                
                              
%% EXERCISE II
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   Re-arrange the data so that   %
%   the frequency is halved and play the file  %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

zeroArr = zeros(2*size(y,1),1);
zeroArr(1:2:end) = y;
sound(zeroArr,Fs)
duration = numel(y) / (Fs/2);                       % Calculate the duration
pause(duration + 2)
                            
                                                
                                                
%% EXERCISE III 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   Double Fs and play the sound  %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

sound(y, 2*Fs);                                   % Play the sound & wait until it finishes

duration = numel(y) / (2*Fs);                       % Calculate the duration
pause(duration + 2) 


%% EXERCISE IV
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   Divide Fs by two and play the sound  %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


sound(y, Fs/2);                                   % Play the sound & wait until it finishes

duration = numel(y) / (Fs/2);                       % Calculate the duration
pause(duration + 2) 

