# Discount BABL
It's basically just a bunch of colorspace transformation algorithms stored in a .py file. Imagine if BABL was slower and had less features.

### Current Status
Convert to/from sRGB, integer RGB, hexadecimal, linear RGB, XYZ, CIE LAB, and CIE LCH.

HSL/HSV support todo

## Description
It's just a single class called "Color" that has 3 fields for sRGB R, G, B, and a bunch of different methods to set or retrieve the value as any format.

```python
from discount_babl import Color

# set_ fns return self
color1 = Color().set_LCH(60, 35, 240)

print(color1.as_LAB())
>>> (60.00088343939376, -17.499393070593783, -30.310025186940948)

print(color1.as_SRGB())
>>> (0.1401421059848601, 0.6110329053739673, 0.7732676695658262)

print(Color().set_HEX('#AF0844').as_LCH())
>>> (37.3076521100872, 63.23728181801215, 13.113554007284156)
```

Algorithms were sourced from https://www.easyrgb.com/en/math.php with results compared to other converters, so they may not be optimal. New algorithm proposals welcome.

## FAQ
Question|Answer
--------|------
**Q.** Alpha?|**A.** Not supported. Alpha isn't part of colorspaces. The only 'conversion' would be multiplying by 255 and rounding for integer rgb, and the hex jibberish.
**Q.** Why did you make this instead of using something else?|**A.** I didn't feel like downloading a whole-ass image processing library just to say "hey take this rgb tuple and make it lch", so I wrote this. I looked at solutions like Babl but it's GObject Introspection library seems incomplete.
