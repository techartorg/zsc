
"""
Conventions:

    * Python type hints reinforce expected types
    * Input with supplied defaults are Zbrush optionals. If the input is typed but specified with
        'None', it means no input is required
    * Most inputs are strings or numbers; here they are specified as str, float or int but in
      zbrush they are all ascii strings or 'numbers' unless specified
        * there's no unicode nonsense in zbrush, all strings are ascii or utf-8
    * references to memeory blocks use the MemBlock type hint
    * references to StrokeData use the StrokeData or MultipleStrokeData type hints

Not all functions in the zscript command list are represented directly as functions.  The ones that
are omitted are represented by other python constructs

"""
from typing import Optional, Any, NewType, Callable


class StrokeData:
    pass


class MultipleStrokeData:
    pass


class MemBlock:
    pass


def BackColorSet(Red: int, Green: int, Blue: int) -> None:
    """
    Sets the pen background color
    """


def ButtonFind(InterfaceItemPath: str, ButtonText: str, InitiallyDisabled: int = 0) -> str:
    """
    Locates a ZBrush interface item
    """
    pass


def ButtonPress(InterfaceItemPath: str, ButtonText: str, InitiallyDisabled: int = 0) -> None:
    """
    Locates and presses a ZBrush interface item
    """
    pass


def ButtonSet(InterfaceItemPath: str, Value: Any, ButtonName: str, InitiallyDisabled: int = 0) -> None:
    """
    Locates and sets a new value to a ZBrush interface item
    """
    pass


def ButtonUnPress(InterfaceItemPath: str, ButtonName: str = "", InitiallyDisabled: int = 0) -> None:
    """
    Locates and unpresses a ZBrush interface item
    """
    pass


def CanvasClick(*positions: int) -> None:
    """
    Emulates a click within the current canvas area
    Positions are passed 1 to 8  X, Y values, eg

        CanvasClick (128, 128, 256, 512)

    clicks at (x = 128, y= 128) and then (x=256, y=512)
    """
    pass


def CanvasGyroHide() -> None:
    """
    Hides the Transformation Gyro
    """
    pass


def CanvasGyroShow() -> None:
    """
    Shows the Transformation Gyro
    """
    pass


def CanvasPanGetH() -> int:
    """
    Returns the H pan value of the active document view

    Output: The current H Pan value.
    """
    pass


def CanvasPanGetV() -> int:
    """
    Returns the V pan value of the active document view

    Output: The current V Pan value.
    """
    pass


def CanvasPanSet(HValue: int, VValue: int) -> None:
    """
    Pans (Scrolls) the active document view
    """
    pass


def CanvasStroke(StrokeData: StrokeData, DelayedUpdate: float = 0, Rotation: float = 0, HScale: float = 0, VScale: float = 0, HOffset: int = 0, VOffset: int = 0, HRotateCenter: int = 0, VRotateCenter: int = 0) -> None:
    """
    Emulates a brush stroke within the current canvas area
    """
    pass


def CanvasStrokes(StrokeData: MultipleStrokeData, DelayedUpdate: float = 0, Rotation: float = 0, HScale: float = 0, VScale: float = 0, HOffset: int = 0, VOffset: int = 0, HRotateCenter: int = 0, VRotateCenter: int = 0) -> None:
    """
    Emulates multiple brush strokes within the current canvas area
    """
    pass


def CanvasZoomGet() -> float:
    """
    Returns the zoom value of the active document view

    Output: The current zoom value.
    """
    pass


def CanvasZoomSet(ZoomFactor: float) -> None:
    """
    Sets the zoom factor of the active document view
    """
    pass


def Caption(Text: str) -> None:
    """
    Displays a text line using the current Caption settings
    """
    pass


def CurveAddPoint(CurveIndex: int, XPos: int, YPos: int, ZPos: int) -> int:
    """
    Add a new point to the specified curve

    Output: Returns the point index (zero based) or -1 if failed.
    """
    pass


def CurvesCreateMesh(Name: str, Action: int = 0, Thickness: int = 0) -> int:
    """
    Creates a mesh from the current curves.

    Action values:

        0: Append mesh to the active mesh,  
        1: Add as a new subtool,  
        2: Export OBJ file if does not exists,  
        3: Export Obj file and overwrite if exsits,


    Output: Returns the number of points in the new mesh. zero=error, 1=file exists
    """
    pass


def CurvesDelete(CurveList: str) -> None:
    """
    Deletes named curves list.

    """
    pass


def CurvesNewCurve() -> int:
    """
    Creates a new curve in the current curves list.

    Output: Returns the curve index (zero based) or -1 if failed.
    """
    pass


def CurvesNew(Name: str) -> None:
    """
    Creates a new curves list.
    """
    pass


def CurvesToUI() -> int:
    """
    Copy the ZScript curves to UI

    Output: Returns zero of OK or -1 if failed.
    """
    pass


def Delay(DelaySeconds: float) -> None:
    """
    Delays execution of ZScript for specified amount of time
    """
    pass


def DispMapCreate(ImageWidth: int, ImageHeight: int, Smooth: int = 1, SubPoly: int = 0, Border: int = 8, UVTileIndex=0) -> int:
    """
    Creates DisplacementMap

    Output: Returns zero if executed successfully. Any other value indicates an error
    """
    pass


# todo: do we want to support this with a python construct directly?
# if so, what?
def Exit() -> None:
    """
    Aborts execution and exits the current ZScript
    """
    pass


def FileDelete(FileName: str) -> int:
    """
    Delete specific file.

    Output: Returns zero if command executed successfully.
    """
    pass


def FileExecute(FileName: str, MethodName: str, TextInputMem: MemBlock = None, Number: float = 0, InOutMem1: MemBlock = None, InOutMem2: MemBlock = None) -> int:
    """
    Executes the specified plugin file (DLL).

    Output: Returns the result value which was returned by the executed routine. Returns zero if error
    """
    pass


def FileExists(FileName: str) -> int:
    """
    Check if a specific file exists.

    Output: Returns 1 if file exists. Returns zero if does not exists
    """
    pass


def FileGetInfo(FileName: str, InfoIndex: int) -> float:
    """
    Retrieve information about a specified file.

    InfoIndex values:

        1: file size (in mb)
        2 -7: Creation date: year, month(1-12), day, hour, minutes, seconds
        8 -13: Modified date: year, month(1-12), day, hour, minutes, seconds
        14 -19: Access date: year, month(1-12), day, hour, minutes, seconds.


    Output: Returns the requested information or zero if file not found
    """
    pass


