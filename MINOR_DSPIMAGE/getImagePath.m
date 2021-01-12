function imagePath=getImagePath()

%  Opens an open file dialog box for selecting.
%  Returns the file and path when a file is selected and open button is
%  clicked.
%  Returns 0 when cancel or X button is clicked.
[file,path]=uigetfile('*.jpg;*.png');

if isequal(file,0)
   %disp("User did not select any file");
   imagePath=0;
else
   %disp(file);
   %disp(path);
   fullPath=fullfile(path,file);
   %disp(fullPath); 
   imagePath=fullPath;
end

