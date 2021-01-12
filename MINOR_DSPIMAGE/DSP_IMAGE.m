function varargout = DSP_IMAGE(varargin)
% DSP_IMAGE MATLAB code for DSP_IMAGE.fig
%      DSP_IMAGE, by itself, creates a new DSP_IMAGE or raises the existing
%      singleton*.
%
%      H = DSP_IMAGE returns the handle to a new DSP_IMAGE or the handle to
%      the existing singleton*.
%
%      DSP_IMAGE('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in DSP_IMAGE.M with the given input arguments.
%
%      DSP_IMAGE('Property','Value',...) creates a new DSP_IMAGE or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before DSP_IMAGE_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to DSP_IMAGE_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help DSP_IMAGE

% Last Modified by GUIDE v2.5 05-Apr-2019 04:24:39

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @DSP_IMAGE_OpeningFcn, ...
                   'gui_OutputFcn',  @DSP_IMAGE_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before DSP_IMAGE is made visible.
function DSP_IMAGE_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to DSP_IMAGE (see VARARGIN)

% Choose default command line output for DSP_IMAGE
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes DSP_IMAGE wait for user response (see UIRESUME)
% uiwait(handles.figure1);
init(handles);

% --- Outputs from this function are returned to the command line.
function varargout = DSP_IMAGE_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;

function init(handles)

global imagePath;
imagePath='';

movegui(gcf,'center');

set(handles.axes1,'XTick',[]);
set(handles.axes1,'YTick',[]);
set(handles.axes2,'XTick',[]);
set(handles.axes2,'YTick',[]);

set(handles.redSlider, 'Min', 0);
set(handles.redSlider, 'Max', 255);
set(handles.redSlider, 'Value', 0); 
set(handles.redLabel, 'String', 'Red: 0'); 

set(handles.greenSlider, 'Min', 0);
set(handles.greenSlider, 'Max', 255);
set(handles.greenSlider, 'Value', 0); 
set(handles.greenLabel, 'String', 'Green: 0'); 

set(handles.blueSlider, 'Min', 0);
set(handles.blueSlider, 'Max', 255);
set(handles.blueSlider, 'Value', 0); 
set(handles.blueLabel, 'String', 'Blue: 0'); 
 


% --- Executes on button press in selectImageButton.
function selectImageButton_Callback(hObject, eventdata, handles)
% hObject    handle to selectImageButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global imagePath;

imagePath=getImagePath();

if ~isequal(imagePath,0)
   img=imread(imagePath);
   init(handles);
   axes(handles.axes1);
   imshow(img);
else
    init(handles);
end

% --- Executes on button press in grayscaleButton.
function grayscaleButton_Callback(hObject, eventdata, handles)
% hObject    handle to grayscaleButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

img=getimage(handles.axes1);
gray=imageProcessing(img,1);

axes(handles.axes2);
imshow(gray);


% --- Executes on button press in openingButton.
function openingButton_Callback(hObject, eventdata, handles)
% hObject    handle to openingButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
img=getimage(handles.axes1);
opening=imageProcessing(img,2);

axes(handles.axes2);
imshow(opening);

% --- Executes on button press in increaseContrastButton.
function increaseContrastButton_Callback(hObject, eventdata, handles)
% hObject    handle to increaseContrastButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
img=getimage(handles.axes1);
increaseContrast=imageProcessing(img,3);

axes(handles.axes2);
imshow(increaseContrast);

% --- Executes on button press in decreaseContrastButton.
function decreaseContrastButton_Callback(hObject, eventdata, handles)
% hObject    handle to decreaseContrastButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
img=getimage(handles.axes1);
decreasedContrast=imageProcessing(img,4);

axes(handles.axes2);
imshow(decreasedContrast);

% --- Executes on button press in thresholdButton.
function thresholdButton_Callback(hObject, eventdata, handles)
% hObject    handle to thresholdButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
img=getimage(handles.axes1);
mask=imageProcessing(img,5);

axes(handles.axes2);
imshow(mask);

% --- Executes on button press in removeBackgroundButton.
function removeBackgroundButton_Callback(hObject, eventdata, handles)
% hObject    handle to removeBackgroundButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
img=getimage(handles.axes1);
masked=imageProcessing(img,6);

axes(handles.axes2);
imshow(masked);


% --- Executes on button press in viewCharImage1Button.
function viewCharImage1Button_Callback(hObject, eventdata, handles)
% hObject    handle to viewCharImage1Button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global imagePath;

if size(imagePath,1)~=0
	disp('debug');
    imageinfo(imagePath);  
end


% --- Executes on button press in viewCharImage2Button.
function viewCharImage2Button_Callback(hObject, eventdata, handles)
% hObject    handle to viewCharImage2Button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global imagePath;

if size(imagePath,1)~=0
    img=getimage(handles.axes2);
    imwrite(img,'./Temporary Images/temp.jpg');
    imageinfo('./Temporary Images/temp.jpg');  
end

% --- Executes on button press in saveOutputImageButton.
function saveOutputImageButton_Callback(hObject, eventdata, handles)
% hObject    handle to saveOutputImageButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global imagePath;

if (size(imagePath,1)~=0)
    img=getimage(handles.axes2);
    saveImage('output.jpg',img);
    msgbox("Output image saved!");
end


% --- Executes on slider movement.
function redSlider_Callback(hObject, eventdata, handles)
% hObject    handle to redSlider (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
val=get(handles.redSlider,'Value');
set(handles.redLabel, 'String', strcat('Red: ',num2str(round(val)))); 
img=getimage(handles.axes1);

if size(img,3)==3
   img(:,:,1)=val;
   axes(handles.axes2);
   imshow(img);
end

% --- Executes during object creation, after setting all properties.
function redSlider_CreateFcn(hObject, eventdata, handles)
% hObject    handle to redSlider (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on slider movement.
function greenSlider_Callback(hObject, eventdata, handles)
% hObject    handle to greenSlider (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
val=get(handles.greenSlider,'Value');
set(handles.greenLabel, 'String', strcat('Green: ',num2str(round(val)))); 
img=getimage(handles.axes1);

if size(img,3)==3
   img(:,:,2)=val;
   axes(handles.axes2);
   imshow(img);
end

% --- Executes during object creation, after setting all properties.
function greenSlider_CreateFcn(hObject, eventdata, handles)
% hObject    handle to greenSlider (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on slider movement.
function blueSlider_Callback(hObject, eventdata, handles)
% hObject    handle to blueSlider (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
val=get(handles.blueSlider,'Value');
set(handles.blueLabel, 'String', strcat('Blue: ',num2str(round(val)))); 
img=getimage(handles.axes1);

if size(img,3)==3
   img(:,:,3)=val;
   axes(handles.axes2);
   imshow(img);
end

% --- Executes during object creation, after setting all properties.
function blueSlider_CreateFcn(hObject, eventdata, handles)
% hObject    handle to blueSlider (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end
