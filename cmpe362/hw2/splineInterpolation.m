close all;
y = [1025, 1400, 1710, 2080, 2425, 2760, 3005, 2850, 2675];
x = [265,  400,  500,  700,  950,  1360, 2080, 2450, 2940];
N  =   length(x)-1;

b = [1025;1400;1400;1710;1710;2080;2080;2425;
    2425;2760;2760;3005;3005;2850; 2850;2675;
    0;  0;  0;  0;  0;  0;  0;  0; ];

A = zeros(3*N);

col = 1;
for i = 2:N+1
    A(2*i-3,col:col+2) = [x(i-1)^2, x(i-1), 1];
    A(2*i-2, col:col+2) = [x(i)^2, x(i), 1];
    col = col + 3;
end

col = 1;
for i = 2*N+1:3*N-1
    A(i,col:col+4) = [x(i-2*N+1)*2, 1, 0, -2*x(i-2*N+1),-1];
    col = col + 3;
end

A(3*N,1) = 1;

Results = linsolve(A,b);

hold on;

j=1;
for i=1:N
    %           a* x^2        +  b*x + c
    curve=@(l) Results(j)*l.^2+Results(j+1)*l+Results(j+2);
    ezplot(curve,[x(i),x(i+1)]);
    hold on
    j=j+3;
end

%plot the graph
scatter(x,y,'r','filled')
grid on;

xlim([0 3000]);
ylim([0 3500]);

xlabel('x');
ylabel('y');

title('Quadratic Spline InterPolation')
