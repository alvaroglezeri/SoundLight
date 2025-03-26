# Sweetlight Project structure

The structure for a Sweetlight project is the following:

```text
Project
├── 3DView
│   ├── 3dview.ini
│   └── fixtures.ini
├── Editor
│   ├── 2DView
│   │   ├── 2dview.ini
│   │   ├── background.jpg
│   │   └── fixtures.ini
│   ├── editor.ini
│   ├── Generator
│   │   ├── curves
│   │   │   ├── default.gcv
│   │   │   ├── pulse.gcv
│   │   │   ├── sin.gcv
│   │   │   ├── sin_6point.gcv
│   │   │   ├── sin_6pointrev.gcv
│   │   │   └── triangle.gcv
│   │   └── curves_rgbcmy
│   │       └── default.gcv
│   └── groups.ini
├── fixtures
│   └── <fixture>.txt
├── fixtures.ini
├── fixtures_backup.ini
├── Live
│   ├── live.ini
│   └── TimeLine
│       ├── timeline.ini
│       └── timelines
│           └── <timeline>.tml
├── scenes
│   └── <scene>.scex
├── ScreenControl
│   └── screencontrol.ini
├── StandAlone
│   └── standalone.ini
└── thelightingcontroller.ini
```

The project is divided into several levels:

## `fixtures.ini`

INI file that contains a list of fixtures. Each fixture's structure is:

```ini
[FixtureX]                  # Fixture ID: f.e., 'Fixture1'
address = 1                 # Starting address in patch. For universes > 1, 
                            # add 512 to the real address, f.e., 513 for 
                            # address 1 in U2
name = 150wLEDBeamMover     # Display name of the fixture
model = 150wLEDBeamMover    # Fixture model. Must exist in 'fixtures' folder
quantity = 1                # Number of physical fixtures. Normally 1
group = a                   # Group shortcut. For more than one group, 
                            # concatenate shortcuts, f.e.:'ab'
id = 1742819250             # Unique ID

# Offset values for pan/tilt/zoom. Normally 0
offset_pan = 0              
offset_tilt = 0
zoom_pan = 0
zoom_tilt = 0
```

## `thelightincontroller.ini`

INI file that configures the program and contains metadata. Optional.

## 3DView

Folder containing info about the 3D real-time viewer.

### 3DView > `3dview.ini`

INI file with the configuration for the 3D Viewer:

```ini
[3D]                    # 3D Rendering configuration (Optional)
FPS = 60                # Max FPS for the viewer 1~60. (D=10)
TopMost = 1             # Show window always on top. (D=0)
Beam = 2                # Beam resolution 0(Low) ~ 2(High). (D=0)
Beam_Lenght = 16        # Beam length 10~40. Adjusted based on the stage model. (D=10)
Beam_Opacity = 4        # Beam intensity 0~10 (D=4)
RenderMode = 4          # Render mode for lights (D=3)
                        # 0: Points
                        # 1: Lines
                        # 2: Flat
                        # 3: Gouraud
                        # 4: Phong
OpenGLCompatibility = 1 # Compat with OpenGL
Realistic_Beam = 1      # Realistic beam rendering. (D=1)
Gobos = 1               # Render gobos (D=1)
AutoRotation = 1        # Auto rotation enabled (D=0)
ARTimeOut = 15          # Timeout for auto rotation (D=600)

[Textures]              # Rendering box texture config (Optional)
# Each wall has its number: 0-Ground, 1-Front, 2-Back, 3-Left, 4-Right, 5-Roof
Wall0 = 1,metal2.png,10.0,10.0
# Params (in order, separated with comma):
# Enabled/disabled (D=0)
# Texture image name. Can be custom. (D=<empty>)
# X-scale. Float. (D=1)
# Y-scale. Float. (D=1)

[Scene]                     # Rendering box config (Optional)
Size = 40.00,10.00,20.00    # Size (Width, Height, Depth) in _Unit_ (D=20,10,20)
Unit = meter                # Measure unit 'feet'/'meter' (D=meter)
Ambient_Light = 0           # Room brightness 0~10 (D=0)
```

### 3DView > `fixtures.ini`

INI file with the configuration for the fixtures in the 3D Viewer:

```ini
[1742819250]                # Fixture's Unique ID
Name = 150wLEDBeamMover     # Fixture's display name for the list
Position = -8.00,8.00,-2.00 # Coordinates (X,Y,X)
Orientation = 0,90,0        # Orientation (Xº,Yº,Zº) (D=0,0,0)
Scale = 1,1,1               # Scale (X,Y,Z) (D=1,1,1)
Color = 125,125,125         # Color (R,G,B) (D=125,125,125)
Object = big_led_wash(12u)  # (O) Shape/Model. 
                            # Must exist in SweetLight/3DViewer/fixtures/ as an .obj file.
```

### 3DView > `other.ini`

INI file with the configuration for the objects in the 3D Viewer:

```ini
[mirror_ball_1]             # Object's Unique ID
Object = disco/mirror_ball  # Shape/Model. Idem to fixtures.ini
Position = 0,0,0            # Coordinates (X,Y,Z)
Orientation = 0,0,0         # Orientation (Xº,Yº,Zº) (D=0,0,0)
Scale = 1,1,1               # Scale (X,Y,Z) (D=1,1,1)
Color = 125,125,125         # Color (R,G,B) (D=125,125,125)
```

