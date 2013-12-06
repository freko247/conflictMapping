# -*- coding: utf-8 -*-
"""
Module with methods for visualizing data with different graphs.
"""
from bisect import bisect
import cStringIO
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import shapefile


def heat_map(map_file, data, logger=None, output='stream'):
    """
    Method takes path to shape file as first argument. Method takes data,
    in the form of a list of tuples (title, value), as second argument.

    The different shapes in the shape file are matched with the titles
    in the data.
    The shapes are coloured based on the relative value from the data.
    If a shape is not recognised/matched it will be colored grey.

    The third given argument

    The method also takes an optional fourth argument, output.
    This determines in what format the plot should be output. The default value
    is 'stream'.

    'stream': Sends the plot as a data stream (used when serving html files).
    'plot'  : Opens the plot in a new dialog window.
    'save'  : Saves the plot as 'plot.png' in the current directory.
    """
    if output not in ['stream', 'plot', 'save']:
        return None
    sf = shapefile.Reader(map_file)
    shape_titles = zip(*data)[0]
    shape_titles = [title.lower().strip('"') for title in shape_titles]
    shape_values = zip(*data)[1]
    # Color map
    colors = ['#00E58E', '#00E585', '#01E57D', '#01E674',
              '#02E66C', '#03E663', '#03E75B', '#04E752',
              '#05E74A', '#05E842', '#06E839', '#07E931',
              '#07E929', '#08E921', '#09EA19', '#09EA10',
              '#0CEA0A', '#15EB0B', '#1EEB0B', '#28EB0C',
              '#31EC0D', '#3BEC0D', '#44ED0E', '#4DED0F',
              '#57ED0F', '#60EE10', '#69EE11', '#72EE11',
              '#7CEF12', '#85EF13', '#8EEF13', '#97F014',
              '#A0F015', '#A9F116', '#B2F116', '#BBF117',
              '#C4F218', '#CDF218', '#D6F219', '#DFF31A',
              '#E8F31B', '#F1F31B', '#F4EE1C', '#F4E61D',
              '#F5DE1D', '#F5D61E', '#F5CE1F', '#F6C620',
              '#F6BE20', '#F6B621', '#F7AE22', '#F7A622',
              '#F79E23', '#F89724', '#F88F25', '#F98725',
              '#F97F26', '#F97827', '#FA7028', '#FA6928',
              '#FA6129', '#FB592A', '#FB522B', '#FC4A2C',
              ]
    data_interval = []
    max_shape_value = (max(shape_values))
    for i in range(len(colors) - 1):
        data_interval.append(((i + 1) * max_shape_value / len(colors)))
    # Plot
    fig = plt.figure(figsize=(14, 9))
    ax = fig.add_subplot(111)
    for index, shape in enumerate(sf.shapes()):
        parts = []
        title = sf.record(index)[4].lower()
        if title in shape_titles:
            color = colors[bisect(data_interval,
                           shape_values[shape_titles.index(title)])]
        else:
            if logger:
                logger.debug('No match for: %s' % title)
            color = 'grey'
        for i, p in enumerate(shape.parts):
            pnext = -1 if i == len(shape.parts) - 1 else shape.parts[i + 1]
            parts.append(shape.points[p:pnext])
        for part in parts:
            ax.add_artist(plt.Polygon(part,
                                      edgecolor=(.5, .6, 1),
                                      facecolor='none',
                                      linewidth=.5,
                                      zorder=5))
            ax.add_artist(plt.Polygon(part,
                                      edgecolor='none',
                                      facecolor=color,
                                      linewidth=1,
                                      zorder=2))
    ax.set_xlim(-200, 200)
    ax.set_ylim(-100, 100)
    ax.set_axis_off()
    if output == 'stream':
        # Output to IOstream
        format = "png"
        sio = cStringIO.StringIO()
        plt.savefig(sio, format=format)
        return sio.getvalue().encode("base64").strip()
    elif output == 'plot':
        # Output to new dialog window
        plt.show()
        return ''
    elif output == 'save':
        # Output to file
        plt.savefig("plot.png")
        return ''


def main():
    """
    Module main method, mainly used for testing
    different methods in the module.
    """
    map_file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'static',
                            'TM_WORLD_BORDERS-0.3.shp')
    data = [('Finland', 100),
            ('Sweden', 200),
            ('Norway', 300),
            ('Denmark', 150)
            ]
    heat_map(map_file, data, output='save')

if __name__ == '__main__':
    main()