def FileNameAdvance(FileNameBase: str, NumDigits: int, AddCopyTag: int) -> str:
    """
    Increments the index value contained within a filename string . 
    if "AddCopyTag" is not zero, add "Copy" to the name.

    Output: Updated file Name
    """
    pass


def FileNameAsk(Extensions: str, DefaultName: str = None, DialogTitle: str = None) -> str:
    """
    Asks user for a file name
    If DefaultName is omitted, it's an Open dialog

    Output: Result file name or an empty string if user canceled operation
    """
    pass


def FileNameExtract(FileName: str, Component: int) -> str:
    """
    Extracts filename components. 

    Components:
        1: path
        2: name
        4: extension

    values can be OR'ed, s FileNameExtract('xxx', 7) gets the full path with name and extension

    Output: The extracted filename component/s.
    """
    pass
    # todo: should we use path.splitext, basename, etc?


def FileNameGetLastTyped() -> str:
    """
    Retrieves the latest file name that was typed by the user in a Save/Load action

    Output: Latest file name that was typed by the user. Returned Variable will be empty if the user has canceled the action.
    """
    pass


def FileNameGetLastUsed() -> str:
    """
    Retrieves the latest file name that was used (by the user or by ZBrush) in a Save/Load action

    Output: Latest file name that was used. Returned Variable will be empty if the user has canceled the action.
    """
    pass


def FileNameGetNext() -> str:
    """
    Get the preset file name that will be used in the next Save/Load action,  if it has been preset

    Output: File name that will be used in the next Save/Load action. Returned Variable will be empty if no next file name is preset.
    """
    pass


def FileNameHasNext() -> int:
    """
    Test if the preset file name that will be used in the next Save/Load action have been set or not

    Output: Returns 1 if next file name has been set,  0 otherwise.
    """
    pass


def FileNameMake(BaseFileName: str, Index: int, NumDigits: int) -> str:
    """
    Combines a base filename with an index number

    Output: Combined file name Variable
    """
    pass


def FileNameResolvePath(LocalFileName: str) -> str:
    """
    Resolves local path to full path

    Output: Full path.
    """
    pass


def FileNameSetNext(FileName: str, TemplatePath: str = None) -> None:
    """
    Pre-sets the file name that will be used in the next Save/Load action
    """
    pass


def FileTemplateGetNext():
    """
    Get the preset template file name that will be used in the next Save/Load action,  if it has been preset

    Output: Template file name that will be used in the next Save/Load action. Returned Variable will be empty if no next template file name is preset.
    """
    pass


def FontSetColor(Red: int, Green: int, Blue: int) -> None:
    """
    Sets the color of the text-flow font
    """
    pass


def FontSetOpacity(Opacity: float) -> None:
    """
    Sets the opacity of the text-flow font
    """
    pass


def FontSetSize(Size: int) -> None:
    """
    Sets the intensity of the text-flow font
    Values:
        1: Small
        2: Med
        3: Large
    """
    pass


def FontSetSizeLarge() -> None:
    """
    Sets the size of the text-flow font to large
    """
    pass


def FontSetSizeMedium() -> None:
    """
    Sets the size of the text-flow font to medium
    """
    pass


def FontSetSizeSmall() -> None:
    """
    Sets the size of the text-flow font to small
    """
    pass


def FrontColorSet(Description: str, Red: int, Green: int, Blue: int, Disabled: int = 0) -> None:
    """
    Sets the main interface color to a new value
    """
    pass


def GetActiveToolPath() -> str:
    """
    Returns the full path of the active tool

    Output: The path of the active tool
    """
    pass


# this is in the command text file but not the website... todo: is it supported?
'''def GetPolyMesh3DVolume():
    """
    Get the volume of current PolyMesh3D SubTool

    Output: Returns the Volume of current PolyMesh3D SubTool,  or 0 if not a PolyMesh3D. Note: if PolyMesh3D is NOT a valid volume,  then resulting value may be not accurate.

    """
    pass
'''


def HotKeyText(InterfacePath: str) -> None:
    """
    Displays a hot-key for the specified interface item
    """
    pass

#------------- interface


def IButton(ButtonText: str, PopupText: str = None, Commands: Callable = ..., Disabled: int = 0, Width: int = 0, Hotkey: str = '', Icon: str = '', Height: int = 0) -> None:
    """
    Creates an interactive push button
    """
    pass

# TODO: Pick up type annotations here


def IClick(InterfacePath: str, *positions) -> None:
    """
    Emulates a click within a specified ZBrush interface item

    """
    pass


def IClose(InterfacePath: str, ShowZoom: int = 0, TargetParent: int = 0):
    """
    Closes an interface item.

    """
    pass


def IColorSet(Red: int, Green: int, Blue: int):
    """
    Sets the active color to a new value

    """
    pass


def IConfig(Config):
    """
    Sets ZBrush internal version-configuration

    """
    pass


def IDialog(Title: str, TitleMode: int = 0, Icon: str = '', LeftInset: int = 0, RightInset: int = 0, LeftTop: int = 0, RightBottom: int = 0) -> int:
    """
    Adds a subpalette to ZBrush interface.
    Mode :
     mode? (0=Show Title and minimize button(ByDefault) 1=Show Title without minimize button 2=Hide Title )

    Icon:  Optional subpalette gray-scale (8-bits) icon (Standrad size of 20x20 pixels)


    Output: Returns 1 if subpalette added succesfuly. Returns 0 if subpalette could not be added or if it already exsists.

    """
    pass


def IDisable(WindowPath: str, WindowID: int) -> None:
    """
    Disables a ZScript interface item (can only be used for ZScript-generated interface items)

    """
    pass


def IEnable(WindowPath: str, WindowID: int) -> None:
    """
    Enables a ZScript interface item (can only be used for ZScript-generated interface items)

    """
    pass


def IExists(InterfaceItemPath: str) -> int:
    """
    Verifies that a specified interface item exists.

    Output: 1 if item exists, 0 otherwise

    """
    pass


def IFadeIn(FadeOutSpeed: float = 0.5) -> None:
    """
    Fades ZBrush window to black.

    """
    pass


def IFadeOut(FadeOutSpeed: float = 0.5) -> None:
    """
    Fades ZBrush window to black.

    """
    pass


