#!/usr/bin/python3
import math
import re


# All functions based off of the most 'standard' way. RGB = sRGB unless specified. CIE uses D65 @ 2 degrees
# RGB is represented as 0.0...1.0 instead of 0...255. Use converters if necessary
# Nothing checks for clipping by default. Clip checking functions provided.

# Formats:
# SRGB - Standard RGB
# IRGB - Same as SRGB but uses ints (0...255 instead of 0.0...1.0)
# HEX - Hex RGB. ie, "#FFAA00"
# LRGB - RGB without gamma corrections, ie Linear RGB
# XYZ - CIE XYZ format
# LAB - CIE Lab format
# LCH - CIE Lch "Lightness Chroma Hue" format. Personal favorite and initial reason for creating this module.


# int RGB to float RGB
def IRGBtoSRGB(R: int, G: int, B: int) -> tuple:
    return (R / 255, G / 255, B / 255)


# float RGB (0.0...1.0) to int RGB (0...255)
def SRGBtoIRGB(R: float, G: float, B: float) -> tuple:
    return (int(round(R * 255)), int(round(G * 255)), int(round(B * 255)))


def HEXtoIRGB(Hex: str) -> tuple:
    if not HEXvalid(Hex):
        raise ValueError
    Hex = Hex.lstrip('#').upper()

    hexR = Hex[0:2]
    hexG = Hex[2:4]
    hexB = Hex[4:6]

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

    return tuple(rgb)


# Exception to 'no clip check' rule, as any values outside 0..255 will produce an invalid hex.
def IRGBtoHEX(R: int, G: int, B: int) -> str:
    if IRGBclip(R, G, B):
        raise ValueError
    Hex = "#"

    for x in (R, G, B):
        n1 = int(x / 16)
        n2 = x % 16
        for n in (n1, n2):
            Hex += str(chr((n - 10) + 65) if n >= 10 else n)

    return Hex


# gamma corrected to linear
def GtoL(C: float) -> float:
    if C <= 0.04045:
        C = C / 12.92
    else:
        C = ((C + 0.055) / 1.055) ** 2.4
    return C


# linear to gamma corrected
def LtoG(C: float) -> float:
    if C <= 0.0031308:
        C = 12.92 * C
    else:
        C = 1.055 * (C ** (1 / 2.4)) - 0.055
    return C


# batch linear to gamma
def LRGBtoSRGB(R: float, G: float, B: float) -> tuple:
    return (LtoG(R), LtoG(G), LtoG(B))


# batch gamma to linear
def SRGBtoLRGB(R: float, G: float, B: float) -> tuple:
    return (GtoL(R), GtoL(G), GtoL(B))


def LRGBtoXYZ(R: float, G: float, B: float) -> tuple:
    X = (0.4124*R + 0.3576*G + 0.1805*B) * 100
    Y = (0.2126*R + 0.7152*G + 0.0722*B) * 100
    Z = (0.0193*R + 0.1192*G + 0.9505*B) * 100
    return (X, Y, Z)


def SRGBtoXYZ(R: float, G: float, B: float) -> tuple:
    return(LRGBtoXYZ(*SRGBtoLRGB(R, G, B)))


def XYZtoLRGB(X: float, Y: float, Z: float) -> tuple:
    X /= 100
    Y /= 100
    Z /= 100
    R = 3.2406*X - 1.5372*Y - 0.4986*Z
    G = -0.9689*X + 1.8758*Y + 0.0415*Z
    B = 0.0557*X - 0.2040*Y + 1.0570*Z
    return (R, G, B)


def XYZtoSRGB(X: float, Y: float, Z: float) -> tuple:
    return LRGBtoSRGB(*XYZtoLRGB(X, Y, Z))


def XYZtoLAB(X: float, Y: float, Z: float) -> tuple:
    # reference vals. D65 @ 2 degrees
    X /= 95.057
    Y /= 100
    Z /= 108.883

    def f(n):
        if (n > 0.008856):
            return n ** (1 / 3)
        else:
            return (7.787 * n) + (16 / 116)
    X = f(X)
    Y = f(Y)
    Z = f(Z)

    L = (116 * Y) - 16
    A = 500 * (X - Y)
    B = 200 * (Y - Z)

    return (L, A, B)


def LABtoXYZ(L: float, A: float, B: float) -> tuple:
    Y = (L + 16) / 116
    X = (A / 500) + Y
    Z = Y - (B / 200)

    def f(n):
        if (n**3 > 0.008856):
            return n ** 3
        else:
            return (n - (16 / 116)) / 7.787
    X = f(X)
    Y = f(Y)
    Z = f(Z)

    X *= 95.057
    Y *= 100
    Z *= 108.883

    return (X, Y, Z)


def SRGBtoLAB(R: float, G: float, B: float) -> tuple:
    return XYZtoLAB(*SRGBtoXYZ(R, G, B))


def LABtoSRGB(L: float, A: float, B: float) -> tuple:
    return XYZtoSRGB(*LABtoXYZ(L, A, B))


def LABtoLCH(L: float, A: float, B: float) -> tuple:
    H = math.atan2(B, A)

    if H > 0:
        H = (H / math.pi) * 180
    else:
        H = 360 - ((abs(H) / math.pi) * 180)

    C = math.sqrt((A ** 2) + (B ** 2))

    return (L, C, H)


def LCHtoLAB(L: float, C: float, H: float) -> tuple:
    A = math.cos(math.radians(H)) * C
    B = math.sin(math.radians(H)) * C
    return (L, A, B)


def SRGBtoLCH(R: float, G: float, B: float) -> tuple:
    return LABtoLCH(*SRGBtoLAB(R, G, B))


def LCHtoSRGB(L: float, C: float, H: float) -> tuple:
    return LABtoSRGB(*LCHtoLAB(L, C, H))


# In theory would also work for LRGB if needed in a pinch.
def SRGBclip(R: float, G: float, B: float) -> tuple:
    for x in (R, G, B):
        if x > 1.0:
            return True, 1
        elif x < 0.0:
            return True, 0
    return False


def IRGBclip(R: int, G: int, B: int) -> bool:
    for x in (R, G, B):
        if x > 255:
            return True, 1
        elif x < 0:
            return True, 0
    return False


# Note, 'valid' returns true if acceptable.
# Compared to 'clip' which returns true if values are outside a range
def HEXvalid(Hex: str) -> bool:
    return bool(re.fullmatch(r"#[0-9A-Fa-f]{6}", Hex))


# I'm going to be honest I haven't read into the science of XYZ at all outside of how it's different from sRGB.
# Therefore, omitting for now.
def XYZclip(X: float, Y: float, Z: float) -> bool:
    pass


# For both LAB and LCH, I've read that clip vals aren't exactly 100, but I can't find much information on it.
# If a good source is found with adequate reason to change, the clip vals will be updated

# In theory would also work XYZ if needed in a pinch
def LABclip(L: float, A: float, B: float) -> bool:
    for x in (L, A, B):
        if x > 100.0:
            return True, 1
        elif x < 0.0:
            return True, 0
    return False


def LCHclip(L: float, C: float, H: float) -> bool:
    for x in (L, C):
        if x > 100.0:
            return True, 1
        elif x < 0.0:
            return True, 0
    if H > 360.0:
        return True, 1
    elif H < 0.0:
        return True, 0
    return False
