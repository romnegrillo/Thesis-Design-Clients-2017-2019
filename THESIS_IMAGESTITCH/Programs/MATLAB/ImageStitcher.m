function varargout = ImageStitcher(varargin)
% IMAGESTITCHER MATLAB code for ImageStitcher.fig
%      IMAGESTITCHER, by itself, creates a new IMAGESTITCHER or raises the existing
%      singleton*.
%
%      H = IMAGESTITCHER returns the handle to a new IMAGESTITCHER or the handle to
%      the existing singleton*.
%
%      IMAGESTITCHER('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in IMAGESTITCHER.M with the given input arguments.
%
%      IMAGESTITCHER('Property','Value',...) creates a new IMAGESTITCHER or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before ImageStitcher_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to ImageStitcher_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help ImageStitcher

% Last Modified by GUIDE v2.5 24-Jul-2018 23:40:23

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @ImageStitcher_OpeningFcn, ...
                   'gui_OutputFcn',  @ImageStitcher_OutputFcn, ...
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


% --- Executes just before ImageStitcher is made visible.
function ImageStitcher_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to ImageStitcher (see VARARGIN)

% Choose default command line output for ImageStitcher
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes ImageStitcher wait for user response (see UIRESUME)
% uiwait(handles.figure1);
movegui(handles.figure1,'center');
set(handles.axes1, 'XTick',[]);
set(handles.axes1, 'YTick',[]);

set(handles.pushbutton1,'Enable','on');
set(handles.pushbutton2,'Enable','off');
set(handles.pushbutton3,'Enable','off');
set(handles.pushbutton4,'Enable','off');

set(handles.slider1,'Value',339);
set(handles.slider2,'Value',164);

global connectClicked; 
global previewClicked;
global captureClicked;
global stitchClicked;
global stop;

connectClicked=false;
previewClicked=false;
captureClicked=false;
stitchClicked=false;
stop=false;

% --- Outputs from this function are returned to the command line.
function varargout = ImageStitcher_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB

global connectClicked; 
global previewClicked;
global captureClicked;
global stitchClicked;
global stop;

global xValue;
global yValue;
xValue=339;
yValue=164;

clear rpi;
connectedToRPi=false;
set(handles.pushbutton1,'Enable','off');
set(handles.text3,'String','Connecting...','ForegroundColor',[0, 0, 1]);
drawnow;

try
    
    rpi=raspi('192.168.137.10','pi','raspberry');
    set(handles.text3,'String','Raspberry Pi Connected','ForegroundColor',[0, 1, 0]);
    
    connectClicked=true;
    previewClicked=false;
    captureClicked=false;
    stitchClicked=false;
    
    set(handles.pushbutton1,'Enable','off');
    set(handles.pushbutton2,'Enable','on');
    set(handles.pushbutton3,'Enable','off');
    set(handles.pushbutton4,'Enable','off');
    
    connectedToRPi=true;
catch
    set(handles.text3,'String','Raspberry Pi Disconnected','ForegroundColor',[1, 0, 0]);
    set(handles.pushbutton1,'Enable','on');
    msgbox('Cannot connect to Raspberry Pi!','Error');
end

% When the connection is successful, 
% connect to the camera.
connectedToCamera=false;

if connectedToRPi
    try
        cam = cameraboard(rpi, 'Resolution', '1280x720');
        connectedToCamera=true;
    catch
        msgbox('Cannot connect to Camera Board!','Error');
    end
end

if connectedToCamera
    axes(handles.axes1);
    
    try
        
    while ~stop
        
        % Occurs only when preview button is clicked.
        if previewClicked
            img = snapshot(cam);
           
            R = mean2(img(:, :, 1));
            G = mean2(img(:, :, 2));
            B = mean2(img(:, :, 3));
            
            %disp(R);
            %disp(G);
            %disp(B);
            
            if R>G & R>B
                set(handles.text2, 'String', 'RED');
            elseif G>R & G>B
                set(handles.text2,'String', 'GREEN');
            else
                set(handles.text2, 'String', 'BLUE');
            end

            drawn=insertShape(img,'rectangle',[xValue yValue 495 440],'LineWidth',5);
            drawn=insertText(drawn, [10 10], 'ROI', 'FontSize', 50);
            imshow(drawn);
      
        end

        % Occurs only when capture button is clicked.
        if captureClicked & ~stop
            folderName='MicroscopeImages/'
            prefixName='image';
            suffixName=1;
                for i=1:120
                    
                    for shot=1:5
                        img = snapshot(cam);
                    end
                    
                    img_crop=imcrop(img, [xValue yValue 495 440]);
                    fname=strcat(folderName,prefixName,num2str(suffixName),'.jpg');
                    suffixName=suffixName+1;
                    imwrite(img_crop, fname);
                    
                    R = mean2(img(:, :, 1));
                    G = mean2(img(:, :, 2));
                    B = mean2(img(:, :, 3));

                    if R>G & R>B
                        set(handles.text2, 'String', 'RED');
                    elseif G>R & G>B
                        set(handles.text2,'String', 'GREEN');
                    else
                        set(handles.text2, 'String', 'BLUE');
                    end

                    imshow(img, 'Parent',handles.axes1);
                    drawnow;
                    
                    system(rpi, 'python3 /home/pi/Desktop/Programs/XLeft.py');

                    if mod(i,20) == 0     

                        drawn=insertText(img, [10 10], 'Going left...', 'FontSize', 50);
                        imshow(drawn, 'Parent',handles.axes1);
                        drawnow;
                        
                        for j=1:20
                            system(rpi, 'python3 /home/pi/Desktop/Programs/XRight.py');
                        end
                         
                        system(rpi, 'python3 /home/pi/Desktop/Programs/YDown.py');
                        pause(1);
                    end
                end
             
             system(rpi, 'python3 /home/pi/Desktop/Programs/YUp.py');
             img=img*0;
             drawn=insertText(img, [10 10], 'Ready to stitch.', 'FontSize', 50);
             imshow(drawn, 'Parent',handles.axes1);
             captureEnd(handles)
        end

        % Occurs only when stitch button is clicked.
        if stitchClicked
            % Performing stitching on the function.
            % This block won't be excecute since the
            % function called will reset the button clicked
            % and the state of the button widgets.
            disp("DEBUG");
        end

         drawnow;
    end
    
    catch
        clear;
        clc;
    end
end

% --- Executes on button press in pushbutton2.
function pushbutton2_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global connectClicked; 
global previewClicked;
global captureClicked;
global stitchClicked;

connectClicked=false;
previewClicked=true;
captureClicked=false;
stitchClicked=false;

set(handles.pushbutton1,'Enable','off');
set(handles.pushbutton2,'Enable','off');
set(handles.pushbutton3,'Enable','on');
set(handles.pushbutton4,'Enable','off');


% --- Executes on button press in pushbutton3.
function pushbutton3_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global connectClicked; 
global previewClicked;
global captureClicked;
global stitchClicked;

connectClicked=false;
previewClicked=false;
captureClicked=true;
stitchClicked=false;

set(handles.pushbutton1,'Enable','off');
set(handles.pushbutton2,'Enable','off');
set(handles.pushbutton3,'Enable','off');
set(handles.pushbutton4,'Enable','off');


% --- Executes on button press in pushbutton4.
function pushbutton4_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global connectClicked; 
global previewClicked;
global captureClicked;
global stitchClicked;

connectClicked=false;
previewClicked=false;
captureClicked=false;
stitchClicked=true;

set(handles.pushbutton1,'Enable','on');
set(handles.pushbutton2,'Enable','off');
set(handles.pushbutton3,'Enable','off');
set(handles.pushbutton4,'Enable','off');

if stitchClicked
    disp("Performing stitching...");
    stitchImage();
end

defaultGlobalValues(handles)

function captureEnd(handles)

global connectClicked; 
global previewClicked;
global captureClicked;
global stitchClicked;

connectClicked=false;
previewClicked=false;
captureClicked=false;
stitchClicked=false;

set(handles.pushbutton1,'Enable','off');
set(handles.pushbutton2,'Enable','off');
set(handles.pushbutton3,'Enable','off');
set(handles.pushbutton4,'Enable','on');

function defaultGlobalValues(handles)

global connectClicked; 
global previewClicked;
global captureClicked;
global stitchClicked;

connectClicked=false;
previewClicked=false;
captureClicked=false;
stitchClicked=false;

set(handles.pushbutton1,'Enable','off');
set(handles.pushbutton2,'Enable','on');
set(handles.pushbutton3,'Enable','off');
set(handles.pushbutton4,'Enable','off');

% --- Executes when user attempts to close figure1.
function figure1_CloseRequestFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: delete(hObject) closes the figure
delete(hObject);
global stop;
stop=true;

function stitchImage()

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
img=imread(fileName);
R = mean2(img(:, :, 1));
G = mean2(img(:, :, 2));
B = mean2(img(:, :, 3));

if R>G & R>B
    titleAxes='RED DOMINANT';
elseif G>R & G>B
    titleAxes='GREEN DOMINANT';
else
    titleAxes='BLUE DOMINANT';
end
figure;
imshow(img);                    
title(titleAxes);

% --- Executes on slider movement.
function slider1_Callback(hObject, eventdata, handles)
% hObject    handle to slider1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
global xValue;
xValue = get(handles.slider1, 'Value');
disp(xValue);

% --- Executes during object creation, after setting all properties.
function slider1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to slider1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on slider movement.
function slider2_Callback(hObject, eventdata, handles)
% hObject    handle to slider2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
global yValue;
yValue = get(handles.slider2, 'Value');
disp(yValue);

% --- Executes during object creation, after setting all properties.
function slider2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to slider2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on button press in pushbutton6.
function pushbutton6_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton6 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
delete(handles.figure1);
global stop;
stop=true;
