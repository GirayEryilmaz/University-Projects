%scalar variables

%basic sclar variables
a = 10
b = 2.5 * 10.^25
c = 4 + 1i*3        % i means complex number i
d = exp(1i*2*pi/3)  % pi is the famous number pi, 3.14...  etc.

%vector variables

aVec = [ 3.14 16 19 26 ]        %an array
bVec = [2.71; 8;  28; 182]      %a vector. rows are separeted by semicolon ;
cVec = 5:-.2:-5                 %from  5 to -5, decreasing 2 at each step
dVec = logspace(0,1,101)        %nice little built-in function ; array of 101 elements 1 to 10 spaced logarithmicly
eVec = 'Hello'              % a string

%matrix variables
aMat = ones(9)*2                    %ones returns a matrix full of 1's
bMat = diag([1 2 3 4 5 4 3 2 1])    %did not need zeros
cMat = reshape(1:100,[10,10])       %re shape does what the name implies
dMat = NaN(3,4)                     %matrix of NaN's
eMat = [13  -1 5 ;  -22  10 -87]    %2 to 3 custom matrix
fMat = floor(7*(rand(5,3)))-3 %randi(6,5,3)-3 would make more sense

%4. Scalar equations
x = 1/(1+ exp(-(a-15)/6))           %exp means e over (...)
y = (sqrt(a) + b^(1/21))^pi         % square root
z = log(real((c+d)*(c-d))*sin(a*pi/3))./(c*conj(c)) %log -> natural log , real -> real part of a complex number
                                                    %conj -> conjugate of a
                                                    %complex number

%5. Vector equations
xVec = (1/(2*pi*2.5^2)^(1/2))*exp(-cVec.^2./(2*2.5^2))  %
yVec = ((aVec.').^2 + bVec.^2).^(1/2)                   %.' takes transpose
 zVec = log10(1./dVec)

%6 matrix
xMat = aVec*bVec*aMat^2
yMat = bVec*aVec
zMat = det(cMat)*((aMat.*bMat).')       % det takes determinat

%7Common functions
cSum = sum(cMat)                        %sum squizes matrix to an array by adding up all rows
eMean = mean(eMat,2)                    %means takes means of all rows

eMat = [1,1,1;eMat(2:end,:)]            %replace first row of eMat by concatenating 
                                        %one row with rest of the eMat(exculuding first row)
                                        
cSub = cMat(2:9,2:9)                    %take submatrix
lin = 1:20                              %then make every other value in it negative
lin(:,2:2:20) = -(lin(:,2:2:20))

r = rand(1,5)               %random numbers
r(find(r<0.5)) = 0 %here find is unnecessary r(r<0.5)=0 would do the trick


