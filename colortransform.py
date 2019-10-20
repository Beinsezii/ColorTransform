#!/usr/bin/python3
import math


# All functions based off of the most 'standard' way. RGB = sRGB unless specified. CIE uses D65 @ 2 degrees
# RGB is represented as 0.0...1.0 instead of 0...255. Use converters if necessary


# float RGB (0.0...1.0) to int RGB (0...255)
def RGBftoi(R: float, G: float, B: float) -> tuple:
    return (int(round(R * 255)), int(round(G * 255)), int(round(B * 255)))


# int RGB to float RGB
def RGBitof(R: int, G: int, B: int) -> tuple:
    return (R / 255, G / 255, B / 255)


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
