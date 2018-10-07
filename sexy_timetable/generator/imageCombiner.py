from copy import deepcopy
from PIL import Image


def combine_pixs(pix_a, pix_b, val_a):
    return int(pix_a[0] * val_a + pix_b[0] * (1 - val_a)), int(pix_a[1] * val_a + pix_b[1] * (1 - val_a)), int(pix_a[2] * val_a + pix_b[2] * (1 - val_a)), 255


def add_timetable_with_background(background, timetable):
    timetable = timetable.convert("RGBA")
    background = background.convert("RGBA")

    pix_time = timetable.load()

    width_offset = int(background.size[0] / 2 - timetable.size[0] / 2)
    pix_back = background.load()

    for i in range(timetable.size[0]):
        for j in range(timetable.size[1]):
            if pix_time[i, j][3] == 0:
                pix_time[i, j] = pix_back[i + width_offset, j]
            else:
                pix_time[i, j] = combine_pixs(pix_time[i, j], pix_back[i + width_offset, j], 0.7)

    return timetable