def IFreeze(Commands: Callable = ..., FadeOutSpeed=0.05) -> None:
    """
    Disables interface updates.

    """
    pass


def IGet(InterfaceItemPath: str) -> object:
    """
    Returns the current value of a ZBrush or ZScript interface item

    Output: The item value

    """
    pass


def IGetFlags(InterfaceItemPath: str) -> int:
    """
    Returns the status flags of the specified interface item

    Output: The flags

    """
    pass


def IGetHotkey(InterfaceItemPath: str) -> str:
    """
    Returns the hotkey of the specified interface item

    Output: The Hotkey

    """
    pass


def IGetID(InterfaceItemPath: str) -> str:
    """
    Returns the window ID code of the specified interface item

    Output: The Title

    """
    pass


def IGetInfo(InterfaceItemPath: str) -> str:
    """
    Returns the info (popup info) of the specified interface item

    Output: The info

    """
    pass


def IGetMax(InterfaceItemPath: str) -> float:
    """
    Returns the maximum possible value of a ZBrush or ZScript interface item

    Output: The item maximum value

    """
    pass


def IGetMin(InterfaceItemPath: str) -> float:
    """
    Returns the minimum possible value of a ZBrush or ZScript interface item

    Output: The item minimum value

    """
    pass


def IGetSecondary(InterfaceItemPath: str) -> float:
    """
    Returns the the scondary value of a 2D interface item

    Output: The item value
    """
    pass


def IGetStatus(InterfaceItemPath: str) -> float:
    """
    Returns the Enabled/Disabled status of a ZBrush or ZScript interface item

    Output: The item status
        0=Disabled
        1=Enabled
    """
    pass


def IGetTitle(InterfaceItemPath: str, ReturnFullPath: int) -> str:
    """
    Returns the title of the specified interface item

    Output: The Title of the button

    """
    pass


def IHeight(InterfaceItemPath: str) -> int:
    """
    Returns the pixel-height of an interface item.

    Output: The height of the interface item.

    """
    pass


def IHide(InterfaceItemPath: str, ShowZoomRectangles: int = 0, TargetParentWindow: int = 0) -> None:
    """
    Hides an interface item.

    """
    pass


def IHPos(InterfaceItemPath: str, UseGlobalCoords: int = 0) -> int:
    """
    Returns the H position of the interface item in Canvas or Global coordinates.

    Output: The H position of the interface item.

    """
    pass


# how to annotate this?
def IKeyPress(KeyCode: str, Commands: Callable = ..., HCursor=None, VCursor=None):
    """
    Simulates a key press

    """
    pass


def ILock(WindowPath, WindowID):
    """
    Locks an interface item 

    """
    pass


def Image(FileName: str, Align: int, ResizedWidth: int) -> None:
    """
    Loads and displays an image
    Align (0=center 1=left 2=right
    """


def IMaximize(InterfaceItemPath: str, MaximizeSubPalettes: int) -> None:
    """
    Locates an interface item and (if possible) maximize its size.

    """
    pass


def IMinimize(InterfaceItemPath: str, MinimizeSubPalettes: int) -> None:
    """
    Locates an interface item and (if possible) minimize its size.

    """
    pass


def IModGet(InterfaceItemPath: str) -> int:
    """
    Returns the current modifiers binary state of a ZBrush or ZScript interface item

    Output: The item value

    """
    pass


def IModSet(InterfaceItemPath: str, value:int) ->None:
    """
    Sets the modifiers binary value of a ZBrush or a ZScript interface item

    """
    pass


def Interpolate(Time, Value1, Value2, Value3, Value4, AngleInterpolate=0):
    """
    Performs time-based interpolation

    Time: (0=AtStart 0.5=half 1=AtEnd)	
    Values are (Num,  VarName or ListName)


    Output: Interpolated value or list

    """
    pass


def IPress(InterfaceItemPath):
    """
    Presses a ZBrush or ZScript interface item

    """
    pass


def IReset(ItemToReset=0, ZBrushVersion=1.5):
    """
    Interface Reset
    ItemToReset = 0=All, 1=Interface, 2=Document, 3=Tools, 4=Lights, 5=Materials, 6=Stencil


    Output: Returns the button that the user clicked. ( 0=NO,  1=YES )

    """
    pass


def IsDisabled(InterfaceItemPath):
    """
    Returns 1 if the specified ZBrush or ZScript interface item is currently disabled,  returns 0 otherwise

    Output: The item 'Disabled' status (1=Disabled 0=Enabled)

    """
    pass


def IsEnabled(InterfaceItemPath):
    """
    Returns 1 if the specified ZBrush or ZScript interface item is currently enabled,  returns 0 otherwise

    Output: The item 'Enabled' status (1=Enabled 0=Disabled)

    """
    pass


def ISet(InterfaceItemPath, Value, SecondaryValue=None):
    """
    Sets a new value to a ZBrush or ZScript interface item

    """
    pass


def ISetHotkey(InterfaceItemPath, Hotkey):
    """
    Sets the hotkey of the specified interface item
    0 = no hotkey
    """
    pass


def ISetMax(InterfaceItemPath, MaxValue):
    """
    Sets the maximum value for an ISlider interface item (can only be used for ZScript-generated interface items)

    """


def ISetMin(InterfaceItemPath, MinValue):
    """
    Sets the minimum value for an ISlider interface item (can only be used for ZScript-generated interface items)

    """
    pass


def ISetStatus(InterfaceItemPath, Status):
    """
    Enables or Disables a ZScript interface item (can only be used for ZScript-generated interface items)
    New status ( 0=Disable NotZero=Enable )
    """
    pass


def IShowActions(ShowActions):
    """
    Temorarily sets the status of ShowActions
    . 0=Disable ShowActions,  Positive value=enable show actions Negative value=Reset ShowActions 

    """
    pass


def IShow(InterfaceItemPath, ShowZoomRectangles=0, TargetParenWindow=0):
    """
    Locates an interface item and makes it visible.

    """
    pass


def ISlider(SliderText, CurValue, Resolution, MinValue, MaxValue, PopupText, ChangeCommand, InitiallyDisabled=0, ButtonWidth=0):
    """
    Creates an interactive slider
    ButtonWidth:  in pixels (0=AutoWidth NonZero=Specified width)
    """
    pass


def IsLocked(InterfaceItemPath):
    """
    Returns 1 if the specified ZBrush or ZScript interface item is currently locked,  returns 0 otherwise

    Output: The item 'Locked' status (1=Locked 0=Unlocked)

    """


