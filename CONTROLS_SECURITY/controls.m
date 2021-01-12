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

% Last Modified by GUIDE v2.5 18-Jan-2019 10:46:17

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


global portPresent;
global s;
global connected;
portPresent=false;
s="";
connected=false;
movegui(gcf,'center');
set(handles.disconnectButton,'enable','off');

if ~isequal(size(seriallist,2),0)
    set(handles.popupmenu1,'String',seriallist)
    portPresent=true;
end

% --- Outputs from this function are returned to the command line.
function varargout = controls_OutputFcn(hObject, eventdata, handles) 
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
global fileID;

try
    if ~connected
        if portPresent
            disp("Connecting...");
            index = get(handles.popupmenu1,'Value');
            items = get(handles.popupmenu1,'String');

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
            set(s,'Timeout',2);

            disp("Connected.");
            connected=true;

            set(handles.connectButton,'enable','off');
            set(handles.disconnectButton,'enable','on');
            set(handles.arduinoStatus,'String','Connected');
            set(handles.arduinoStatus,'ForegroundColor','green');

            h = animatedline('Color','r');
            distanceAxes = gca;
            distanceAxes.YGrid = 'on';
            distanceAxes.YLim = [0 100];
 
            
            startTime = datetime('now'); 
            
            while connected

                data=fgets(s);
                disp(data);

                data = strsplit(data,',');
                motionIndicator=data(1);
                distance=str2double(data(2));
                
                disp(distance);
                
                if(distance<10)
                    set(handles.bar1,'BackgroundColor','red');
                    set(handles.bar2,'BackgroundColor','red');
                else
                    set(handles.bar1,'BackgroundColor','green');
                    set(handles.bar2,'BackgroundColor','green');
                end
                set(handles.distanceText,'String',strcat("Distance Reading:  ",num2str(distance),' cm'));
                t =  datetime('now') - startTime;
                addpoints(h,datenum(t),distance)

                drawnow;

                distanceAxes.XLim = datenum([t-seconds(15) t]);
                datetick('x','keeplimits')
        

                if strcmp(motionIndicator,"motion")
                    disp("motion detected")
                    set(handles.bar1,'BackgroundColor','red');
                    set(handles.bar2,'BackgroundColor','red');
                    set(handles.statusText,"String","Motion Detected");

                    c=clock;
    %                 disp(c(1));
    %                 disp(c(2));
    %                 disp(c(3));
    %                 disp(c(4));
    %                 disp(c(5));


                    datetime.setDefaultFormats('default','eeee, MMMM d, yyyy h:mm a')
                    set(handles.lastTimeText,'String',"Last Time: " + datestr(datetime))
                    fileID = fopen('logs.txt','a');
                    fprintf(fileID,'%s\n',"Last Time: " + datestr(datetime));
                    fclose(fileID);

                elseif strcmp(motionIndicator,"no motion")
                    disp("no motion detected")
                    set(handles.statusText,"String","No Motion Detected");
                    
                    if ~(distance<10)
                        set(handles.bar1,'BackgroundColor','green');
                        set(handles.bar2,'BackgroundColor','green');
                    end
                end

                drawnow;    
            end

        end
    end
catch
    
end
% --- Executes on selection change in popupmenu1.
function popupmenu1_Callback(hObject, eventdata, handles)
% hObject    handle to popupmenu1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns popupmenu1 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from popupmenu1


% --- Executes during object creation, after setting all properties.
function popupmenu1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to popupmenu1 (see GCBO)
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
global fileID;

if connected
    fclose(s);
    disp("Port disconnected.");
    set(handles.connectButton,'enable','on');
    set(handles.disconnectButton,'enable','off');
    set(handles.arduinoStatus,'String','Disconnected');
    set(handles.arduinoStatus,'ForegroundColor','red');
    connected=false;
end

% --- Executes when user attempts to close figure1.
function figure1_CloseRequestFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: delete(hObject) closes the figure

global connected;
global s;
global fileID;

if connected
    fclose(s);
    disp("Port disconnected.");
    set(handles.connectButton,'enable','on');
    set(handles.disconnectButton,'enable','off');
    set(handles.arduinoStatus,'String','Disconnected');
    set(handles.arduinoStatus,'ForegroundColor','red');
    connected=false;
end

delete(hObject);
