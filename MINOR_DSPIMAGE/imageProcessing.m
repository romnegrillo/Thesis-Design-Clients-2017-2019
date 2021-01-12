function processedImage=imageProcessing(img, currentView)

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
    
    contrast=imadjust(img,[0 0 0; .6 .6 .6],[]);
    decreasedContrast=imadjust(img,[.5 .5 .5; .6 .6 .6],[]);
    
    if(currentView==1)
        processedImage=gray;
    elseif(currentView==2)
        processedImage=morp;   
    elseif(currentView==3)
        processedImage=contrast;
    elseif(currentView==4)
        processedImage=decreasedContrast;
    elseif(currentView==5)
        processedImage=mask;
    elseif(currentView==6)
        processedImage=masked;
    end
else
    processedImage=0;
end