def IsPolyMesh3DSolid():
    """
    Tests if current PolyMesh3D is a Solid

    Output: Returns 1 if current PolyMesh3D is a valid Solid,  0 otherwise.

    """
    pass


def IStroke(InterfaceItemPath, StrokeData):
    """
    Emulates a brush stroke within an interface item

    """
    pass


def ISubPalette(PaletteName, TitleMode=0,  Icon=None, LeftInset=0, RightInset=0, LeftTop=0, RightBottom=0):
    """
    Adds a subpalette to ZBrush interface.

    TitleMode: ? (0=Show Title and minimize button(ByDefault) 1=Show Title without minimize button 2=Hide Title ),
    Icon  (8-bits) icon (Standrad size of 20x20 pixels)


    Output: Returns 1 if subpalette added succesfuly. Returns 0 if subpalette could not be added or if it already exsists.

    """
    pass


def IsUnlocked(InterfaceItemPath):
    """
    Returns 1 if the specified ZBrush or ZScript interface item is currently unlocked,  returns 0 otherwise

    Output: The item 'Unlocked' status (1=Unlocked 0=locked)

    """
    pass


def ISwitch(ButtonText, InitialState, PopupText, PressCommands: Callable = ..., UnpressedCommands: Callable = ..., InitiallyDisabled=0, ButtonWidth=0):
    """
    Creates an interactive switch
    InitialState (1=pressed, 0=unpressed),
    """
    pass


def IToggle(InterfaceItemPath):
    """
    Toggles the state of a ZBrush or ZScript interface item

    """
    pass


def IUnlock(WindowPath, WindowID):
    """
    Unlocks an interface item

    """
    pass


def IUnPress(InterfaceItemPath):
    """
    Unpresses a ZBrush or ZScript interface item
    """
    pass


def IUpdate(RepeatCount=1, Redraw=0):
    """
    Updates the ZBrush interface.
    """
    pass


def IVPos(InterfaceItemPath, UseGlobalCoords=0):
    """
    Returns the V position of the interface item in Canvas or Global coordinates.

    Output: The V position of the interface item.

    """
    pass


def IWidth(InterfaceItemPath):
    """
    Returns the pixel-width of an interface item.

    Output: The width of the interface item.

    """
    pass


def MemCopy(FromBlock, FromOffset, ToBlock, ToOffset, NumBytes=None) -> int:
    """
    Copies data from one memory block into another.
    if NumBytes is supplied, limit to that number of b

    Output: Returns the mumber of bytes moved. (-1 indicates an error)

    """
    pass


def MemCreate(BlockID, BlockSize, InitialFill=None) -> int:
    """
    Creates a new memory block.
    If InitialFill is supplied, fil with that value


    Output: Returns the size of the new memory block or error code...0=Error -1=Memory already exists -2=Can't create memory block.
    """
    pass


def MemCreateFromFile(BlockId, FileName, FileOffset=0, MaxBytes=None) -> int:
    """
    Creates a new memory block from a disk file.
    if FileOffset is supplied, read fron that byte
    if MaxBytes is supplied, read only that many bytes


    Output: Returns the size of the new memory block or error code...0=Error -1=Memory already exists -2=Can't create memory block -3=File not found.

    """
    pass


def MemDelete(BlockID) -> int:
    """
    Deletes a memory block.

    Output: Returns the size of the deleted memory block. Returns 0 if memory block could not be found.

    """
    pass


def MemGetSize(BlockID) -> int:
    """
    Returns the size of a memory block (Also useful for determining if a memory block already exists

    Output: Returns the size of the memory block. Returns 0 if data block could not be found.

    """
    pass


def MemMove(BlockID, FromOffset, ToOffset, NumBytes) -> int:
    """
    Move data within an existing memory block.

    Output: Returns the mumber of bytes moved.

    """
    pass


def MemMultiWrite(BlockID, Value, Format, Offset, RepeatCount, SubsequentOffset) -> int:
    """
    Write data to a memory block.
    Format: (0=omited=float,  1=signed char, 2=unsigned char, 3=signed short, 4=unsigned short, 5=signed long, 6=unsigned long, 7=fixed16 (16.16)

    Output: Returns the number of actual bytes written
    """
    pass


def MemRead(BlockID, ReadVariable, Format, Offset) -> int:
    """
    Reads data from a memory block.
    Data format (0=omited=float,  1=signed char, 2=unsigned char, 3=signed short, 4=unsigned short, 5=signed long, 6=unsigned long, 7=fixed16 (16.16)

    Output: Returns the number of actual bytes read

    """
    pass


def MemReadString(BlockID, StringVar, Offset, BreakAtLineEnd=0, SkipWhiteSpace=0, MaxReadLength=255) -> int:
    """
    Reads a string from a memory block.

    Output: Returns the number of bytes scanned. (may be larger than the actual bytes read)

    """
    pass


def MemResize(BlockID, NewSize, FillValue=None) -> int:
    """
    Resizes an exsiting memory block.
    if FillValue supplied, use it to fill newly allocated memory

    Output: Returns the new size of the memory block. Zero indicates an error.

    """
    pass


def MemSaveToFile(BlockID, FileName, OverwriteIfExists=0) -> int:
    """
    Saves an exisiting memory block to a disk file.
    Overwrite if exists? Set to nonzero value to save the file even if an identically named file already exists on disk. Default=Do not overwrite.

    Output: Returns the size of the new memory block or error code...0=Error -1=Memory does not exists -2=File already exits -3=File write error.

    """
    pass


def MemWrite(BlockID, Value, Format=0, Offset=0) -> int:
    """
    Write data to a memory block.
    Format (0=omited=float,  1=signed char, 2=unsigned char, 3=signed short, 4=unsigned short, 5=signed long, 6=unsigned long, 7=fixed16 (16.16)

    Output: Returns the number of actual bytes written

    """
    pass


def MemWriteString(BlockID, Value, Offset=0, WriteNullTerminator=1) -> int:
    """
    Writes a string into a memory block.

    Output: Returns the number of bytes written. (including the terminating zero)
    """
    pass


def MergeUndo():
    """
    Merge the next undo with the previous undo.

    """
    pass


