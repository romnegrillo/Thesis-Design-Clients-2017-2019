function varargout = DiffEquDesign(varargin)
% DIFFEQUDESIGN MATLAB code for DiffEquDesign.fig
%      DIFFEQUDESIGN, by itself, creates a new DIFFEQUDESIGN or raises the existing
%      singleton*.
%
%      H = DIFFEQUDESIGN returns the handle to a new DIFFEQUDESIGN or the handle to
%      the existing singleton*.
%
%      DIFFEQUDESIGN('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in DIFFEQUDESIGN.M with the given input arguments.
%
%      DIFFEQUDESIGN('Property','Value',...) creates a new DIFFEQUDESIGN or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before DiffEquDesign_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to DiffEquDesign_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help DiffEquDesign

% Last Modified by GUIDE v2.5 07-Mar-2018 22:20:34

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @DiffEquDesign_OpeningFcn, ...
                   'gui_OutputFcn',  @DiffEquDesign_OutputFcn, ...
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


% --- Executes just before DiffEquDesign is made visible.
function DiffEquDesign_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to DiffEquDesign (see VARARGIN)

% Choose default command line output for DiffEquDesign
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes DiffEquDesign wait for user response (see UIRESUME)
% uiwait(handles.figure1);
movegui(gcf,'center');
clear;
clc;
axes1=gca;  
cla(axes1);

% --- Outputs from this function are returned to the command line.
function varargout = DiffEquDesign_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on selection change in popupmenu1.
function popupmenu1_Callback(hObject, eventdata, handles)
% hObject    handle to popupmenu1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns popupmenu1 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from popupmenu1

switch get(hObject, 'Value')
    case 1
        set(handles.panel_logistic, 'Visible', 'on');
        set(handles.panel_mixture, 'Visible', 'off');
        set(handles.panel_cooling, 'Visible', 'off');
        set(handles.panel_escapeVelocity, 'Visible', 'off');
        set(handles.panel_eulers, 'Visible', 'off');
    case 2
        set(handles.panel_logistic, 'Visible', 'off');
        set(handles.panel_mixture, 'Visible', 'on');
        set(handles.panel_cooling, 'Visible', 'off');
        set(handles.panel_escapeVelocity, 'Visible', 'off');
        set(handles.panel_eulers, 'Visible', 'off');
    case 3
        set(handles.panel_logistic, 'Visible', 'off');
        set(handles.panel_mixture, 'Visible', 'off');
        set(handles.panel_cooling, 'Visible', 'on');
        set(handles.panel_escapeVelocity, 'Visible', 'off');
    case 4
        set(handles.panel_logistic, 'Visible', 'off');
        set(handles.panel_mixture, 'Visible', 'off');
        set(handles.panel_cooling, 'Visible', 'off');
        set(handles.panel_escapeVelocity, 'Visible', 'on');
        set(handles.panel_eulers, 'Visible', 'off');
    case 5
        set(handles.panel_logistic, 'Visible', 'off');
        set(handles.panel_mixture, 'Visible', 'off');
        set(handles.panel_cooling, 'Visible', 'off');
        set(handles.panel_escapeVelocity, 'Visible', 'off');
        set(handles.panel_eulers, 'Visible', 'on');
    otherwise
end

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



function logistic_yo_Callback(hObject, eventdata, handles)
% hObject    handle to logistic_yo (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of logistic_yo as text
%        str2double(get(hObject,'String')) returns contents of logistic_yo as a double


% --- Executes during object creation, after setting all properties.
function logistic_yo_CreateFcn(hObject, eventdata, handles)
% hObject    handle to logistic_yo (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function logistic_k_Callback(hObject, eventdata, handles)
% hObject    handle to logistic_k (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of logistic_k as text
%        str2double(get(hObject,'String')) returns contents of logistic_k as a double


% --- Executes during object creation, after setting all properties.
function logistic_k_CreateFcn(hObject, eventdata, handles)
% hObject    handle to logistic_k (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function logistic_r_Callback(hObject, eventdata, handles)
% hObject    handle to logistic_r (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of logistic_r as text
%        str2double(get(hObject,'String')) returns contents of logistic_r as a double


% --- Executes during object creation, after setting all properties.
function logistic_r_CreateFcn(hObject, eventdata, handles)
% hObject    handle to logistic_r (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function logistic_t_Callback(hObject, eventdata, handles)
% hObject    handle to logistic_t (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of logistic_t as text
%        str2double(get(hObject,'String')) returns contents of logistic_t as a double


% --- Executes during object creation, after setting all properties.
function logistic_t_CreateFcn(hObject, eventdata, handles)
% hObject    handle to logistic_t (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function logistic_yAns_Callback(hObject, eventdata, handles)
% hObject    handle to logistic_yAns (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of logistic_yAns as text
%        str2double(get(hObject,'String')) returns contents of logistic_yAns as a double


% --- Executes during object creation, after setting all properties.
function logistic_yAns_CreateFcn(hObject, eventdata, handles)
% hObject    handle to logistic_yAns (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in logistic_calculateButton.
function logistic_calculateButton_Callback(hObject, eventdata, handles)
% hObject    handle to logistic_calculateButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
logisticGrowth(handles);

function logisticGrowth(handles)

try
    
    yo=str2double(get(handles.logistic_yo, 'string'));
    k=str2double(get(handles.logistic_k, 'string'));
    r=str2double(get(handles.logistic_r, 'string'));
    time=str2double(get(handles.logistic_t, 'string'));

    [t, y] = ode45(@(t,y) r*y*(1-(y/k)), [0:1:time], yo);
    set(handles.logistic_yAns, 'string', y(time+1));

    axes1=gca;  
    cla(axes1);
    plot(t, y);
    xlabel('t');
    ylabel('y(t)');
catch
    h = msgbox({'Invalid input detected','Please try again.'},'Error');
end



