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

% Last Modified by GUIDE v2.5 18-Apr-2019 17:12:34

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

global portPresent
global s;
global connected;

movegui(gcf,'center');

portPresent=false;
s="";
connected=false;

if ~isequal(size(seriallist,2),0)
    set(handles.portListCB,'String',seriallist)
    portPresent=true;
end

set(handles.axes1,'XTick',[]);
set(handles.axes1,'YTick',[]);
  axes1 = gca;
        axes1.YGrid = 'on';
        axes1.YLim = [0 1023];
        set(handles.axes1,'YTick',[0:100:1023]);
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
        index = get(handles.portListCB,'Value');
        items = get(handles.portListCB,'String');

        if isequal(size(index,2),1) 
            disp(items);
            s=serial(items);  
        else
            disp(items{index});
            s=serial(items{index});
        end
        
        fopen(s);
        set(s,'DataBits',8);
        set(s,'StopBits',1);
        set(s,'BaudRate', 9600);
        set(s,'Parity','none');
        set(s,'Timeout',10);
        
        connected=true;
        
        set(handles.serial_status,'String','Loading...');
        set(handles.serial_status,'ForegroundColor','green');
        set(handles.connectButton,'enable','off');
        set(handles.disconnectButton,'enable','on');
  
        axes1 = gca;
        axes1.YGrid = 'on';
        axes1.YLim = [0 1023];
        set(handles.axes1,'YTick',[0:100:1023]);
        tempLine = animatedline('Color','r');
        gasLine = animatedline('Color','g');
        startTime = datetime('now'); 
        
        legend('Temperature','Gas')
        drawnow;
        
        while connected
            try
                data=fgets(s);
                data=data(1:end-1);
                data=strsplit(data,",");
                 
                
                if size(data,1)~=0
                    
                    set(handles.serial_status,'String','Connected');
                
                set(handles.tempLabel,'String',data(2) + " - " + data(1) + " C");
                set(handles.smokeLabel,'String',data(4) + " - " + num2str(str2double(data(3))*(5.0)/(1023)) + " V");
                set(handles.fanLabel,'String',data(5));
                
                t =  datetime('now') - startTime;
                
                addpoints(tempLine,datenum(t),str2double(data(1)))
                addpoints(gasLine,datenum(t),str2double(data(3)));
                
                drawnow;
                
                axes1.XLim = datenum([t-seconds(15) t]);
                datetick('x','keeplimits')
                end
                
            catch ME
                %disp(ME.identifier);
                %msgbox('An error has occured from reading serial device');
                 
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

if connected
    connected=false;
    fclose(s);
    init(handles);

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



function smokeLabel_Callback(hObject, eventdata, handles)
% hObject    handle to text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of text as text
%        str2double(get(hObject,'String')) returns contents of text as a double


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



function tempLabel_Callback(hObject, eventdata, handles)
% hObject    handle to tempLabel (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of tempLabel as text
%        str2double(get(hObject,'String')) returns contents of tempLabel as a double


% --- Executes during object creation, after setting all properties.
function tempLabel_CreateFcn(hObject, eventdata, handles)
% hObject    handle to tempLabel (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function fanLabel_Callback(hObject, eventdata, handles)
% hObject    handle to fanLabel (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of fanLabel as text
%        str2double(get(hObject,'String')) returns contents of fanLabel as a double


% --- Executes during object creation, after setting all properties.
function fanLabel_CreateFcn(hObject, eventdata, handles)
% hObject    handle to fanLabel (see GCBO)
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
function smokeLabel_CreateFcn(hObject, eventdata, handles)
% hObject    handle to smokeLabel (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