def Mesh3DGet(Property, IndexInput,  OptionalInput, OptionalOutput1=None,  OptionalOutput2=None,  OptionalOutput3=None,  OptionalOutput4=None,  OptionalOutput5=None,  OptionalOutput6=None,  OptionalOutput7=None,  OptionalOutput8=None) -> int:
    """
    Gets information about the currently active  Mesh3D tool.
    Property: 0=PointsCount, 1=FacesCount, 2=XYZ bounds, 3=UVBounds, 4=1stUVTile, 5=NxtUVTile, 6=PolysInUVTile, 7=3DAreaOfUVTile, 8=Full3DMeshArea
    IndexInput:  Vertix/Face/Group/UVTile H index (0 based),
    OutputVariables will be filled based on chosen inputs

    Output: Returns zero if command executed successfully,  any other value indicates and error.

    """
    pass


def MessageOK(Message, Title):
    """
    Displays a user message with a single OK button

    """
    pass


def MessageOKCancel(Message, Title) -> int:
    """
    Displays a user message with CANCEL and OK buttons

    Output: Returns the button that the user clicked. (0=CANCEL,  1=OK)

    """
    pass


def MessageYesNo(Message, Title) -> int:
    """
    Displays a user message with YES and NO buttons

    Output: Returns the button that the user clicked. (0=NO,  1=YES)

    """
    pass


def MessageYesNoCancel(Message, Title) -> int:
    """
    Displays a user message with YES,  NO and CANCEL buttons

    Output: Returns the button that the user clicked. (0=NO,  1=YES CANCEL=-1)

    """
    pass


def MouseHPos(UseGlobalCoordinates=0) -> int:
    """
    Returns the current H position of the mouse in Canvas or Global coordinates.

    Output: The H position of the mouse

    """
    pass


def MouseLButton() -> int:
    """
    Returns the current state of the left mouse button 

    Output: Returns 1 if mouse button is pressed,  returns zero if unpressed

    """
    pass


def MouseVPos(UseGlobalCoordinates=0) -> int:
    """
    Returns the current V position of the mouse in Canvas or Global coordinates.

    Output: The V position of the mouse

    """
    pass


def MTransformGet(BlockID, VariableIndex=0):
    """
    Gets current transformation values into an existing memory block

    """
    pass


def MTransformSet(BlockID, VariableIndex=0):
    """
    Sets new transformation values from an existing memory block.

    """
    pass


def MVarDef(BlockID,  Count, InitialFill=0) -> int:
    """
    pass

    defines a new variables memory block.

    Output: Returns the variables count of the new memory block or error code...0=Error -1=Memory already exists -2=Can't create memory block.

    """
    pass


def MVarGet(BlockID, VariableIndex) -> float:
    """
    Reads a float value from a memory block.

    Output: Returns the float value.

    """
    pass


def MVarSet(BlockID, VariableIndex):
    """
    Writes a float value to a memory block.

    Output: Returns the old value of the variable.

    """
    pass


def NormalMapCreate(ImageWidth, ImageHeight, Smooth=1, SubPoly=0, Border=0, UVTile=None, UseTangentCoords=0) -> int:
    """
    Creates NormalMap

    Output: Returns zero if executed successfully. Any other value indicates an error

    """
    pass


def Note(Text, InterfaceItemPath=None, DisplayDuration=0, PopupBackgroundColor=0x606060, OffsetDistance=48, Width=400,  WindowFillColor=None, FrameHorizontalSize=1, FrameVerticalSize=1, FrameLeft=0,  FrameTop=0, IconFileName=None) -> int:
    """
    Displays a note to the user.

    BackgroundColor = x000000<->0xffffff,  default=0x606060,  0=NoBackground 

    FrameLeft ( 0=left (default) ,  .5=center,  1=right )
    FrameTop ( 0=top (default) ,  .5=center,  1=bottom )


    Output: If the note has UI buttons then the return value of the pressed buttons (1=1st button,  2=2nd button ...),  otherwise the return value will be zero.
    """
    pass


def NoteBar(Message=None, ProgressVarValue=0):
    """
    Displays a note in progress bar.

    """
    pass


def NoteIButton(ButtonText, ButtonIcon=None, InitiallyPressed=0, InitiallyDisabled=0, HRelativePos=0, VRelativePos=0, ButtonWidth=None, ButtonHeight=None, ButtonColor=0x000000,  TextColor=0xffffff, BGOpacity=1, TextOpacity=1, ImageOpacity=1):
    """
    pass

    defines a button to be included within the next Note to be shown.
    HRelativePos: (Positive value=offset from left,  Negative value=offset from right,  0=automatic),
    VRelativePos:  (Positive value=offset from top,  Negative value=offset from bottom,  0=automatic),
    colors :   0x000000<->0xffffff (blue + (green*256) + (red*65536) )
    """
    pass


def NoteIGet(NoteButtonIndexOrName) -> int:
    """
    Returns the value of am NoteIButton which was shown in the last displayed Note.

    Output: The item value

    """
    pass


def NoteISwitch(ButtonText, ButtonIcon=None, InitiallyPressed=0, InitiallyDisabled=0, HRelativePos=0, VRelativePos=0, ButtonWidth=None, ButtonHeight=None, ButtonColor=0x000000,  TextColor=0xffffff, BGOpacity=1, TextOpacity=1, ImageOpacity=1):
    """
    pass

    define a switch-button to be included within the next Note to be shown.

    """
    pass


def PageSetWidth(PageWidth):
    """
    Sets the width of the page

    """
    pass


def PaintBackground(Red, Green, Blue):
    """
    Paints the background using the current background color

    """
    pass


def PaintBackSliver(height, Red, Green, Blue):
    """
    Draws a full page-width rectangle using the current background color

    """
    pass


def PaintPageBreak():
    """
    Draws a visual page-break

    """
    pass


def PaintRect(Width, Height, Red, Green, Blue):
    """
    Draws a rectangle (in the ZScript window) using the current pen color

    """
    pass


def PaintTextRect(Width, Height, Text):
    """
    Draws a rectangle with imbedded text

    """
    pass


def PD():
    """
    Moves the pen position to the beginning of the next line (Same as PenMoveDown)

    """
    pass


def PenMoveCenter():
    """
    Moves the pen position to the horizontal center of the page

    """
    pass


def PenMoveDown():
    """
    Moves the pen position to the beginning of the next line

    """
    pass


def PenMoveLeft():
    """
    Moves the pen position to the left side of the page

    """
    pass


def PenMoveRight():
    """
    Moves the pen position to the right side of the page

    """
    pass


def PenMove(HOffset, VOffset):
    """
    Moves the pen a relative distance

    """
    pass


