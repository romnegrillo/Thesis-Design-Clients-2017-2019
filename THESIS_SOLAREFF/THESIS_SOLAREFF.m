function varargout = THESIS_SOLAREFF(varargin)
% THESIS_SOLAREFF MATLAB code for THESIS_SOLAREFF.fig
%      THESIS_SOLAREFF, by itself, creates a new THESIS_SOLAREFF or raises the existing
%      singleton*.
%
%      H = THESIS_SOLAREFF returns the handle to a new THESIS_SOLAREFF or the handle to
%      the existing singleton*.
%
%      THESIS_SOLAREFF('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in THESIS_SOLAREFF.M with the given input arguments.
%
%      THESIS_SOLAREFF('Property','Value',...) creates a new THESIS_SOLAREFF or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before THESIS_SOLAREFF_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to THESIS_SOLAREFF_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help THESIS_SOLAREFF

% Last Modified by GUIDE v2.5 10-Jun-2019 23:39:34

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @THESIS_SOLAREFF_OpeningFcn, ...
                   'gui_OutputFcn',  @THESIS_SOLAREFF_OutputFcn, ...
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


% --- Executes just before THESIS_SOLAREFF is made visible.
function THESIS_SOLAREFF_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to THESIS_SOLAREFF (see VARARGIN)

% Choose default command line output for THESIS_SOLAREFF
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes THESIS_SOLAREFF wait for user response (see UIRESUME)
% uiwait(handles.figure1);
init(handles);

function init(handles)

global portPresent
global s;
global connected;

portPresent=false;
s="";
connected=false;

set(handles.serial_status,'String','Disconnected');
set(handles.serial_status,'ForegroundColor','red');
set(handles.connectButton,'enable','on');
set(handles.disconnectButton,'enable','off');
  
       
movegui(gcf,'center');
set(handles.axes1,'XTick',[]);
set(handles.axes1,'YTick',[]);

if ~isequal(size(seriallist,2),0)
    set(handles.portListCB,'String',seriallist)
    portPresent=true;
end

% --- Outputs from this function are returned to the command line.
function varargout = THESIS_SOLAREFF_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


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
            disp("One Serial");
            disp(items);
            s=serial(items);  
        else
            disp("Two or more Serial");
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
        axes1.YLim = [0 100];
        set(handles.axes1,'YTick',0:10:100);
        
        node1Eff = animatedline('Color','r');
        node2Eff = animatedline('Color','g');
        node3Eff = animatedline('Color', 'b');
        node4Eff = animatedline('Color','y');
        
        startTime = datetime('now'); 
        
        legend('Node 1','Node 2', 'Node 3', 'Node 4');
        
        drawnow;
        
        while connected
            try
                data=fgets(s);
                data=data(1:end-2);
                data=strsplit(data,",");
                disp(data);
                
                %disp(size(data,2));
                
                % node1,1,2,3 * 4 =16
                if size(data,2)==16
                    
                    node1_current=data(2);
                    node1_voltage=data(3);
                    node1_lux=data(4);
                    node1_power=str2double(node1_current)*10^-3*str2double(node1_voltage);
                    node1_eff=(node1_power/((str2double(node1_lux)*0.0079)*(0.0630)))*100;
                    
                    node2_current=data(6);
                    node2_voltage=data(7);
                    node2_lux=data(8);
                    node2_power=str2double(node2_current)*10^-3*str2double(node2_voltage);
                    node2_eff=(node2_power/((str2double(node2_lux)*0.0079)*(0.0630)))*100;
                    
                    node3_current=data(10);
                    node3_voltage=data(11);
                    node3_lux=data(12);
                    node3_power=str2double(node3_current)*10^-3*str2double(node3_voltage);
                    node3_eff=(node3_power/((str2double(node3_lux)*0.0079)*(0.0630)))*100;
                    
                    node4_current=data(14);
                    node4_voltage=data(15);
                    node4_lux=data(16);
                    node4_power=str2double(node4_current)*10^-3*str2double(node4_voltage);
                    node4_eff=(node4_power/((str2double(node4_lux)*0.0079)*(0.0630)))*100;
                    
                    disp("EFF");
                    disp(node1_eff);
                    disp(node2_eff);
                    disp(node3_eff);
                    disp(node4_eff);
                    
                    set(handles.node1_current,'String',strcat(node1_current,' mA'));
                    set(handles.node1_voltage,'String',strcat(node1_voltage, ' V'));
                    set(handles.node1_lux,'String',strcat(node1_lux, ' lux'));
                    set(handles.node1_power,'String',strcat(num2str(node1_power),' W'));
                    set(handles.node1_eff,'String',strcat(num2str(node1_eff), ' %'));
                    
                    set(handles.node2_current,'String',strcat(node2_current,' mA'));
                    set(handles.node2_voltage,'String',strcat(node2_voltage, ' V'));
                    set(handles.node2_lux,'String',strcat(node2_lux, ' lux'));
                    set(handles.node2_power,'String',strcat(num2str(node2_power),' W'));
                    set(handles.node2_eff,'String',strcat(num2str(node2_eff), ' %'));

                    set(handles.node3_current,'String',strcat(node3_current,' mA'));
                    set(handles.node3_voltage,'String',strcat(node3_voltage, ' V'));
                    set(handles.node3_lux,'String',strcat(node3_lux, ' lux'));
                    set(handles.node3_power,'String',strcat(num2str(node3_power),' W'));
                    set(handles.node3_eff,'String',strcat(num2str(node3_eff), ' %'));

                    set(handles.node4_current,'String',strcat(node4_current,' mA'));
                    set(handles.node4_voltage,'String',strcat(node4_voltage, ' V'));
                    set(handles.node4_lux,'String',strcat(node4_lux, ' lux'));
                    set(handles.node4_power,'String',strcat(num2str(node4_power),' W'));
                    set(handles.node4_eff,'String',strcat(num2str(node4_eff), ' %'));

                   
                    
                    disp("DEBUG");
           
                    t =  datetime('now') - startTime;
                    axes1.XLim = datenum([t-seconds(15) t]);
                    datetick('x','keeplimits')
         
                    
                    addpoints(node1Eff,datenum(t),(node1_eff));
                    addpoints(node2Eff,datenum(t),(node2_eff));
                    addpoints(node3Eff,datenum(t),(node3_eff));
                    addpoints(node4Eff,datenum(t),(node4_eff));
                    
                     drawnow;
                end
                
            catch ME
                disp(ME.identifier);
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



function node4_current_Callback(hObject, eventdata, handles)
% hObject    handle to node4_current (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of node4_current as text
%        str2double(get(hObject,'String')) returns contents of node4_current as a double


% --- Executes during object creation, after setting all properties.
function node4_current_CreateFcn(hObject, eventdata, handles)
% hObject    handle to node4_current (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function node4_voltage_Callback(hObject, eventdata, handles)
% hObject    handle to node4_voltage (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of node4_voltage as text
%        str2double(get(hObject,'String')) returns contents of node4_voltage as a double


% --- Executes during object creation, after setting all properties.
function node4_voltage_CreateFcn(hObject, eventdata, handles)
% hObject    handle to node4_voltage (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function node4_power_Callback(hObject, eventdata, handles)
% hObject    handle to node4_power (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of node4_power as text
%        str2double(get(hObject,'String')) returns contents of node4_power as a double


% --- Executes during object creation, after setting all properties.
function node4_power_CreateFcn(hObject, eventdata, handles)
% hObject    handle to node4_power (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function node4_lux_Callback(hObject, eventdata, handles)
% hObject    handle to node4_lux (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of node4_lux as text
%        str2double(get(hObject,'String')) returns contents of node4_lux as a double


% --- Executes during object creation, after setting all properties.
function node4_lux_CreateFcn(hObject, eventdata, handles)
% hObject    handle to node4_lux (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function node3_current_Callback(hObject, eventdata, handles)
% hObject    handle to node3_current (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of node3_current as text
%        str2double(get(hObject,'String')) returns contents of node3_current as a double


% --- Executes during object creation, after setting all properties.
function node3_current_CreateFcn(hObject, eventdata, handles)
% hObject    handle to node3_current (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function node3_voltage_Callback(hObject, eventdata, handles)
% hObject    handle to node3_voltage (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of node3_voltage as text
%        str2double(get(hObject,'String')) returns contents of node3_voltage as a double


% --- Executes during object creation, after setting all properties.
function node3_voltage_CreateFcn(hObject, eventdata, handles)
% hObject    handle to node3_voltage (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function node3_power_Callback(hObject, eventdata, handles)
% hObject    handle to node3_power (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of node3_power as text
%        str2double(get(hObject,'String')) returns contents of node3_power as a double


% --- Executes during object creation, after setting all properties.
function node3_power_CreateFcn(hObject, eventdata, handles)
% hObject    handle to node3_power (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function node3_lux_Callback(hObject, eventdata, handles)
% hObject    handle to node3_lux (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of node3_lux as text
%        str2double(get(hObject,'String')) returns contents of node3_lux as a double


% --- Executes during object creation, after setting all properties.
function node3_lux_CreateFcn(hObject, eventdata, handles)
% hObject    handle to node3_lux (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function node2_current_Callback(hObject, eventdata, handles)
% hObject    handle to node2_current (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of node2_current as text
%        str2double(get(hObject,'String')) returns contents of node2_current as a double


% --- Executes during object creation, after setting all properties.
function node2_current_CreateFcn(hObject, eventdata, handles)
% hObject    handle to node2_current (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function node2_voltage_Callback(hObject, eventdata, handles)
% hObject    handle to node2_voltage (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of node2_voltage as text
%        str2double(get(hObject,'String')) returns contents of node2_voltage as a double


% --- Executes during object creation, after setting all properties.
function node2_voltage_CreateFcn(hObject, eventdata, handles)
% hObject    handle to node2_voltage (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function node2_power_Callback(hObject, eventdata, handles)
% hObject    handle to node2_power (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of node2_power as text
%        str2double(get(hObject,'String')) returns contents of node2_power as a double


% --- Executes during object creation, after setting all properties.
function node2_power_CreateFcn(hObject, eventdata, handles)
% hObject    handle to node2_power (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function node2_lux_Callback(hObject, eventdata, handles)
% hObject    handle to node2_lux (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of node2_lux as text
%        str2double(get(hObject,'String')) returns contents of node2_lux as a double


% --- Executes during object creation, after setting all properties.
function node2_lux_CreateFcn(hObject, eventdata, handles)
% hObject    handle to node2_lux (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function node1_current_Callback(hObject, eventdata, handles)
% hObject    handle to node1_current (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of node1_current as text
%        str2double(get(hObject,'String')) returns contents of node1_current as a double


% --- Executes during object creation, after setting all properties.
function node1_current_CreateFcn(hObject, eventdata, handles)
% hObject    handle to node1_current (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function node1_voltage_Callback(hObject, eventdata, handles)
% hObject    handle to node1_voltage (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of node1_voltage as text
%        str2double(get(hObject,'String')) returns contents of node1_voltage as a double


% --- Executes during object creation, after setting all properties.
function node1_voltage_CreateFcn(hObject, eventdata, handles)
% hObject    handle to node1_voltage (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function node1_power_Callback(hObject, eventdata, handles)
% hObject    handle to node1_power (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of node1_power as text
%        str2double(get(hObject,'String')) returns contents of node1_power as a double


% --- Executes during object creation, after setting all properties.
function node1_power_CreateFcn(hObject, eventdata, handles)
% hObject    handle to node1_power (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function node1_lux_Callback(hObject, eventdata, handles)
% hObject    handle to node1_lux (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of node1_lux as text
%        str2double(get(hObject,'String')) returns contents of node1_lux as a double


% --- Executes during object creation, after setting all properties.
function node1_lux_CreateFcn(hObject, eventdata, handles)
% hObject    handle to node1_lux (see GCBO)
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



function node4_eff_Callback(hObject, eventdata, handles)
% hObject    handle to node4_eff (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of node4_eff as text
%        str2double(get(hObject,'String')) returns contents of node4_eff as a double


% --- Executes during object creation, after setting all properties.
function node4_eff_CreateFcn(hObject, eventdata, handles)
% hObject    handle to node4_eff (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function node3_eff_Callback(hObject, eventdata, handles)
% hObject    handle to node3_eff (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of node3_eff as text
%        str2double(get(hObject,'String')) returns contents of node3_eff as a double


% --- Executes during object creation, after setting all properties.
function node3_eff_CreateFcn(hObject, eventdata, handles)
% hObject    handle to node3_eff (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function node2_eff_Callback(hObject, eventdata, handles)
% hObject    handle to node2_eff (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of node2_eff as text
%        str2double(get(hObject,'String')) returns contents of node2_eff as a double


% --- Executes during object creation, after setting all properties.
function node2_eff_CreateFcn(hObject, eventdata, handles)
% hObject    handle to node2_eff (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function node1_eff_Callback(hObject, eventdata, handles)
% hObject    handle to node1_eff (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of node1_eff as text
%        str2double(get(hObject,'String')) returns contents of node1_eff as a double


% --- Executes during object creation, after setting all properties.
function node1_eff_CreateFcn(hObject, eventdata, handles)
% hObject    handle to node1_eff (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
