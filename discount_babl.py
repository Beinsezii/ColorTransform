#!/usr/bin/python3
import math


# 'class', more just a struct with methods
class Color():
    """Stored internally as sRGB, aka the universal format.
as_ functions return float tuples, or int tuple for IRGB and a str for HEX.
set_ functions return self.

CIE LAB is calculated @ D65 2 degrees.

No alpha channel support, as it's not part of the colorspaces.
The only conversions would be from int, float, and hex."""
    def __init__(self,
                 r: float = 1.0,
                 g: float = 1.0,
                 b: float = 1.0):
        self.R = r
        self.G = g
        self.B = b

    # ##### Get functions #####

    # {{{

    def as_SRGB(self) -> tuple:
        """Return sRGB"""
        return (self.R, self.G, self.B)

    def as_IRGB(self) -> tuple:
        """Return Integer sRGB"""
        return (max(0, min(255, int(round(self.R * 255)))),
                max(0, min(255, int(round(self.G * 255)))),
                max(0, min(255, int(round(self.B * 255)))))

    def as_HEX(self) -> str:
        """Return hex string"""
        Hex = "#"

        for x in self.as_IRGB():
            n1 = int(x / 16)
            n2 = x % 16
            for n in (n1, n2):
                Hex += str(chr((n - 10) + 65) if n >= 10 else n)

        return Hex

    def as_LRGB(self) -> tuple:
        """Return linear RGB"""
        return tuple(map(
            lambda c:
                c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4,
            self.as_SRGB()))

    def as_XYZ(self) -> tuple:
        """Return XYZ"""
        R, G, B = self.as_LRGB()
        return (
            (0.4124 * R + 0.3576 * G + 0.1805 * B) * 100,  # X
            (0.2126 * R + 0.7152 * G + 0.0722 * B) * 100,  # Y
            (0.0193 * R + 0.1192 * G + 0.9505 * B) * 100,  # Z
        )

    def as_LAB(self) -> tuple:
        """Return CIE LAB"""
        # convert to D65 2 degrees
        X, Y, Z = self.as_XYZ()
        X /= 95.057
        Y /= 100
        Z /= 108.883

        X, Y, Z = tuple(map(
            lambda c: c ** (1 / 3) if (c > 0.008856)
            else (7.787 * c) + (16 / 116),
            (X, Y, Z)
        ))

        L = (116 * Y) - 16
        A = 500 * (X - Y)
        B = 200 * (Y - Z)

        return (L, A, B)

    def as_LCH(self) -> tuple:
        """Return CIE LCH"""
        L, A, B = self.as_LAB()

        H = math.atan2(B, A)
        if H > 0:
            H = (H / math.pi) * 180
        else:
            H = 360 - ((abs(H) / math.pi) * 180)

        C = math.sqrt((A ** 2) + (B ** 2))

        return (L, C, H)

    # }}}

    # ##### Set functions #####

    # {{{

    def set_SRGB(self, r: float, g: float, b: float) -> 'Color':
        """Set from sRGB"""
        self.R = r
        self.G = g
        self.B = b
        # so you can do Color().set_FORMAT(...).as_FORMAT(...)
        # to essentially use it functionally. Questionable.
        return self

    def set_IRGB(self, r: int, g: int, b: int) -> 'Color':
        """ Set from integer RGB"""
        return self.set_SRGB(r / 255, g / 255, b / 255)

    def set_HEX(self, hex: str) -> 'Color':
        """Set from hex string"""
        hex = hex.lstrip('#').upper()

        hexR = hex[0:2]
        hexG = hex[2:4]
        hexB = hex[4:6]

        rgb = [0, 0, 0]
        for n, x in enumerate((hexR, hexG, hexB)):
            # 16s place
            if x[0].isalpha():
                rgb[n] += (ord(x[0]) - 65 + 10) * 16
            elif x[0].isdigit():
                rgb[n] += int(x[0]) * 16
            else:
                print("This should be impossible.")
                raise ValueError
            # 1s place
            if x[1].isalpha():
                rgb[n] += (ord(x[1]) - 65 + 10)
            elif x[1].isdigit():
                rgb[n] += int(x[1])
            else:
                print("This should be impossible.")
                raise ValueError

        return self.set_IRGB(*rgb)

    def set_LRGB(self, r: float, g: float, b: float) -> 'Color':
        """Set from linear RGB"""
        return self.set_SRGB(*tuple(map(
            lambda c: 12.92 * c if c <= 0.0031308
            else 1.055 * (c ** (1 / 2.4)) - 0.055,
            (r, g, b)
        )))

    def set_XYZ(self, x: float, y: float, z: float) -> 'Color':
        """Set from XYZ"""
        x /= 100
        y /= 100
        z /= 100
        return self.set_LRGB(
            3.2406 * x - 1.5372 * y - 0.4986 * z,
            -0.9689 * x + 1.8758 * y + 0.0415 * z,
            0.0557 * x - 0.2040 * y + 1.0570 * z,
        )

    def set_LAB(self, l: float, a: float, b: float) -> 'Color':  # noqa: E741
        """Set from CIE LAB"""
        y = (l + 16) / 116
        x = (a / 500) + y
        z = y - (b / 200)

        x, y, z = tuple(map(
            lambda c:
                c ** 3 if (c**3 > 0.008856) else (c - (16 / 116)) / 7.787,
            (x, y, z)
        ))

        # convert back from D65 2 degrees
        x *= 95.057
        y *= 100
        z *= 108.883

        return self.set_XYZ(x, y, z)

    def set_LCH(self, l: float, c: float, h: float) -> 'Color':  # noqa: E741
        """Set from CIE LCH"""
        return self.set_LAB(
            l,
            math.cos(math.radians(h)) * c,
            math.sin(math.radians(h)) * c,
        )

    # }}}
