function processedImage=imageProcessing(imagePath, currentView)

img=imread(imagePath);

% Check if it is a 3 channel image.
if(size(img,3)==3)
    gray=rgb2gray(img);
    filtered=imgaussfilt(gray,5);
    se = strel('disk',10);
    morp=imopen(filtered,se);
    
    level=graythresh(morp);
    mask=imbinarize(morp,level);
    mask=imcomplement(mask);
    mask=imfill(mask,'holes');
    
    masked=bsxfun(@times, img, cast(mask, 'like', img));
    
    contrast=imadjust(gray);
    
    if(currentView==1)
        % Object separated from background.
        processedImage=masked;
    elseif(currentView==2)
        % Gray scale image.
        processedImage=gray;   
    elseif(currentView==3)
        % Filtered image.
        processedImage=filtered;
    elseif(currentView==4)
        % Morphologically Open.
        processedImage=morp;    
    elseif(currentView==5)
        % Binary Image.
        processedImage=mask;        
    elseif(currentView==6)
        processedImage=contrast;            
    end
else
    processedImage=0;
    msgbox(["Input image must have 3 channels!","Ex: RGB"],"Error");
end