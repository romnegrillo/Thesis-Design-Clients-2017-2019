function decreasedContrast=func_decrease_contrast(imagePath)

i=imread(imagePath);
if(size(i,3)==3)
    decreasedContrast=imadjust(i,[.5 .5 .5; .6 .6 .6],[]);
else
    msgbox(["Input image must have 3 channels!","Ex: RGB"],"Error");
end
 
