from PIL import Image
import phoneInfo as phone


def resize_back_time(background, timetable):
    background = background.resize(
        (int((phone.SCREEN_HEIGHT / background.size[1]) * background.size[0]), phone.SCREEN_HEIGHT),
        Image.ANTIALIAS)

    if background.size[0] > phone.SCREEN_WIDTH:
        shift = int((background.size[0] - phone.SCREEN_WIDTH) / 2)
        background = background.crop((shift, 0, background.size[0] - shift, background.size[1]))
    elif background.size[0] < phone.SCREEN_WIDTH:
        background = background.resize(
            (phone.SCREEN_WIDTH, int((phone.SCREEN_WIDTH / background.size[0]) * background.size[1])),
            Image.ANTIALIAS)
        shift = int((background.size[1] - phone.SCREEN_HEIGHT) / 2)
        background = background.crop((0, shift, background.size[0], background.size[1] - shift))

    background = background.resize((phone.SCREEN_WIDTH, phone.SCREEN_HEIGHT), Image.ANTIALIAS)
    img1 = Image.new('RGB', size=(phone.SCREEN_WIDTH, phone.SCREEN_HEIGHT), color=(255, 255, 255))
    img1.paste(background, (0, 0))

    timetable = timetable.resize((phone.SCREEN_WIDTH, phone.SCREEN_HEIGHT), Image.ANTIALIAS)
    img2 = Image.new('RGB', size=(phone.SCREEN_WIDTH, phone.SCREEN_HEIGHT), color=(255, 255, 255))
    img2.paste(timetable, (0, 0))

    return img1, img2
