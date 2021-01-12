dirImages=char(strcat(pwd,'\MicroscopeImages'));
imgDirectory = imageDatastore(dirImages);
montage(imgDirectory,'Size', [6 20]);
MyMontage = getframe(gca);

dirStitched=char(strcat(pwd,'\Stitched'));
try
    stitchedDirectory=imageDatastore(dirStitched);
    numStitched=numel(stitchedDirectory.Files);
catch
    numStitched=0;
end
 
fileName=char(strcat('Stitched\','Stitched',num2str(numStitched+1),'.tif'))
imwrite(MyMontage.cdata,fileName,'tif');
title('Labels');