def PenSetColor(Red, Green, Blue):
    """
    Sets the pen main color

    """
    pass


def PixolPick(ComponentIndex, HPosition, VPosition) -> int:
    """
    Retrieves information about a specified Pixol
    componentIndex: 0=CompositeColor ( 0x000000<->0xffffff  or red*65536+green*256+blue) 1=Z(-32576 to 32576) 2=Red(0 to 255 ) 3=Green(0 to 255 ) 4=Blue(0 to 255 )  5=MaterialIndex(0 to 255 ) 6=XNormal(-1 to 1) 7=YNormal(-1 to 1) 8=ZNormal(-1 to 0) 


    Output: The value of the specified Pixol

    """
    pass


def PropertySet(CommandName, PropertyIndex, Value):
    """
    Modifies the setting of Title,  SubTitle and Caption text

    CommandName {Title, SubTitle, Caption}

    """
    pass


def Randomize(SeedValue):
    """
    Resets the Rand generator.
    SeedValue <= int16

    """
    pass


def RGB(Red, Green, Blue):
    """
    Combines 3 color-components into one RGB value

    Output: Combined RGB

    """
    pass

# def RoutineCall (Name of the routine to be called, Input Var01, Input Var02, Input Var03, Input Var04, Input Var05, Input Var06, Input Var07, Input Var08, Input Var09, Input Var10):
#     """
#     Executes the specified defined routine

#     """
#     pass

# def RoutineDef (Name of the routine, Commands group that will be executed when the routine is called, Input Var01, Input Var02, Input Var03, Input Var04, Input Var05, Input Var06, Input Var07, Input Var08, Input Var09, Input Var10):
#     """
#     pass

#     defines a named commands group

#     """
#     pass


def SectionBegin(SectionTitle, Expanded, PopupText, ExpandCommands, CollapsCommands, InitiallyDisabled=0):
    """
    Begins a collapsible section

    """
    pass


def SectionEnd():
    """
    Ends a collapsible section

    """
    pass


def ShellExecute(ShellCommand):
    """
    Execute a shell command

    """
    pass


def Sleep(Time, AwakenCommands,  EventType, OutEventCode, OutWindow):
    """
    Exists ZScript and be awaken by specified event.

    EventType:  (default=1) (1=Timer, 2=Mouse Moved, 4=LButton down, 8=LButton up, 16=KeyDown, 32=keyUp, 64=ModifierKeyDown, 128=ModifierKeyUp, 256=Startup, 512=Shut down, 1024 InterfaceItem pressed/unpressed, 2048 tool selected, 4096 texture selected,  8192 alpha sele

    """
    pass


def SleepAgain(Time, EventType):
    """
    Exists ZScript and continues the Sleep command.
    EventType:  (default=1) (1=Timer, 2=Mouse Moved, 4=LButton down, 8=LButton up, 16=KeyDown, 32=keyUp, 64=ModifierKeyDown, 128=ModifierKeyUp, 256=Startup, 512=Shut down, 1024 InterfaceItem pressed/unpressed, 2048 tool selected, 4096 texture selected,  8192 alpha sele

    """
    pass


def SoundPlay(BlockID, PlayMode) -> int:
    """
    Plays the sounds loaded into a specified memory block.
    PlayMode: . 0=default=Play once,  dont wait for completion. 1=Play once,  wait for completion. 2=Play loop,  dont wait for completion.):


    Output: Returns the zero if command executed successfully.

    """
    pass


def SoundStop(BlockId) -> int:
    """
    Stops the currently specified sound. 


    Output: Returns the zero if command executed successfully.

    """
    pass

#----- strings


def StrAsk(InitialString, Title="") -> str:
    """
    Asks user to input a string.

    Output: Returns the text typed by user or an empty string if canceled.

    """
    pass


def StrExtract(InputString, StartCharacterIndex, EndCharacterIndex) -> str:
    """
    Returns specified portion of the input string

    Output: The extracted portion of the input string.

    """
    pass


def StrFind(FindStr, InStr, StartIndex=0) -> int:
    """
    Locate a string within a string.

    Output: Returns the starting index of the 1st string within the 2nd string. returns -1 if not found.

    """
    pass


def StrFromAsc(CharacterNum) -> str:
    """
    Returns the character of the specified Ascii value.

    Output: The character of the specified Ascii value.

    """
    pass


def StrLength(InputStr) -> int:
    """
    Returns the number of characters in the input string.

    Output: Number of characters in the input string.

    """
    pass


def StrLower(InputString) -> str:
    """
    Returns the lowercase version of the input string.

    Output: The lowercase version of the input string.

    """
    pass


def StrMerge(Str1, Str2, Str3="", Str4="", Str5="", Str6="", Str7="", Str8="", Str9="", Str10="", Str11="", Str12="") -> str:
    """
    Combines two (or more) strings into one string.

    Output: The combined string. Note: result string will not exceed 255 characters in length 

    """
    pass


def StrToAsc(InputString, Offset=0) -> int:
    """
    Returns the Ascii value of a character.

    Output: The Ascii value of a character.

    """
    pass


def StrUpper(InputStr) -> str:
    """
    Returns the uppercase version of the input string.

    Output: The uppercase version of the input string.

    """
    pass


def StrokeGetInfo(StrokeVariable, InfoNumber, PointIndex) -> object:
    """
    Retrieves the information from a specified Stroke-type Variable

    Output: StrokeInfo result

    """
    pass

# stroke -------------


def StrokeGetLast() -> object:
    """
    Retrieves the last drawn brush stroke

    Output: StrokeData

    """
    pass


def StrokeLoad(FileName) -> object:
    """
    Loads a brush-stroke text file

    Output: StrokeData

    """
    pass


def StrokesLoad(FileName) -> object:
    """
    Loads a brush-strokes text file

    Output: StrokesData

    """
    pass


def SubTitle(Text):
    """
    Displays a text line using the current SubTitle settings

    """
    pass


def SubToolGetActiveIndex() -> int:
    """
    Returns the index of the active subtool

    Output: Returns the index of the active subtool (zero based).

    """
    pass


def SubToolGetCount() -> int:
    """
    Returns the number of subtools in the active tool

    Output: Returns the number of subtools.  Return 0 if error.

    """
    pass


def SubToolGetFolderIndex(SubtoolIndex) -> int:
    """
    Returns the folder index in which this subtool is contained
    If SubtoolIndex omited then use the currently selected tool.


    Output: Returns the foldr index or -1 if this subtool is not within a folder.


    """
    pass


