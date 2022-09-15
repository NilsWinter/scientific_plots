import os
import struct
from glob import glob

from matplotlib import font_manager

import scientific_plots as sp


def get_style(stylesheet_name='mmll'):
    """
    Function to get stylesheet to be used to apply a style to matplotlib plots.
    Example:
    >> import matplotlib.pyplot as plt
    >> from sciplotlib import style as spstyle
    >> nature_style = spstyle.get_style('nature')
    >> with plt.style.context(nature_style):
    >>      plt.plot([1, 2, 3, 4, 5])
    Parameters
    ----------
    stylesheet_name : (str)
        name of stylesheet to get
    Returns
    -------
    stylesheet_path : (str)
        path of stylesheet
    """

    package_dir = sp.__path__[0]
    dirname = os.path.join(package_dir, 'styles')
    stylesheet_path = os.path.join(dirname, stylesheet_name + '.mplstyle')

    return stylesheet_path


def get_palette(name='nature-reviews', output_type='hex'):
    """
    Currently copied from here
    https://github.com/Timothysit/sciplotlib/blob/master/module/style.py

    Parameters
    ----------
    name : (str)
        name of the color scheme you want to get
    output_type : (str)
        way in which the color is specified: hex or RGB
    Returns
    -------
    """

    supported_colorschemes = ['nature-reviews', 'nature', 'economist', 'aaas',
                              'mondrian', 'kanagawa']

    if (name == 'nature-reviews') or (name == 'nature'):
        colors = ['#E64B35', '#4DBBD5', '#00A087', '#3C5488',
                  '#F39B7F', '#8491B4', '#91D1C2FF', '#DC0000',
                  '#7E6148', '#B09C85']
    elif name == 'economist':
        colors = ['#6794a7', '#014d64', '#7ad2f6', '#01a2d9',
                  '#7bc0c1', '#00887d', '#91D1C2FF', '#DC0000',
                  '#7E6148', '#B09C85']
    elif name == 'aaas':
        colors = ['#3B4992FF', '#EE0000FF', '#008B45FF',
                  '#631879FF', '#008280FF', '#BB0021FF',
                  '#5F559BFF', '#A20056FF', '#808180FF',
                  '#1B1919FF']
    elif name == 'mondrian':
        # based on the wikipedia image of
        # Composition with Red Blue and Yello
        colors = ["#DD271C", '#015A9C', '#EBDC75', '#071C13', '#E5E3E4']
    elif name == 'kanagawa':
        # based on the Great Wave of Kanagawa
        # Source: http://sierrakellermeyer.com/blog/10-color-palettes-based-on-famous-paintings
        colors = ['#7E9CA7', '#C1B9A9', '#DED4C5', "#07244b",
                  "#45494D"]
    else:
        print('No valid color scheme specified, returning none')
        print('The supported color schemes are ' + supported_colorschemes)
        colors = None

    if output_type == 'rgb':
        # remove the '#', then convert to RGB
        colors = [struct.unpack('BBB', color[1:].decode('hex')) for color in colors]

    return colors


def add_fonts():
    package_dir = sp.__path__[0]
    dirname = os.path.join(package_dir, 'fonts/*')
    font_folders = glob(dirname)
    for folder in font_folders:
        for font in font_manager.findSystemFonts(folder):
            font_manager.fontManager.addfont(font)
