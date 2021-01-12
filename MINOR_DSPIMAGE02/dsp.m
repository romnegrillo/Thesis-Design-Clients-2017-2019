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

% Last Modified by GUIDE v2.5 07-Jan-2019 03:51:25

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


% --- Outputs from this function are returned to the command line.
function varargout = dsp_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;
initialize(handles)

function initialize(handles)

movegui(gcf,'center');

axes(handles.axes1);
cla reset;

axes(handles.axes2);
cla reset;

set(handles.axes1,'XTick',[]);
set(handles.axes1,'YTick',[]);
set(handles.axes2,'XTick',[]);
set(handles.axes2,'YTick',[]);

global imageInput;
imageInput=0;

% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global imageInput;
global imagePath;

[file,path]=uigetfile('*.jpg;*.png');

if ~isequal(file,0)
    imagePath=fullfile(path,file);
    axes(handles.axes1);
    imshow(imagePath);
    imageInput=1;
end

% --- Executes on button press in pushbutton2.
function pushbutton2_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global imageInput;
global imagePath;

if isequal(imageInput,1)
   outputImage=func_gray(imagePath);
   axes(handles.axes2);
   imshow(outputImage);
else
    msgbox("No valid image input found","Error");
end

% --- Executes on button press in pushbutton3.
function pushbutton3_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global imageInput;
global imagePath;

if isequal(imageInput,1)
   outputImage=func_opening(imagePath);
   axes(handles.axes2);
   imshow(outputImage);
else
    msgbox("No valid image input found","Error");
end

% --- Executes on button press in pushbutton4.
function pushbutton4_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global imageInput;
global imagePath;

if isequal(imageInput,1)
   outputImage=func_increase_contrast(imagePath);
   axes(handles.axes2);
   imshow(outputImage);
else
    msgbox("No valid image input found","Error");
end

% --- Executes on button press in pushbutton5.
function pushbutton5_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global imageInput;
global imagePath;

if isequal(imageInput,1)
   outputImage=func_decrease_contrast(imagePath);
   axes(handles.axes2);
   imshow(outputImage); 
else
    msgbox("No valid image input found","Error");
end

% --- Executes on button press in pushbutton6.
function pushbutton6_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton6 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global imageInput;
global imagePath;

if isequal(imageInput,1)
   outputImage=func_threshold(imagePath);
   axes(handles.axes2);
   imshow(outputImage);
else
    msgbox("No valid image input found","Error");
end

% --- Executes on button press in pushbutton7.
function pushbutton7_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton7 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global imageInput;
global imagePath;

if isequal(imageInput,1)
   outputImage=func_remove_background(imagePath);
   axes(handles.axes2);
   imshow(outputImage);
else
    msgbox("No valid image input found","Error");
end

% --- Executes on button press in inputCharButton.
function inputCharButton_Callback(hObject, eventdata, handles)
% hObject    handle to inputCharButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global imageInput;
global imagePath;

if isequal(imageInput,1)
   imageinfo(imagePath);
else
    msgbox("No valid image input found","Error");
end

% --- Executes on button press in outputCharButton.
function outputCharButton_Callback(hObject, eventdata, handles)
% hObject    handle to outputCharButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global imageInput;

if isequal(imageInput,1)
   
   isEmptyAxes = isempty(get(handles.axes2, 'Children'));
   
   if ~isEmptyAxes
       currentImage=getimage(handles.axes2);
       imwrite(currentImage,'currentview.jpg');
       imageinfo('currentview.jpg');
   else
       msgbox("No processed image found.");
   end
else
    msgbox("No valid image input found","Error");
end

% --- Executes on button press in saveOutputImageButton.
function saveOutputImageButton_Callback(hObject, eventdata, handles)
% hObject    handle to saveOutputImageButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global imageInput;

if isequal(imageInput,1)
    isEmptyAxes = isempty(get(handles.axes2, 'Children'));
    
    if ~isEmptyAxes
        [file,path]=uiputfile("./Saved Images/outputImage.jpg");
        
        if ~isequal(file,0)
            fullPath=fullfile(path,file);
            imwrite(getimage(handles.axes2),fullPath);

            msgbox("Image saved.");
        end
    else
        msgbox("No processed image found.");
    end
else
    msgbox("No valid image input found","Error");
end
