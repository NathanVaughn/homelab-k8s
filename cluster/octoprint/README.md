# Octoprint

## Post Setup

- Stream URL: `https://octoprint-cam.nathanv.app/?action=stream`
- Snapshot URL: `https://octoprint-cam.nathanv.app/?action=snapshot`
- Path to FFMPEG: `/usr/bin/ffmpeg`
- Restart command: `s6-svc -r /var/run/s6/services/octoprint`

While Octoprint does host the webcam on `/webcam/` as well, this seems less reliable.

### Ender 3 Config

- Origin: Lower Left
- Heated Bed: true
- Width: 220m
- Depth: 220m
- Height: 250m
- Nozzle Diameter: 0.4mm

### Cura

Not needed in OctoPrint, but setup in Cura:

Start:

```gcode
; Ender 3 Custom Start G-code
G92 E0 ; Reset Extruder
G28 ; Home all axes
G29 ; Bed-leveling
G1 Z2.0 F3000 ; Move Z Axis up little to prevent scratching of Heat Bed
G1 X0.1 Y20 Z0.3 F5000.0 ; Move to start position
G1 X0.1 Y200.0 Z0.3 F1500.0 E15 ; Draw the first line
G1 X0.4 Y200.0 Z0.3 F5000.0 ; Move to side a little
G1 X0.4 Y20 Z0.3 F1500.0 E30 ; Draw the second line
G92 E0 ; Reset Extruder
G1 Z2.0 F3000 ; Move Z Axis up little to prevent scratching of Heat Bed
G1 X5 Y20 Z0.3 F5000.0 ; Move over to prevent blob squish
```

End:

```gcode
G91 ;Relative positioning
G1 E-2 F2700 ;Retract a bit
G1 E-2 Z0.2 F2400 ;Retract and raise Z
G1 X5 Y5 F3000 ;Wipe out
G1 Z10 ;Raise Z more
G90 ;Absolute positioning

G1 X0 Y{machine_depth} ;Present print
M106 S0 ;Turn-off fan
M104 S0 ;Turn-off hotend
M140 S0 ;Turn-off bed

M84 X Y E ;Disable all steppers but Z
```