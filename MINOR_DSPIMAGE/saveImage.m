function imagePath=save_image(imageName,image)

%  Opens an open file dialog box for saving.
%  Returns the file name if a file is selected and save button is
%  clicked.
%  Returns 0 when cancel or X button is clicked.
[file,path]=uiputfile(imageName);

if isequal(file,0)
    disp("User did not select any file");
    imagePath=0;
else
    fullPath=fullfile(path,file);
    disp(file);
    imwrite(image,fullPath);
end
