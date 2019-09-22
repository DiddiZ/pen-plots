"""
This module concerns converting strokes to gcode.
"""


def write_gcode(
    writer,
    strokes,
    offset,
    z_hop=2,
    feedrate_draw=1800,
    feedrate_travel=3600,
    feedrate_z_hop=300,
    start_gcode='G28\nG21\n',
    end_gcode='G28 X0 Y0\n',
):
    """
    Converts strokes to gcode.

    Parameters
    ----------
    writer : writable
        Openend output file.
    strokes : list of strokes
        Strokes to be plotted.
    offset : array_like (2,)
        Offset to be applied to all points. Useful for positioning the drawn image on the paper.
    z_hop : mm
        z-hop distance.
    feedrate_draw/feedrate_travel/feedrate_z_hop : mm/min
        feedrates used for drawing.
    start_gcode/end_gcode : str
        instruction to set up and clean up the plotter.
    """
    # Write start
    if start_gcode is not None:
        writer.write(start_gcode)
        if start_gcode[-1] != '\n':
            writer.write('\n')

    # Write strokes
    for stroke in strokes:
        # Move to start
        writer.write(
            'G0 F%d X%.03f Y%.03f Z%.03f\n' %
            (feedrate_travel, offset[0] + stroke[0][0], offset[1] + stroke[0][1], z_hop)
        )
        # Pen down
        writer.write('G0 F%d Z%.03f\n' % (feedrate_z_hop, 0))

        # Draw lines
        for i in range(1, len(stroke)):
            writer.write('G0 F%d X%.03f Y%.03f\n' % (feedrate_draw, offset[0] + stroke[i][0], offset[1] + stroke[i][1]))

        # Pen up
        writer.write('G0 F%d Z%.03f\n' % (feedrate_z_hop, z_hop))

    # Write end
    if end_gcode is not None:
        writer.write(end_gcode)
        if start_gcode[-1] != '\n':
            writer.write('\n')
