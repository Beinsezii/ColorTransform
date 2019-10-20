# ColorTransform.py
It's basically just a bunch of colorspace transformation algorithms stored in a .py file.

### Current Status
Conversions between sRGB, linear RGB, CIE XYZ, CIE Lab, and CIE Lch are present.

## Description
No, it's really just a file of like 20 color conversion functions.

### Main Design Goals
Work.

### Future Goals
Add sRGB <-> hex, functions to check clipping for different formats.

## Features
Basically, this
```python
import colortransform as ct

# int rgb to float. all processing is done in floats.
color1: tuple = ct.RGBitof(100, 150, 200)
print(color1)
>(0.39, 0.58, 0.78)

# sRGB into Lab
print( ct.SRGBtoLAB(*color1) )
>(60.5, -2.79, -30.9)

# Lch into sRGB
print( ct.SRGBtoLCH(50.0, 30.0, 200.0) )
>(0.02, 0.51, 0.53)
```
Note it does no rounding, so a values will come out to python default level of decimal places.

### Experimental Features
Algorithms were sourced from https://www.easyrgb.com/en/math.php, so they may not be optimal. New algorithm proposals welcome.

## Development
Will add more conversions if I need them.

## History
I was making a ui color scheme to replace Solarized in GIMP using 2.10's new Lab/Lch features, and thought "hey, most of these colors are all directly related to the starting color. Bet I could make a math for this.

And so I did. Or tried to. Turns all the python color libraries (on the firs page of Google, at least) are part of some huge package of everything ever. I don't feel like installing an entire image processing suite just to say "make this RGB tuple an LCH one."

## FAQ
Question|Answer
--------|------
**Q.** Where are conversions such as LCHtoXYZ()?|**A.** The converters are made in 'steps'. SRGB -> LRGB is one, LRGB -> XYZ is another, XYZ -> LAB is yet another, and LAB -> LCH is the final, along with the reverse equivalents. Anything else is purely for convenience to avoid writing code. So, for example, calling SRGB -> XYZ just chains function calls to expand into SRGB -> LRGB -> XYZ -> LAB. I've added these shortcut functions only for the major working formats sRGB, LAB, and LCH, or when it's useful inside the program itself. Anything else will have to be chained together manually.
