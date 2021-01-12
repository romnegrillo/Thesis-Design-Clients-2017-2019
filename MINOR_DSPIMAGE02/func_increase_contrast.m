function increasedContrast=func_increase_contrast(imagePath)

i=imread(imagePath);
if(size(i,3)==3)
    increasedContrast=imadjust(i,[0 0 0; .6 .6 .6],[]);
else
    msgbox(["Input image must have 3 channels!","Ex: RGB"],"Error");
end
 
