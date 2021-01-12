function varargout = controls(varargin)
% CONTROLS MATLAB code for controls.fig
%      CONTROLS, by itself, creates a new CONTROLS or raises the existing
%      singleton*.
%
%      H = CONTROLS returns the handle to a new CONTROLS or the handle to
%      the existing singleton*.
%
%      CONTROLS('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in CONTROLS.M with the given input arguments.
%
%      CONTROLS('Property','Value',...) creates a new CONTROLS or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before controls_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to controls_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help controls

% Last Modified by GUIDE v2.5 18-Apr-2019 17:21:12

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @controls_OpeningFcn, ...
                   'gui_OutputFcn',  @controls_OutputFcn, ...
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


% --- Executes just before controls is made visible.
function controls_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to controls (see VARARGIN)

% Choose default command line output for controls
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes controls wait for user response (see UIRESUME)
% uiwait(handles.figure1);
init(handles);

% --- Outputs from this function are returned to the command line.
function varargout = controls_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


function init(handles)

global portPresent; % For checking is there are available serial ports.
global s;           % Serial object.
global connected;   % For checking if we are connected already to port so we won't connect again.

movegui(gcf,'center');

portPresent=false;
s="";
connected=false;

% If the number of columns is not zero, port is present.
if ~isequal(size(seriallist,2),0)
    set(handles.portListCB,'String',seriallist)
    portPresent=true;
end

axes(handles.axes1);
cla;
set(handles.axes1,'XTick',[]);
set(handles.axes1,'YTick',[]);
set(handles.connectButton,'enable','on')
set(handles.disconnectButton,'enable','off')
set(handles.serial_status,'String','Disconnected');
set(handles.serial_status,'ForegroundColor','red');


% --- Executes on button press in connectButton.
function connectButton_Callback(hObject, eventdata, handles)
% hObject    handle to connectButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global portPresent;
global s;
global connected;

if ~connected
    if portPresent
        disp("Connecting...");
        index = get(handles.portListCB,'Value');    % Get current selected index.
        items = get(handles.portListCB,'String');   % Get all values in the combobox.

        % If the number of columns is one we will, items will return the
        % string of the portname. So index is just 1.
        if isequal(size(index,2),1) 
            disp(items);
            s=serial(items);  
        % Else, items will return a matrix of ports and we will use the
        % index to select that port. Index will return more than 1.
        else
            disp(items{index});
            s=serial(items{index});
        end
        
        % Open serial port with specified settings.
        fopen(s);
        set(s,'DataBits',8);
        set(s,'StopBits',1);
        set(s,'BaudRate', 9600);
        set(s,'Parity','none');
        set(s,'Timeout',5);
        
        % Finally set connected variable to true so we won't connect again.
        connected=true;
        
        set(handles.serial_status,'String','Connected');
        set(handles.serial_status,'ForegroundColor','green');
        set(handles.connectButton,'enable','off');
        set(handles.disconnectButton,'enable','on');
  
        % Get current axes.
        axes1 = gca;
        
        % Show y grid and set limit to 0-20.
        axes1.YGrid = 'on';
        axes1.YLim = [0 400];
        set(handles.axes1,'YTick',[0:50:400]);
        
        % Animated y axes lines that will move in the axes.
        containerALevel = animatedline('Color','r');
        containerBLevel = animatedline('Color','g');
        containerCLevel = animatedline('Color','b');
        
        % Animated x axes that will move in the axes.
        startTime = datetime('now'); 
        
        % Legends.
        legend('Container A','Container B', 'Container C');
        drawnow;
        
        while connected
            try
                data=fgets(s);
                data=data(1:end-1);
                data=strsplit(data,",");
                disp(data);
                
                if size(data,1)~=0

                    set(handles.containerALabel,'String',data(1));
                    set(handles.containerBLabel,'String',data(2));
                    set(handles.containerCLabel,'String',data(3));
                   
                    set(handles.pumpALabel,'String',data(4));
                    set(handles.pumpBLabel,'String',data(5));
                    set(handles.pumpCLabel,'String',data(6));
                    
                    t =  datetime('now') - startTime;

                    addpoints(containerALevel,datenum(t),str2double(data(1)))
                    addpoints(containerBLevel,datenum(t),str2double(data(2)));
                    addpoints(containerCLevel,datenum(t),str2double(data(3)));
                    
                    drawnow;

                    axes1.XLim = datenum([t-seconds(15) t]);
                    datetick('x','keeplimits')
                end
                
            catch ME
                %disp(ME.identifier);
                %msgbox('Serial port has been interrupted. Program is closing...');
                fclose(s);
            end
            
            drawnow;
        end
        
    else
        msgbox('No port selected');
    end
else
    msgbox('Already connected');
end

% --- Executes on button press in disconnectButton.
function disconnectButton_Callback(hObject, eventdata, handles)
% hObject    handle to disconnectButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global connected;
global s;   

try
    if connected
        connected=false;
        fclose(s);
        init(handles);
    end
catch
end

% --- Executes on selection change in portListCB.
function portListCB_Callback(hObject, eventdata, handles)
% hObject    handle to portListCB (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns portListCB contents as cell array
%        contents{get(hObject,'Value')} returns selected item from portListCB


% --- Executes during object creation, after setting all properties.
function portListCB_CreateFcn(hObject, eventdata, handles)
% hObject    handle to portListCB (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes during object creation, after setting all properties.
function text_CreateFcn(hObject, eventdata, handles)
% hObject    handle to text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function containerALabel_Callback(hObject, eventdata, handles)
% hObject    handle to containerALabel (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of containerALabel as text
%        str2double(get(hObject,'String')) returns contents of containerALabel as a double

% --- Executes during object creation, after setting all properties.
function containerALabel_CreateFcn(hObject, eventdata, handles)
% hObject    handle to containerALabel (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function containerCLabel_Callback(hObject, eventdata, handles)
% hObject    handle to containerCLabel (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of containerCLabel as text
%        str2double(get(hObject,'String')) returns contents of containerCLabel as a double

% --- Executes during object creation, after setting all properties.
function containerCLabel_CreateFcn(hObject, eventdata, handles)
% hObject    handle to containerCLabel (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

% --- Executes when user attempts to close figure1.
function figure1_CloseRequestFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global connected;
global s;   

try
    if connected
        connected=false;
        fclose(s);
    end
catch
end
% Hint: delete(hObject) closes the figure
delete(hObject);


% --- Executes during object creation, after setting all properties.
function containerBLabel_CreateFcn(hObject, eventdata, handles)
% hObject    handle to containerBLabel (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function pumpBLabel_Callback(hObject, eventdata, handles)
% hObject    handle to pumpBLabel (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of pumpBLabel as text
%        str2double(get(hObject,'String')) returns contents of pumpBLabel as a double


% --- Executes during object creation, after setting all properties.
function pumpBLabel_CreateFcn(hObject, eventdata, handles)
% hObject    handle to pumpBLabel (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function pumpALabel_Callback(hObject, eventdata, handles)
% hObject    handle to pumpALabel (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of pumpALabel as text
%        str2double(get(hObject,'String')) returns contents of pumpALabel as a double


% --- Executes during object creation, after setting all properties.
function pumpALabel_CreateFcn(hObject, eventdata, handles)
% hObject    handle to pumpALabel (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function pumpCLabel_Callback(hObject, eventdata, handles)
% hObject    handle to pumpCLabel (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of pumpCLabel as text
%        str2double(get(hObject,'String')) returns contents of pumpCLabel as a double


% --- Executes during object creation, after setting all properties.
function pumpCLabel_CreateFcn(hObject, eventdata, handles)
% hObject    handle to pumpCLabel (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