## Editor

The editor folder contains all relevant files for the Editor tab in the software. 

### Editor > `editor.ini`

INI file with the configuration for the Editor window(s). Optional.

### Editor > `groups.ini`

INI file with the group definitions:

```ini
[Groups]
a = Name1       # Group key and name
b = Name2
...
Z = Name52      # Up to 52 groups, one per letter (lower/upper). 
                # Numbers 0-9 'can' be used, but not recommended.

[NotUsedInLC]   # (O)
a = 0           # Specifies if the group can be used in the Lightshow Creator. (D=0)
b = 1
```

### Editor > 2DView

Folder that configurates the 2D view of the stage. Optionally, can contain a `background.jpg` image for the background.

#### Editor > 2DView > `2dview.ini`

INI file that configurates the params for the 2D View. Optional:

```ini
[Params]
ShowGrid = 1            # Shows or hides the grid. (D=0)
SnapToGrid = 1          # Enables grid snapping. (D=0)
ImagesSize = 1          # Image and grid size 0~2. (D=0)
LockFixtures = 0        # Disables moving the fixtures. (D=0)
ShowHiddenFixtures = 1  # Shows or hides hidden fixtures. (D=0)
```

#### Editor > 2DView > `fixtures.ini`

INI file that configurates the position of the fixtures in the 2D View. For each fixture:

```ini
[Name]              # Display name of the fixture
Position = 100,100  # Coordinates (X<1000,Y<750). Zero in top-left.
```

### Editor > Generator

TODO

## fixtures

Folder containing the definition files for each fixture type. For each fixture, a personality file named `<modelName>.txt` must exist like this:

```ini
# Parameters for the View menu in Edit Fixture:
ViewType = VIEW_TYPE_HEAD           # Name of .png file in `2dview_fixtures_pictures` with the 2D icon. (???)
ViewPower = VIEW_POWER_LAMP700W     # Wattage of the fixture (30, 60, 250, 575, 700, 1200)
ViewAnglePan = 540                  # Max pan rangeº. Min = 10
ViewAngleTilt = 270                 # Max tilt rangeº. Min = 10
ViewAngleBeam = 2                   # Beam aperture (1~180)º
ViewReversePan = FALSE              # Reverses pan
ViewReverseTilt = FALSE             # Reverses tilt
ViewReverseDimmer = FALSE           # Reverses dimmer
ViewReverseIris = FALSE             # Reverses iris
ViewColor = 16777215                # Color of the beam. Format ARGB/RGBA.
2DViewImage =                       # Name of .png file in `2dview_fixtures_pictures` with the 2D icon.

# Channel definitions:
# Normal channels
Channel = pan                       

Channel = upan

Channel = tilt

Channel = utilt

Channel = pantilt_speed

Channel = dimmer

# Channel with preset ranges: <name>,<range_low>,<range_high>
Channel = shutter                   
 open,0,15 strobe,16,95 pulse_strobe,96,175 random_strobe,176,249 open,250,255 

Channel = prism_rotate
 stop,0,0 index,1,127 right_rotate,128,191 left_rotate,192,255 

Channel = focus

Channel = effect_macro
 no_function,0,79 pattern_01,80,255 
```

## Live

Folder containing info about the Live tab.

### Live > `live.ini`

INI file containing the general configuration of the whole tab:

```ini
[live]                      # General config for all Live tabs
manual_bpm = 123            # Set BPM
master_faders = 1           # Number of master faders present
no_button_overlay = yes     # 
dmx_on = no
fade_time = 300
[Params]
ActiveTab = 1
MMFilesPath = C:\Users\Álvaro\Desktop\
[master_faders]
type_fader0 = 1
caption_fader0 = [LC] - Master Dimmer
v8_master_fader0 = 1742819251,dimmer|1742819255,dimmer|1742819250,dimmer|1742819254,dimmer|1742819253,dimmer|1742819257,dimmer|1742819252,dimmer|1742819256,dimmer|
live_mobile_fader0 = 1
type_fader1 = 1
caption_fader1 = [LC] - Master Speed
v8_master_fader1 = 
live_mobile_fader1 = 1
[display]
trigger_keyboard = yes
trigger_calendar = yes
trigger_midi = yes
trigger_dmx = yes
speed_info = yes
[page]
number = 5
[page1]
name = Page_1
nb_buttons = 0
[page2]
name = [LC] - PC_ALL - pantilt
swap = yes
nb_buttons = 0
[page3]
name = [LC] - PC_ALL - colors
swap = yes
sequential = yes
nb_buttons = 0
[page4]
name = [LC] - PC_ALL - gobos
swap = yes
nb_buttons = 0
[page5]
name = [LC] - PC_ALL - channels
nb_buttons = 1
[page5_button1]
line = 1
column = 1
name = lightshow_creator/PC_ALL/channel - par_can_yellow.scex
title = par_can_yellow - PC_ALL
masterspeedfader = 0
fader = yes
preset_step = 255
[board]
number = 1
[board1]
screen = 0
page = 1
[screen0]
window = no

```

## Pixels
asdf

## scenes
asdf

## ScreenControl
asdf

## StandAlone
asdf



