function varargout = suntracker(varargin)
% SUNTRACKER MATLAB code for suntracker.fig
%      SUNTRACKER, by itself, creates a new SUNTRACKER or raises the existing
%      singleton*.
%
%      H = SUNTRACKER returns the handle to a new SUNTRACKER or the handle to
%      the existing singleton*.
%
%      SUNTRACKER('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in SUNTRACKER.M with the given input arguments.
%
%      SUNTRACKER('Property','Value',...) creates a new SUNTRACKER or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before suntracker_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to suntracker_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help suntracker

% Last Modified by GUIDE v2.5 04-Mar-2019 03:01:23

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @suntracker_OpeningFcn, ...
                   'gui_OutputFcn',  @suntracker_OutputFcn, ...
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


% --- Executes just before suntracker is made visible.
function suntracker_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to suntracker (see VARARGIN)

% Choose default command line output for suntracker
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);
init(handles);

% UIWAIT makes suntracker wait for user response (see UIRESUME)
% uiwait(handles.figure1);

function init(handles)

global portPresent
global s;
global connected;

movegui(gcf, 'center');
set(handles.axes1,'XTick',[]);
set(handles.axes1,'YTick',[]);
set(handles.axes1,'YGrid','on');
set(handles.axes1,'YLim',[0 5]);
set(handles.axes1,'YTick',0:5);

portPresent=false;
s="";
connected=false;

if ~isequal(size(seriallist,2),0)
    set(handles.portListCB,'String',seriallist)
    portPresent=true;
end

set(handles.arduinoStatus,'String','Disconnected');
set(handles.arduinoStatus,'ForegroundColor','red');
set(handles.connectButton,'enable','on');
set(handles.disconnectButton,'enable','off');

% --- Outputs from this function are returned to the command line.
function varargout = suntracker_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


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

        if isequal(size(items,2),2)
            %disp(items{index});
            s=serial(items{index});  
        else
            %disp(items);
            s=serial(items);
        end
        
        fopen(s);
        set(s,'DataBits',8);
        set(s,'StopBits',1);
        set(s,'BaudRate', 9600);
        set(s,'Parity','none');
        set(s,'Timeout',5);
        
        connected=true;
        
        set(handles.arduinoStatus,'String','Connected');
        set(handles.arduinoStatus,'ForegroundColor','green');
        set(handles.connectButton,'enable','off');
        set(handles.disconnectButton,'enable','on');
    
        h = animatedline;
        axes1 = gca;
        startTime = datetime('now'); 
        
        leftLDRVoltageLine=animatedline('Color', 'r');
        rightLDRVoltageLine=animatedline('Color', 'g');
        
        drawnow;
        
        while connected
            try
                data=fgets(s);
                data = strsplit(data,',');
                
                disp(data);
                          
                leftLDRReadingV=str2double(data(1));
                rightLDRReadingV=str2double(data(2));
                
                %Data filtering.

                t =  datetime('now') - startTime;
                
                addpoints(leftLDRVoltageLine,datenum(t),leftLDRReadingV);
                addpoints(rightLDRVoltageLine,datenum(t),rightLDRReadingV);
                
                legend(handles.axes1,{'Time','Left LDR Voltage','Right LDR Voltage'});

                        
                axes1.XLim = datenum([t-seconds(15) t]);
                datetick('x','keeplimits')

            catch ME
                disp(ME.identifier);
                msgbox('An error has occured from reading serial device');
                fclose(s);
                init(handles);
            end
            
            drawnow;
        end
        
    else
        msgbox('No port selected');
    end
else
    msgbox('Already connected');
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


% --- Executes on button press in disconnectButton.
function disconnectButton_Callback(hObject, eventdata, handles)
% hObject    handle to disconnectButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global connected;
global s;

if connected
    fclose(s);
    init(handles);
end


% --- Executes when user attempts to close figure1.
function figure1_CloseRequestFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global s;
global connected;

if connected
    fclose(s);
    init(handles);
end


% Hint: delete(hObject) closes the figure
delete(hObject);
