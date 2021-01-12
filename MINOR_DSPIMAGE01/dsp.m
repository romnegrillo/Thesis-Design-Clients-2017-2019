function varargout = dsp(varargin)
% DSP MATLAB code for dsp.fig
%      DSP, by itself, creates a new DSP or raises the existing
%      singleton*.
%
%      H = DSP returns the handle to a new DSP or the handle to
%      the existing singleton*.
%
%      DSP('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in DSP.M with the given input arguments.
%
%      DSP('Property','Value',...) creates a new DSP or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before dsp_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to dsp_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help dsp

% Last Modified by GUIDE v2.5 25-Sep-2018 03:19:06

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @dsp_OpeningFcn, ...
                   'gui_OutputFcn',  @dsp_OutputFcn, ...
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


% --- Executes just before dsp is made visible.
function dsp_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to dsp (see VARARGIN)

% Choose default command line output for dsp
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes dsp wait for user response (see UIRESUME)
% uiwait(handles.figure1);
global imagePath;
imagePath=0;
global processedImage;
processedImage=0;
global currentView;
currentView=1;

reset(handles);


% --- Outputs from this function are returned to the command line.
function varargout = dsp_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in openImageButton.
function openImageButton_Callback(hObject, eventdata, handles)
% hObject    handle to openImageButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global imagePath;
global processedImage;
global prevPath;

imagePath=getImagePath();
%disp(imageName);

if ~isequal(imagePath,0)
    prevPath=imagePath;
    processedImage=0;
    axes(handles.axes2);
    cla reset;
    axes(handles.axes1);
    h=imshow(imagePath);
    [width,height,class,type]=getImageProp(h);

    row1Display="Input Image";
    row2Display=strcat("(Width, Height): ","(",width,", ",height,")");
    row3Display=strcat("Datatype: ",class, " | Image Type: ", type);
    
    set(handles.inputImgProp,'String',[row1Display,row2Display,row3Display]);
else
    %imagePath=prevPath;
    reset(handles);
end

% --- Executes on button press in processImageButton.
function processImageButton_Callback(hObject, eventdata, handles)
% hObject    handle to processImageButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global imagePath;
global processedImage;
global currentView;
global outputType;
outputType="Masked Image";

if ~isequal(imagePath,0)     
        currentView=1;
        axes(handles.axes2);
        processedImage=imageProcessing(imagePath,currentView);
    
        h=imshow(processedImage);
        [width,height,class,type]=getImageProp(h);

        row1Display=outputType;
        row2Display=strcat("(Width, Height): ","(",width,", ",height,")");
        row3Display=strcat("Datatype: ",class, " | Image Type: ", type);

        set(handles.outputImgProp,'String',[row1Display,row2Display,row3Display]);
else
    msgbox("No image selected!","Error");
end

% --- Executes on button press in saveImageButton.
function saveImageButton_Callback(hObject, eventdata, handles)
% hObject    handle to saveImageButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global imagePath;
global processedImage;

if ~isequal(imagePath,0) && ~isequal(processedImage,0)
    saveImage('ProcessedImage.jpg',processedImage);
else
    msgbox("No image to save!","Error");
end


% --- Executes on button press in clearButton.
function clearButton_Callback(hObject, eventdata, handles)
% hObject    handle to clearButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
reset(handles);


function reset(handles)

global imagePath;
imagePath=0;

global processedImage;
processedImage=0;

global currentView;
currentView=1;

global outputType;
outputType="Background Subtracted Image";

axes(handles.axes1);
cla reset;
set(gca,'Box','On');
axes(handles.axes2);
cla reset;
set(gca,'Box','On');
set(handles.inputImgProp,'String',"");
set(handles.outputImgProp,'String',"");

% --- Executes on button press in changeViewButton.
function changeViewButton_Callback(hObject, eventdata, handles)
% hObject    handle to changeViewButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global imagePath;
global processedImage;
global currentView;
global outputType;

if ~isequal(imagePath,0) 
    if ~isequal(processedImage,0)
        
        updateCurrentView()
        axes(handles.axes2);
        processedImage=imageProcessing(imagePath,currentView);
        h=imshow(processedImage);
        [width,height,class,type]=getImageProp(h);

        row1Display=outputType;
        row2Display=strcat("(Width, Height): ","(",width,", ",height,")");
        row3Display=strcat("Datatype: ",class, " | Image Type: ", type);

        set(handles.outputImgProp,'String',[row1Display,row2Display,row3Display]);
        
    else
        msgbox("No processed image yet!","Error");
    end
else
    msgbox("No image selected!","Error");
end

function updateCurrentView()

global currentView;
global outputType;

if(currentView>=6)
    currentView=1;
else
    currentView=currentView+1;
end

if(currentView==1)
    outputType="Masked Image";
elseif(currentView==2)
    outputType="Grayscale Image";
elseif(currentView==3)
    outputType="Filtered Grayscale Image";
elseif(currentView==4)
    outputType="Morphologicaly Opened Image";
elseif(currentView==5)
    outputType="Binary Image";
elseif(currentView==6)
    outputType="Contrast Adjusted Grayscale Image";
end
