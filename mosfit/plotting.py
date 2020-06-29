"""Functions for assisting with plotting, inherited from AstroCats."""

from collections import OrderedDict
from random import seed, shuffle

import seaborn as sns
from matplotlib.colors import rgb2hex
from palettable import colorbrewer, cubehelix, wesanderson

__all__ = [
    'bandrepf', 'bandcolorf', 'radiocolorf', 'xraycolorf', 'bandaliasf',
    'bandshortaliasf', 'bandwavef', 'bandmetaf', 'bandcodes',
    'bandwavelengths',
    'bandgroupf', 'bandoffsetf'
]

bandreps = {
    'Ks': ['K_s'],
    'UVM2': ['uvm2', 'UVM2', 'UVm2', 'Um2', 'um2','M2'],
    'UVW1': ['uvw1', 'UVW1', 'UVw1', 'Uw1', 'uw1','W1'],
    'UVW2': ['uvw2', 'UVW2', 'UVw2', 'Uw2', 'uw2','W2'],
}

# Some bands are uniquely tied to an instrument/telescope/system, add this
# info here.
bandmeta = {
    'UVM2': {'telescope': 'Swift', 'instrument': 'UVOT'},
    'UVW1': {'telescope': 'Swift', 'instrument': 'UVOT'},
    'UVW2': {'telescope': 'Swift', 'instrument': 'UVOT'},
    'F110W': {'telescope': 'Hubble', 'instrument': 'WFC3'},
    'F225W': {'telescope': 'HST', 'instrument': 'UVIS'},
    'F775W': {'telescope': 'Hubble', 'instrument': 'WFC3'},
    'F850LP': {'telescope': 'Hubble', 'instrument': 'WFC3'}
}

bandcodes = [
    "u",
    "g",
    "r",
    "i",
    "z",
    "u'",
    "g'",
    "r'",
    "i'",
    "z'",
    "u_SDSS",
    "g_SDSS",
    "r_SDSS",
    "i_SDSS",
    "z_SDSS",
    "U",
    "B",
    "V",
    "R",
    "I",
    "G",
    "Y",
    "J",
    "H",
    "K",
    "C",
    "CR",
    "CV",
    "UVM2",
    "UVW1",
    "UVW2",
    "pg",
    "Mp",
    "w",
    "y",
    "Z",
    "F110W",
    "F225W",
    "F775W",
    "F850LP",
    "VM",
    "RM",
    "Ks",
    "NUV",
    "FUV",
    "BL",
    "VL"
]

bandaliases = OrderedDict([
    ("u_SDSS", "u'"),
    ("g_SDSS", "g'"),
    ("r_SDSS", "r'"),
    ("i_SDSS", "i'"),
    ("z_SDSS", "z'")
])

bandshortaliases = OrderedDict([
    ("u_SDSS", "u'"),
    ("g_SDSS", "g'"),
    ("r_SDSS", "r'"),
    ("i_SDSS", "i'"),
    ("z_SDSS", "z'"),
])

bandwavelengths = {
    "u": 354.,
    "g": 475.,
    "r": 622.,
    "i": 763.,
    "z": 905.,
    "y": 963.,
    "u'": 354.,
    "g'": 475.,
    "r'": 622.,
    "i'": 763.,
    "z'": 905.,
    "U": 365.,
    "B": 445.,
    "V": 551.,
    "R": 658.,
    "I": 806.,
    "Y": 1020.,
    "J": 1220.,
    "H": 1630.,
    "K": 2190.,
    "UVM2": 260.,
    "UVW1": 224.6,
    "UVW2": 192.8,
    "FUV": 152.8,
    "NUV": 227.1 
}

bandgroups = {
    "SDSS": ["u'", "g'", "r'", "i'", "z'"],
    "UVOT": ["UVW2", "UVM2", "UVW1"],
    "HST": ['F110W', 'F225W', 'F775W', 'F850LP'],
    "Johnson": ['U', 'B', 'V', 'R', 'I', 'Y', 'J', 'H', 'K'],
    "GALEX": ['NUV', 'FUV']
}

radiocodes = [
    "5.9"
]
xraycodes = [
    "0.3 - 10",
    "0.5 - 8"
]

