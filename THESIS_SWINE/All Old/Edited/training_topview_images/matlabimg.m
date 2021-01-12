img=imread('rgb_2019-01-22_21_33_45.076765.jpg');
hsv=rgb2hsv(img);

im=hsv;

minval=[0.0, 0.1, 0.35];
maxval=[0.1, 0.9, 1];

out = true(size(im,1), size(im,2));

for p = 1 : 3
    out = out & (im(:,:,p) >= minval(p) & im(:,:,p) <= maxval(p));
end

mask=zeros(size(img,1),size(img,2),1,'uint8');

for i=1:10
    nhood=[1 1 1;1 1 1; 1 1 1];
    out=imerode(out,nhood);
end

for i=1:10
    nhood=[1 1 1;1 1 1; 1 1 1];
    out=imdilate(out,nhood);
end

out=imfill(out,'holes');
 
subplot(1,2,1);
imshow(img);
subplot(1,2,2);
imshow(out);