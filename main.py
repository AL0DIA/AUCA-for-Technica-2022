import requests
import urllib.request
from PIL import Image, ImageDraw, ImageFont
import os


def generate_box_art(art_description, box_number):
    deepai_api_key = os.getenv('deepaiapi')

    output_name = 'comicBox' + str(box_number) + '.png'

    print("generating art... please wait :)")

    request = requests.post(
        "https://api.deepai.org/api/text2img",
        data={
            'text': art_description,
        },
        headers={'api-key': deepai_api_key}
    )

    response = request.json()
    url = response["output_url"]
    urllib.request.urlretrieve(url, output_name)


def get_num_boxes():
    valid_option = False
    while not valid_option:
        try:
            num_boxes: int = int(input("How many boxes do you want on your comic strip (max. 6)? "))
            if num_boxes > 6 or num_boxes < 1:
                raise Exception()
            else:
                valid_option = True
                return num_boxes

        except:
            print("\nPlease, choose a valid number!\n")


def add_text(comic_box):
    option = "0"
    colors = {1: (255, 128, 0), 2: (0, 204, 0), 3: (255, 255, 255),
              4: (0, 204, 204), 5: (153, 51, 255)}
    while option != "1" or option != "2":
        try:
            option = input("Do you want to add text to comic box num. "+str(comic_box)+"?\n 1. Yes\n 2. No\n ")
            if option == "1":
                valid_color_option = False
                while not valid_color_option:
                    try:
                        color_option: int = int(input("Choose the color of the text\n 1. Orange\n 2. Green\n"
                                             " 3. White\n 4. Blue\n 5. Purple\n "))
                        if color_option > 6 or color_option < 1:
                            raise Exception()
                        else:
                            color = colors.get(color_option)
                            valid_color_option = True

                    except:
                        print("\nPlease, enter a valid number!\n")

                image = Image.open("comicBox" + str(comic_box) + ".png")
                x0, y0 = 0, 1024
                h, w = 190, 1024
                shape = ((x0, y0), (x0 + w, y0 - h))
                my_font = ImageFont.truetype("Cascadia.ttf", 47)
                full_text = ""
                line = 1
                while line < 4:
                    print("\nYou can enter max 3 lines of 33 char each."
                          "\nIf you enter more, they will be cropped out :(\n")
                    box_text = input("Write the text of line "+str(line)+": ")[:33]
                    full_text = full_text + box_text + "\n"
                    line += 1

                overlay = Image.new("RGBA", image.size, (0, 0, 0) + (0,))
                overlay_draw = ImageDraw.Draw(overlay)
                overlay_draw.rectangle(shape, fill=(0, 0, 0) + (int(255 * 0.9),), outline="black")
                overlay_draw.text((x0 + 50, y0 - 175), full_text, font=my_font, fill=(color))
                image = image.convert("RGBA")
                image = Image.alpha_composite(image, overlay)
                image.save("comicBox"+str(comic_box)+".png")
                break
            elif option == "2":
                break
            elif option != "1" or option != "2":
                raise Exception()

        except:
            print("\nPlease, choose option 1 or 2!\n")


def save_comic(full_comic):
    option = "0"
    while option != "1" or option != "2":
        try:
            option = input("Do you want to save this comic?\n 1. Yes\n 2. No\n ")
            if option == "1":
                name = input("Write your comic name: ")
                full_comic.save(name+".png")
                print("Your comic is saved")
                break
            elif option == "2":
                print("Your comic is forever lost :(")
                break
            elif option != "1" or option != "2":
                raise Exception()

        except:
            print("\nPlease, choose option 1 or 2!\n")


def initiate_comic(number_boxes):
    if number_boxes == 1:
        return Image.new("RGBA", (1024, 1024))
    elif number_boxes == 2:
        return Image.new("RGBA", (2048, 1024))
    elif number_boxes == 3:
        return Image.new("RGBA", (3072, 1024))
    elif number_boxes == 4:
        return Image.new("RGBA", (2048, 2048))
    elif number_boxes == 5:
        return Image.new("RGBA", (5120, 1024))
    else:
        return Image.new("RGBA", (3072, 2048))


class EvenComicConstructor:

    def __init__(self, number_boxes, full_comic, comic_dictionary):
        self.number_boxes = number_boxes
        self.full_comic = full_comic
        self.comic_dictionary = comic_dictionary

    def first_row(self, first_box, last_box):
        coord = 0
        index = first_box
        while index <= last_box:
            self.full_comic.paste(self.comic_dictionary["box" + str(index)], (coord, 0))
            coord += 1024
            index += 1
        return self.full_comic

    def second_row(self, first_box, last_box):
        coord = 0
        index = first_box
        while index <= last_box:
            self.full_comic.paste(self.comic_dictionary["box" + str(index)], (coord, 1024))
            coord += 1024
            index += 1
        return self.full_comic

    @classmethod
    def build_comic(cls, number_boxes, full_comic, comic_dictionary):
        comic_constructor = cls(number_boxes, full_comic, comic_dictionary)
        if number_boxes == 2:
            return comic_constructor.first_row(1, 2)

        elif number_boxes == 4:
            comic_constructor.first_row(1, 2)
            comic_constructor.second_row(3, 4)
            return full_comic

        else:
            comic_constructor.first_row(1, 3)
            comic_constructor.second_row(4, 6)
            return full_comic


def odd_comic_constructor(number_boxes, full_comic, comic_dictionary):
    coord = 0
    if number_boxes > 1:
        for box in range(1, number_boxes+1, 1):
            full_comic.paste(comic_dictionary["box" + str(box)], (coord, 0))
            coord += 1024
    full_comic.paste(comic_dictionary["box"+str(number_boxes)], (coord, 0))
    return full_comic


if __name__ == '__main__':

    box_qty = get_num_boxes()

    box_num = 1
    while box_num <= box_qty:
        description = input("Describe what do you want to appear in comic box num. " + str(box_num) + ": ")
        generate_box_art(description, box_num)
        add_text(box_num)
        box_num += 1
        print("\n")

    comic_boxes_dict = {}
    box_id = 1
    for each_box in enumerate(range(box_qty)):
        comic_boxes_dict["box{}".format(box_id)] = Image.open("comicBox" + str(box_id) + ".png")
        box_id += 1

    comic = initiate_comic(box_qty)
    if box_qty % 2 != 0:
        odd_comic_constructor(box_qty, comic, comic_boxes_dict)
        comic.show("Here's your comic:")
        save_comic(comic)
    else:
        EvenComicConstructor.build_comic(box_qty, comic, comic_boxes_dict)
        comic.show("Here's your comic:")
        save_comic(comic)