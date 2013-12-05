# -*- coding: utf-8 -*-
from bisect import bisect
import os

import matplotlib.pyplot as plt
import shapefile


def heat_map(map_file, data):
    sf = shapefile.Reader(map_file)
    shapes = sf.shapes()
    shape_titles = data[0]
    shape_values = data[1]
    # Color map
    colors = ['green', 'yellow', 'orange', 'red']  # TODO: Fix more colors
    data_interval = []
    max_shape_value = (max(shape_values))
    for i in range(len(colors)):
        data_interval.append(((i + 1) * max_shape_value / len(colors)))
    # Shapes
    record_indexes = []
    for index, record in enumerate(sf.records()):
        if record[4] in shape_titles:
            record_indexes.append(index)
    shapes = []
    for record in record_indexes:
        shapes.append(sf.shapeRecord(record).shape)

    fig = plt.figure(figsize=(14, 14))
    ax = fig.add_subplot(111)
    for shape, value in zip(shapes, shape_values):
        parts = []
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
                                      facecolor=colors[bisect(
                                                       data_interval,
                                                       value) - 1
                                                       ],
                                      linewidth=1,
                                      zorder=2))
    ax.set_xlim(-200, 200)
    ax.set_ylim(-100, 100)
    # TODO: plot to IOstream
    plt.show()


def main():
    map_file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'static',
                            'TM_WORLD_BORDERS-0.3.shp')
    data = (['Finland', 'Sweden', 'Norway', 'Denmark'],
            [100, 200, 300, 150]
            )
    heat_map(map_file, data)

if __name__ == '__main__':
    main()