seed(101)
# bandcolors = ["#%06x" % round(float(x)/float(len(bandcodes))*0xFFFEFF)
# for x in range(len(bandcodes))]
bandcolors = (cubehelix.cubehelix1_16.hex_colors[2:13] +
              cubehelix.cubehelix2_16.hex_colors[2:13] +
              cubehelix.cubehelix3_16.hex_colors[2:13])
shuffle(bandcolors)
bandcolors2 = cubehelix.perceptual_rainbow_16.hex_colors
shuffle(bandcolors2)


#bandcolors = cubehelix.perceptual_rainbow_16.hex_colors

#bandcolors = (cubehelix.cubehelix3_16.hex_colors[4:13])

#shuffle(bandcolors)

bandcolors = bandcolors + bandcolors2

bandcolordict = dict(list(zip(bandcodes, bandcolors)))

radiocolors = wesanderson.Zissou_5.hex_colors
shuffle(radiocolors)
radiocolordict = dict(list(zip(radiocodes, radiocolors)))

xraycolors = colorbrewer.sequential.Oranges_9.hex_colors[2:]
shuffle(xraycolors)
xraycolordict = dict(list(zip(xraycodes, xraycolors)))


def bandrepf(code):
    """Replace code with band name."""
    for rep in bandreps:
        if code in bandreps[rep]:
            return rep
    return code


def bandcolorf(code):
    """Replace band code with color."""
    newcode = bandrepf(code)
    if newcode in bandcolordict:
        return bandcolordict[newcode]
    return 'black'


def radiocolorf(freq):
    """Replace radio code with color."""
    ffreq = (float(freq) - 1.0) / (45.0 - 1.0)
    pal = sns.diverging_palette(200, 60, l=80, as_cmap=True, center="dark")
    return rgb2hex(pal(ffreq))


def xraycolorf(code):
    """Replace xray code with color."""
    if code in xraycolordict:
        return xraycolordict[code]
    return 'black'


def bandaliasf(code):
    """Replace band alias with name."""
    newcode = bandrepf(code)
    if newcode in bandaliases:
        return bandaliases[newcode]
    return newcode


def bandgroupf(code):
    """Replace band code with group."""
    newcode = bandrepf(code)
    for group in bandgroups:
        if newcode in bandgroups[group]:
            return group
    return ''


def bandshortaliasf(code):
    """Replace band code with short alias."""
    newcode = bandrepf(code)
    if newcode in bandshortaliases:
        return bandshortaliases[newcode]
    return newcode


def bandwavef(code):
    """Replace band code with wavelength."""
    newcode = bandrepf(code)
    if newcode in bandwavelengths:
        return bandwavelengths[newcode]
    return 0.


def bandmetaf(band, field):
    """Replace band with meta."""
    if band in bandmeta:
        if field in bandmeta[band]:
            return bandmeta[band][field]
    return ''

bandoffsets={
    "u":1.4,
    "g":-0.9,
    "r":0,
    "i":1.0,
    "z":1.7,
    "u'":1.4,
    "g'":-0.9,
    "r'":0,
    "i'":1.0,
    "z'":1.7,
    "u_SDSS":1.4,
    "g_SDSS":-0.9,
    "r_SDSS":0,
    "i_SDSS":1.0,
    "z_SDSS":1.7,
    "U":0.4,
    "B":2.1,
    "V":2.8,
    "R":0,
    "I":0,
    "G":0,
    "Y":0,
    "J":0,
    "H":0,
    "K":0,
    "C":0,
    "CR":0,
    "CV":0,
    "UVM2":-2,
    "UVW1":-3,
    "UVW2":-1,
    "pg":0,
    "Mp":0,
    "w":0,
    "y":0,
    "Z":0,
    "F110W":0,
    "F225W":-0.9,
    "F775W":0,
    "F850LP":0,
    "VM":0,
    "RM":0,
    "Ks":0,
    "NUV":-2.5,
    "FUV":-1.5,
    "BL":1.5,
    "VL":1.2
}

def bandoffsetf(code):
    """Set up offset for each band to keep lightcurves staggered"""
    newcode = bandrepf(code)
    if newcode in bandoffsets:
        return bandoffsets[newcode]
    return 0

