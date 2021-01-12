function [width,height,class,type]=getImageProp(imageContainer)

h=imattributes(imageContainer);

width=h(1,2);
height=h(2,2);
class=h(3,2);
type=h(4,2);