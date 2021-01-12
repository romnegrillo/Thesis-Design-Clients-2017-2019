function grayImage=func_gray(imagePath)

i=imread(imagePath);
if(size(i,3)==3)
    grayImage=rgb2gray(i);
else
    msgbox(["Input image must have 3 channels!","Ex: RGB"],"Error");
end
 