def SubToolGetFolderName(SubtoolIndex) -> str:
    """
    Returns the ffolder name of the specified subtool
    If SubtoolIndex omited then use the currently selected tool.

    Output: Result folder name or empty if subtool is not in a folder.

    """
    pass


def SubToolGetID(SubtoolIndex) -> int:
    """
    Returns the unique subtool ID
    If SubtoolIndex omited then use the currently selected tool.

    Output: Returns the unique subtool ID or zero if error.

    """
    pass


def SubToolGetStatus(SubtoolIndex) -> int:
    """
    Returns the status of a subtool
    If SubtoolIndex omited then use the currently selected tool.

    Output: Returns the status (Subtool Eye=0x01,  Folder Eye=0x02, UnionAdd=0x10, UnionSub=0x20, UnionClip=0x40, UnionStart=0x80, ClosedFolder=0x400, OpenedFolder=0x800) .

    """
    pass


def SubToolLocate(SubtoolID) -> int:
    """
    Locates a subtool by the specified unique ID

    Output: Returns the index of the located subtool or -1 if error.

    """
    pass


def SubToolSelect(SubtoolIndex) -> int:
    """
    Selects the specified subtool index

    Output: Returns zero if OK,  -1 if error.

    """
    pass


def SubToolSetStatus(SubtoolIndex, Value) -> int:
    """
    Sets the status of a subtool
    If SubtoolIndex omited then use the currently selected tool.
    Value: (Subtool Eye=0x01, Folder Eye=0x02, UnionAdd=0x10, UnionSub=0x20, UnionClip=0x40, UnionStart=0x80, ClosedFolder=0x400, OpenedFolder=0x800)
    """
    pass


def TextCalcWidth(Text) -> int:
    """
    Calculates the pixel-width of the specified string

    Output: Width of text in pixels

    """
    pass


def Title(Text):
    """
    Displays a text line using the current Title settings

    """
    pass


def TLDeleteKeyFrame(KeyIndex) -> int:
    """
    Delete specified key frame index of the active track

    Output: Returns the number of available key frames

    """
    pass


def TLGetActiveTrackIndex() -> int:
    """
    Returns the index of the active track

    Output: Returns the current active track index -1=None 

    """
    pass


def TLGetKeyFramesCount() -> int:
    """
    Returns the total number of key frames in the active track

    Output: Returns the number of key frames in the active track 0=None 

    """
    pass


def TLGetKeyFrameTime(KeyIndex) -> int:
    """
    Get the time of the specified key frame index of the active track

    Output: Returns the time of the selected key frame or -1 if error.

    """
    pass


def TLGetTime() -> float:
    """
    Returns the current TimeLine knob position in  0.0 to 1.0 range

    Output: Returns the current TimeLine knob time 0=start,  1=end

    """
    pass


def TLGotoKeyFrameTime(KeyIndex) -> float:
    """
    Move TimeLine knob position to specified key frame index of the active track

    Output: Returns the time of the selected key frame or -1 if error.

    """
    pass


def TLGotoTime(Time) -> int:
    """
    Sets the current TimeLine knob position in  0.0 to 1.0 range

    Output: Returns zero if OK,  -1 if error.

    """
    pass


def TLNewKeyFrame(Time=None) -> int:
    """
    Create a new key frame in the active track
    if Time is omitted, use current time

    Output: Returns the new key frame index or -1 if error.

    """
    pass


def TLSetActiveTrackIndex(TrackIndex) -> int:
    """
    Sets the active track index

    Output: Returns zero if OK,  -1 if error.

    """
    pass


def TLSetKeyFrameTime(KeyIndex, Time) -> int:
    """
    Set the time of the specified key frame index of the active track
    Time is 0-1

    Output: Returns the new key frame index or -1 if error.

    """
    pass


def ToolGetActiveIndex() -> int:
    """
    Returns the index of the active tool

    Output: Returns the index of the active tool (zero based).

    """
    pass


def ToolGetCount() -> int:
    """
    Returns the number of available tools

    Output:  Returns the number of available tools.

    """
    pass


def ToolGetPath(ToolIndex: int = None) -> int:
    """
    Returns the file path or name of the specified tool
    If ToolIndex is omited then use the currently selected tool.

    Output: Result path (without the .ztl). Empty if error.

    """
    pass


def ToolGetSubToolID(ToolIndex: int = None, SubtoolIndex: int = None) -> int:
    """
    Returns the unique subtool ID
    If ToolIndex is omited then use the currently selected tool.
    If SubtoolIndex omited then use the selected subtool.):

    Output: Returns the unique subtool ID or zero if error.

    """
    pass


def ToolGetSubToolsCount(ToolIndex: int) -> int:
    """
    Returns the number of subtools in the specified tool index
    If ToolIndex is omited then use the currently selected tool.

    Output: Returns the number of subtools.  Return 0 if error.

    """
    pass


def ToolLocateSubTool(SubToolID: int, SubtoolIndex: int = None) -> int:
    """
    Locates a subtool by the specified unique ID

    Output: Returns the index of the located tool and subtool or -1 if error.
    """
    pass


def ToolSelect(SubToolIndex: int) -> int:
    """
    Selects the specified tool index

    Output: Returns zero if OK,  -1 if error.

    """
    pass


def ToolSetPath(SubToolIndex: int = None, NewPath: str = "") -> int:
    """
    Sets the file path or name of the specified tool
    If Tool Index  omited then use the currently selected tool.
    The new tool path ignores extensions

    Output: Returns zero if OK,  -1 if error.

    """
    pass


def TransformGet(xPos, yPos, zPos, xScale, yScale, zScale, xRotate, yRotate, zRotate):
    """
    Gets current transformation values.

    """
    pass


def TransformSet(xPos: float, yPos: float, zPos: float, xScale: float, yScale: float, zScale: float, xRotate: float, yRotate: float, zRotate: float):
    """
    Sets new transformation values.

    """
    pass


def TransposeGet(StarXPos: int, StartYPos: int, StartZPos: int, EndXPos: int, EndYPos: int, EndZPos: int, LineLength: int, RedAxisX: int, RedAxisY: int, RedAxisZ: int, GreenAxisX: int, GreenAxisY: int, GreenAxisZ: int, BlueAxisX: int, BlueAxisY: int, BlueAxisZ: int):
    """
    Gets current Transpose Action Line values.

    """
    pass


