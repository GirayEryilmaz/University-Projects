

load('classGrades'); %load the .mat file

namesAndGrades(1:5,:)  %print a sample portion two verify whats inside

grades = namesAndGrades(:,2:end);  %chop off first column
meanGrades = mean(grades)           %take means of grades of each assignment (columns)
meanGrades = nanmean(grades)        % since NaNs cause problem use nanmean instead
meanMatrix = ones(15,1)*meanGrades
curvedGrades = (grades*3.5)./meanMatrix;

%i would do something like  this instead --> curvedGrades = (grades(:,:)*3.5)./meanGrades(1,:)

nanmean(curvedGrades)            % since NaNs cause problem use nanmean instead

curvedGrades(find(curvedGrades>5)) = 5; %find is not necessary here. make all entries bigger than 5 , 5

totalGrade = nanmean(curvedGrades.').'; %trnspose, nanmean, transpose

ceiledtotalGrade =ceil(totalGrade) ;    %ceil the doubles

letters = ['F' 'D' 'C' 'B' 'A'];     %the array of letters

letterGrades = letters(ceiledtotalGrade);   %nice functional programming trick

disp(['Grades: ',letterGrades]) %display