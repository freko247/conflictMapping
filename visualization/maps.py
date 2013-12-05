# -*- coding: utf-8 -*-
"""
Module with methods for visualizing data with different graphs.
"""
from bisect import bisect
import cStringIO
import os

import matplotlib.pyplot as plt
import shapefile


def heat_map(map_file, data, output='stream'):
    """
    Method takes path to shape file as first argument. Method takes data,
    in the form of a list of tuples (title, value), as second argument.

    The different shapes in the shape file are matched with the titles
    in the data.
    The shapes are coloured based on the relative value from the data.
    If a shape is not recognised/matched it will be colored grey.

    The method also takes an optional third argument, output.
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
    shape_titles = [title.lower() for title in shape_titles]
    shape_values = zip(*data)[1]
    # Color map
    # TODO: Fix more colors
    colors = ['green', 'yellow', 'orange', 'red']
    data_interval = []
    max_shape_value = (max(shape_values))
    for i in range(len(colors) - 1):
        data_interval.append(((i + 1) * max_shape_value / len(colors)))
    # Plot
    fig = plt.figure(figsize=(14, 9))
    ax = fig.add_subplot(111)
    for index, shape in enumerate(sf.shapes()):
        parts = []
        shape_title = sf.record(index)[4].lower()
        if shape_title in shape_titles:
            color = colors[bisect(data_interval,
                           shape_values[shape_titles.index(shape_title)])]
        else:
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
