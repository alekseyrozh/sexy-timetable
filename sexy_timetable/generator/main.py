#!/usr/bin/env python3
from PIL import Image
from sexy_timetable.generator import imagesResizer as resizer
from sexy_timetable.generator import timetablePreparer as prep
# import sexy_timetable.generator.getTimetable
from sexy_timetable.generator import imageCombiner

# from  import imagesResizer

PIC_TYPE = "girl"
# timetable = Image.open("screenshot.png")
# timetable = getTimetable.get_timetable()


def generate_cool_timetable(plain_timetable):

    timetable = plain_timetable
    cutted_timetable = prep.cut_timetable_for_the_correct_size(timetable)

    # for choice_of_back in range(6,len([name for name in os.listdir('pictures') if os.path.isfile(os.path.join('pictures', name))]) - 1):
    # for choice_of_back in range(1, 19):
    for choice_of_back in range(1, 2):
        print(choice_of_back)
        background = 0
        try:
            background = Image.open("static/pictures/" + PIC_TYPE + "s_for_app/" + PIC_TYPE + "_" + str(choice_of_back) + ".jpg")
        except:
            try:
                background = Image.open(
                    "static/pictures/" + PIC_TYPE + "s_for_app/" + PIC_TYPE + "_" + str(choice_of_back) + ".jpeg")
            except:
                background = Image.open(
                    "static/pictures/" + PIC_TYPE + "s_for_app/" + PIC_TYPE + "_" + str(choice_of_back) + ".png")

        background, resized_timetable = resizer.resize_back_time(background, cutted_timetable)

        # new_timetable = Image.blend(background, prepared_timetable, alpha=0.5)
        clear_timetable = prep.remove_white_back(resized_timetable)
        new_timetable = imageCombiner.add_timetable_with_background(background, clear_timetable)

        return new_timetable

        # new_timetable.save("new_timetables/girls/timetable_" + str(choice_of_back) + ".png")
