# `RACKS` section in .dvc files

When generating scenes, Daslight follows this structure under the hood:

```xml
<SCENE attribs...>
    <FIXTUREDATAS>...
    <RACKS>...
</SCENE>

```

The element `FIXTUREDATAS` contains the relevant fixtures' DASUID and DATA (parameter containing information that is yet to be deciphered).

The element `RACKS` on the other hand, is somewhat clearer. For basic scenes, the element can be omitted, as the DATA contains enough information. However, for more complex features, more complex scene types might be better suited.

## Relevant values

### Time parameters

When parameters mention _time_, instead of duration, it uses a **stepping of 40ms**. So, 25 steps is equal to 1000ms, or 1 second.

### `RACK.TYPE`

| Value | Meaning |
| --- | --- |
| 1 | ? |
| 2 | Color FX |
| 3 | Chaser FX |
| 4 | ? |
| 5 | ? |
| 6 | ? |
| 7 | ? |
| 8 | ? |
| 9 | Steps |

### `EFFECT.TYPE`

| Value | Meaning |
| --- | --- |
| 1 | ? |
| 2 | ? |
| 3 | ? |
| 4 | ? |
| 5 | ? |
| 6 | ? |
| 7 | ? |
| 8 | ? |
| 9 | ? |

### `PARAM.TYPE`

| Value | Meaning |
| --- | --- |
| 0 | Int slider |
| 1 | ? |
| 2 | Boolean toggle |
| 3 | ? |
| 4 | Color picker |
| 5 | ? |
| 6 | Dropdown list |
| 7 | ? |
| 8 | ? |
| 9 | ? |

### `PARAM.ID`

| Value | Meaning |
| --- | --- |
| 0 | ? |
| 1 | Color palette |
| 2 | Grayscale toggle |
| 3 | Transform |
| 10 | Size |
| 11 | One way only |
| 12 | Fading/Nb pixels on |
| 13 | Go outside |
| 14 | Gradient |

### `COLOR.VAL`

asdf

## Scene types

### Steps

This scene type is the simplest of the 'complex' scenes. It is built specifying the state of the channels of each fixture in each step, and allows controlling the time taken in each step, as well as the fade time between steps.

```xml
<FIXTUREDATAS NB="0"/> <!-- No fixtures are saved in the scene, as the data is different in each step -->
<RACKS>
    <RACK TYPE="9"> 
        <STEPS NB="2">
            <!-- Each unit of time specified equals 40ms. So, 25 = 1s, 12 = 0.5s -->
            <STEP WAITTIME="25" FADETIME="0">
                <FIXTUREDATAS NB="16">
                    <FIXTUREDATA FIXTURE="8b79ab84-e1ad-4ad6-9011-7ea3004c1812" DATA="eJxiYGT4z8DAwLiHARu0AWIGAAAAAP//"/> <!-- Inside each step, the data is specified. -->
                    ...
                </FIXTUREDATAS>
            </STEP>
            <STEP WAITTIME="250" FADETIME="12">
                <FIXTUREDATAS NB="16">
                    <FIXTUREDATA FIXTURE="8b79ab84-e1ad-4ad6-9011-7ea3004c1812" DATA="eJxiYGSQZGBgYNzDgA3qpe1hYAAAAAD//w=="/>
                    ...
                </FIXTUREDATAS>
            </STEP>
        </STEPS>
    </RACK>
</RACKS>
```

### COLOR FX

This scene type allows for color-related efects, without taking into account movement. The scene is based around specific templates, which dictate the overall look of the effect.

```xml
<RACKS>
    <RACK EXPAND_RACK="1" TYPE="2"> <!-- Type 2 means COLOR FX -->
        <EFFECT TYPE="2" ID="127" DURATION="5000"> <!-- The effect type might be the template -->
            <PARAMS NB="8"> 
                <!--  -->
                <PARAM TYPE="4" ID="1">
                    <COLORS NB="5">
                        <COLOR VAL="1/1/1/0/0/0/0/0/1 / 1/1/1/0/0/0/0/0/1"/>
                        <COLOR VAL="1/0/0/0/0/0/0/0/1 / 1/1/1/0/0/0/0/0/1"/>
                        <COLOR VAL="1/1/0/0/0/0/0/0/1 / 1/1/1/0/0/0/0/0/1"/>
                        <COLOR VAL="1/1/0/0/0/0/0/0/1 / 1/1/1/0/0/0/0/0/1"/>
                        <COLOR VAL="0/1/0/0/0/0/0/0/1 / 1/1/1/0/0/0/0/0/1"/>
                    </COLORS>
                </PARAM>
                <PARAM TYPE="2" ID="2" VAL="0"/>
                <PARAM TYPE="6" ID="3" VAL="0"/>
                <PARAM TYPE="0" ID="10" VAL="16"/>
                <PARAM TYPE="2" ID="11" VAL="1"/>
                <PARAM TYPE="2" ID="12" VAL="1"/>
                <PARAM TYPE="2" ID="13" VAL="1"/>
                <PARAM TYPE="0" ID="14" VAL="33"/>
            </PARAMS>
        </EFFECT>
        <BEAMS NB="16">
            <BEAM FIXTURE="1cf48985-4289-4c6b-9279-f2bcd9f2e014" BEAMID="0" IDSELECTION="1"/>
            <BEAM FIXTURE="7b22f963-bc2f-4fd8-bb79-408c73f7f7a4" BEAMID="0" IDSELECTION="2"/>
            <BEAM FIXTURE="b6515767-1939-4fb7-abcd-e79ea4d8149e" BEAMID="0" IDSELECTION="3"/>
            <BEAM FIXTURE="cb2ec4af-1e21-424e-8162-9d1b77b864dd" BEAMID="0" IDSELECTION="4"/>
            <BEAM FIXTURE="35956133-fd90-47fa-a618-0625f6be771f" BEAMID="0" IDSELECTION="5"/>
            <BEAM FIXTURE="e71ab409-27a0-4412-ab35-9891c31cdb17" BEAMID="0" IDSELECTION="6"/>
            <BEAM FIXTURE="15175965-00a1-4404-a1cd-70ecd687d639" BEAMID="0" IDSELECTION="7"/>
            <BEAM FIXTURE="cf654af3-a86c-4bac-b36f-9cc5c5a4e6a5" BEAMID="0" IDSELECTION="8"/>
            <BEAM FIXTURE="329e8f59-ce68-4f18-af7b-b464c1b449d8" BEAMID="0" IDSELECTION="9"/>
            <BEAM FIXTURE="8394a512-a0e8-465a-8e5d-5f9c1ae4b36b" BEAMID="0" IDSELECTION="10"/>
            <BEAM FIXTURE="438167f4-3cb0-4aec-b977-535b65b285c6" BEAMID="0" IDSELECTION="11"/>
            <BEAM FIXTURE="4aa34685-e29f-45c1-aa44-9e548507c045" BEAMID="0" IDSELECTION="12"/>
            <BEAM FIXTURE="7f0a07d8-9a27-4f14-a2b3-0ba4a8f96cc9" BEAMID="0" IDSELECTION="13"/>
            <BEAM FIXTURE="4889fcaa-50e6-4506-bcc9-b5a006414598" BEAMID="0" IDSELECTION="14"/>
            <BEAM FIXTURE="d61a18f2-ff08-47c5-9810-e55ace1d19c8" BEAMID="0" IDSELECTION="15"/>
            <BEAM FIXTURE="03d89e04-ebc8-4cc4-8cfb-48886d08f9ae" BEAMID="0" IDSELECTION="16"/>
        </BEAMS>
    </RACK>
</RACKS>
```