def TransposeIsShown():
    """
    Returns status of transpose line

    Output: Returns 1 if shown,  zero if not.

    """
    pass


def TransposeSet(StarXPos, StartYPos, StartZPos, EndXPos, EndYPos, EndZPos, LineLength, RedAxisX, RedAxisY, RedAxisZ, GreenAxisX, GreenAxisY, GreenAxisZ, BlueAxisX, BlueAxisY, BlueAxisZ):
    """
    Sets current Transpose Action Line values.

    """
    pass


# this is probably not needed?
def Val(Variable):
    """
    Evaluates the input and returns a numerical value

    Output: Value of the named variable

    """
    pass


# this is represented bu +=
# def VarAdd(Variable name, Value To Add):
#     """
#     Adds a value to an existing variable

#     """
#     pass


# def VarDec(Variable name):
#     """
#     Subtracts 1 from the value of an existing variable

#     """
#     pass


# def VarDef(Variable name, Variable defaultValue):
#     """
#     pass

#     defines a variable

#     """
#     pass


# def VarDiv(Variable name, Value to Divide By):
#     """
#     Divides an existing variable by a value

#     """
#     pass


# def VarInc(Variable name):
#     """
#     Adds 1 to the value of an existing variable

#     """
#     pass


# todo: handle this via slicing
def VarListCopy(DestinationList, DesitnationStart, SourceList, SourceStart, NumToCopy=0):
    """
    Copies items from a source list to a destination list

    """
    pass


def VarLoad(VariableName, FileName, VerifyOnly=0):
    """
    Loads variable/s from a file

    Output: Number of loaded or verfied values

    """
    pass


def VarSave(VariableName, FileName):
    """
    Saves variable value/s to file

    Output: Number of saved values

    """
    pass

# handled via  * 0r *=
# def VarMul(Variable name, Value to Multiply):
#         """
#     Multiplies an existing variable by a value

#     """


# handled implicitly
# def VarSet(Variable name, New Value):
#     """
#     Sets the value of a named variable

#     """
#             pass


# handled via len() for arrays (TODO: has to distinguish between strings and arrays!)
def VarSize(VariableName: str) -> int:
    """
    Returns the number of items in a variable or in a list

    Output: The number of items in a list or 1 if it is a simple variable

    """
    pass


# handled via - or -=
# def VarSub(Variable name, Value To Subtract):
#             """
#     Subtracts a value from an existing variable

#     """
#     pass


# handled.implicitly
# def Var(VariableName):
#     """
#     Gets the value of a named variable
#
#    Output: Value of the named variable
#     """
#     pass


def ZBrushInfo(InfoType: int) -> int:
    """
    Integer type code:

        0: version number
        1: Demo/Beta/Full
        2: Runtime seconds
        3: Mem use
        4: VMem Use
        5: Free Mem
        6: operating system(0: PC, 1: Mac, 2: MacOSX)
        7: Unique session ID
        8: Total RAM
        9: year
        10: mounth
        11: day
        12: hour
        13: minutes
        14: seconds
        15: Day Of The week
        16: cpu

    Output: Result value

    """


def ZBrushPriorityGet() -> int:
    """
    Returns the task-priority of ZBrush.

    Output: The current task-priority (-2 to 2)
    """
    pass


def ZBrushPrioritySet(Priority: int) -> int:
    """
    Sets the task-priority of ZBrush.
        -2: Low
        -1: BelowNormal
        0: normal
        1: Above Normal
        2: High

    """
    pass


def ZSphereAdd(xPos: float, yPos: float, zPos: float, Radius: float, ParentIndex: int = 0,  color=0x000000, Mask=0, TimeStamp=0, Flags=0) -> int:
    """
    Adds new ZSphere to the currently active ZSpheres tool

    Output: Returns the the index of the new ZSphere or -1 if command failed.

    """
    pass


def ZSphereDel(ZSphereIndex) -> int:
    """
    Deletes a ZSphere from the currently active ZSpheres tool

    Output: Returns zero if command executed successfully.
    """
    pass


def ZSphereEdit(ZSphereCommand, StoreUndo: int = 0) -> int:
    """
    Prepares the currently active ZSpheres tool for ZScript editing session.

    Output: Returns the zero if command executed successfully.

    if storeUndo != 0, add to the undo queue
    """
    pass


def ZSphereGet(Property, ZSphereIndex=None, SecondIndex=None):
    """
    Gets information about the currently active ZSpheres tool. (Must be placed within ZSphereEdit command)

    Propery values:

        0: ZSpheres count
        1: xPos
        2: yPos
        3: zPos
        4: radius
        5: color
        6: mask
        7: ParentIndex(-1: none)
        8: LastClickedIndex(-1: none)
        9: TimeStamp; 10: ChildsCount
        11: ChildIndex(2nd index)
        12: TimeStampCount
        13: TimeStampIndex
        14: flags
        15: Twist Angle
        16: Membrane
        16: Membrane
        17: X Res
        18: Y Res
        19: Z Res
        20: XYZ Res
        21: UserValue


    Output: Returns the value of the specified property

    """
    pass


def ZSphereSet(Property, ZSphereIndex: int = 0, NewValue: int = 0) -> None:
    """
    Sets property on the current ZSphere tool or tool at supplied index

    Propery values:

        0: ZSpheres count
        1: xPos
        2: yPos
        3: zPos
        4: radius
        5: color
        6: mask
        7: ParentIndex(-1: none)
        8: LastClickedIndex(-1: none)
        9: TimeStamp; 10: ChildsCount
        11: ChildIndex(2nd index)
        12: TimeStampCount
        13: TimeStampIndex
        14: flags
        15: Twist Angle
        16: Membrane
        16: Membrane
        17: X Res
        18: Y Res
        19: Z Res
        20: XYZ Res
        21: UserValue


    Output: Returns zero if command executed successfully.
    """
    pass

# there are handled implicitly ...
# Math Functions:
# SIN(angle)
# COS(angle)
# TAN(angle)
# ASIN(value)
# ACOS(value)
# ATAN(value)
# ATAN2(value, value)
# LOG(value)
# LOG10(value)
# SQRT(value)
# ABS(value)
# RAND(value)
# IRAND(value)
# BOOL(value)
# INT(value)
# FRAC(value)
# NEG(value)
# MIN(value1, value2)
# MAX(value1, value2)
