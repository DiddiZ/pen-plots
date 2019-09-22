import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from pen_plots.strokes import bounding_box


class LineDataUnits(Line2D):
    """
    Line with linewidth in data units.

    Taken from https://stackoverflow.com/a/42972469/1212813
    """

    def __init__(self, *args, **kwargs):
        _lw_data = kwargs.pop("linewidth", 1)
        super().__init__(*args, **kwargs)
        self._lw_data = _lw_data

    def _get_lw(self):
        if self.axes is not None:
            ppd = 72. / self.axes.figure.dpi
            trans = self.axes.transData.transform
            return ((trans((1, self._lw_data)) - trans((0, 0))) * ppd)[1]
        else:
            return 1

    def _set_lw(self, lw):
        self._lw_data = lw

    _linewidth = property(_get_lw, _set_lw)


def show_strokes(strokes, pen_width=0.32, show_travel=False):
    """
    Renders strokes in matplotlib and shows them.
    """
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    for i, stroke in enumerate(strokes):
        ax1.add_line(
            LineDataUnits(
                stroke[:, 0],
                stroke[:, 1],
                linewidth=pen_width,
                solid_capstyle="round",
                solid_joinstyle="round",
                c='black',
            )
        )
        if show_travel and i > 0:
            ax1.add_line(
                LineDataUnits(
                    [strokes[i - 1][-1, 0], stroke[0, 0]],
                    [strokes[i - 1][-1, 1], stroke[0, 1]],
                    linewidth=pen_width / 2,
                    c='blue',
                )
            )

    bbox = bounding_box(strokes)
    ax1.set_xlim(bbox[:, 0] + [-pen_width * 3, pen_width * 3])
    ax1.set_ylim(bbox[:, 1] + [-pen_width * 3, pen_width * 3])
    ax1.set_aspect('equal')

    plt.xticks([])
    plt.yticks([])
    plt.show()
    plt.close(fig)
