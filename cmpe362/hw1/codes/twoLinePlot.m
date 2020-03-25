 

   t = linspace(0,2*pi,100); %intialize time between 0 and 2pi, 100 pieces
   
   figure; %instantiate a figure
   
   plot(t,sin(t)); %plot t sin(t) vs t
   hold on;         %hold it at hand
   
   plot(t,cos(t),'--');     %plot cos(t) vs t with desired assets
   xlabel('xlabel');        %label x axis
   ylabel('ylabel');        %label y axis
   title('title');          %title
   legend('Sin','Cos')      %the legend
   
   xlim([0 2*pi]);          %adjsut x and y axis's so that it look nicer
   ylim([-1.4 1.4]);
