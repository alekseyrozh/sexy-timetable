"""Prepares screenshot of timetable to be of correct size and transparency"""
import sexy_timetable.generator.phoneInfo as phone

from PIL import Image


def average_pix(pixelInRGBA):
    return float(pixelInRGBA[0] + pixelInRGBA[1] + pixelInRGBA[2]) / 3.0


def is_white(pix):
    return average_pix(pix) == 255


def add_white_pix(pix, x, y):
    if x < 0 or y < 0 or x >= phone.SCREEN_WIDTH or y >= phone.SCREEN_HEIGHT:
        return 0

    if is_white(pix[x, y]):
        return 1

    return 0


def count_white_pix(pix, i, j):
    num = 0

    for k in range(-2, 3):
        for l in range(-2, 3):
            num = num + add_white_pix(pix, i + k, j + l)

    return num


def count_crised(pix, x, y):
    num = 0
    for i in range(-3, 4):
        num = num + add_white_pix(pix, x + i, y)
        num = num + add_white_pix(pix, x, y + i)
    return num


def remove_white_back(img):
    img = img.convert("RGBA")
    pix = img.load()

    for i in range(1, img.size[0]):
        for j in range(1, img.size[1]):
            # if count_white_pix(pix, i, j)  >= 9:
            if count_crised(pix, i, j) > 6:
                pix[i, j] = (255, 255, 255, 0)

    return img


def cut_by_subjects(timetable):
    last = 0
    pix = timetable.load()
    column = timetable.size[0]-1

    while column > 6 and last == 0:
        num_of__wite = 0
        for i in range(5):
            for j in range(timetable.size[1]):
                if average_pix(pix[column - i, j]) == 255:
                    num_of__wite = num_of__wite + 1

        # print(float(num_of__wite) / float(timetable.size[1] * 5))
        if float(num_of__wite) / float(timetable.size[1] * 5) < 0.70:
            last = column
        column = column - 1

    return timetable.crop((0, 0, last + 5, timetable.size[1]))


def cut_timetable_for_the_correct_size(timetable):
    pix = timetable.load()
    found_width = False
    column, first_width, last_width = 0, 0, 0

    while not found_width:
        num_black_pixels = 0
        for i in range(timetable.size[0]):
            if average_pix(pix[i, column]) < 1:
                num_black_pixels = num_black_pixels + 1

        if float(num_black_pixels) / float(timetable.size[0]) > 0.9:
            found_width = True
            first_width = 0
            while average_pix(pix[first_width, column]) > 1:
                first_width = first_width + 1

            last_width = timetable.size[0] - 1
            while average_pix(pix[last_width, column]) > 1:
                last_width = last_width - 1
        column = column + 1

    found_height = False
    row, first_height, last_height = 0, 0, 0

    while not found_height:
        num_black_pixels = 0
        for i in range(timetable.size[1]):
            if average_pix(pix[row, i]) < 1:
                num_black_pixels = num_black_pixels + 1

        if float(num_black_pixels) / float(timetable.size[0]) > 0.9:
            found_height = True
            first_height = 0
            while average_pix(pix[row, first_height]) > 1:
                first_height = first_height + 1

            last_height = timetable.size[1] - 1
            while average_pix(pix[row, last_height]) > 1:
                last_height = last_height - 1
        row = row + 1

    timetable = timetable.crop((first_width, first_height, last_width, last_height))
    return cut_by_subjects(timetable)


def prepare_timetable(timetable):
    timetable = cut_timetable_for_the_correct_size(timetable)
    return timetable
