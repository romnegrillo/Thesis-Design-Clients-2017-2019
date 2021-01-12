function removedBackground=func_remove_background(imagePath)

i=imread(imagePath);
if(size(i,3)==3)
    gray=rgb2gray(i);
    filtered=imgaussfilt(gray,5);
    se = strel('disk',10);
    morp=imopen(filtered,se);
    
    level=graythresh(morp);
    mask=imbinarize(morp,level);
    mask=imcomplement(mask);
    mask=imfill(mask,'holes');
    
    masked=bsxfun(@times, i, cast(mask, 'like', i));
     
    removedBackground=masked;
else
    msgbox(["Input image must have 3 channels!","Ex: RGB"],"Error");
end
 
