import requests
import urllib.request
from PIL import Image
#import os


def generate_box_art(art_description, box_number):
    #deepai = os.getenv('deepaiapi')

    output_name = 'comicBox' + str(box_number) + '.png'

    print("generating art... please wait :)")

    request = requests.post(
        "https://api.deepai.org/api/text2img",
        data={
            'text': art_description,
        },
        headers={'api-key': 'df27bb07-656a-4446-8ce6-c3dc50f387a6'}
    )

    response = request.json()
    url = response["output_url"]
    urllib.request.urlretrieve(url, output_name)


def get_num_boxes():
    try:
        num_boxes: int = int(input("How many boxes do you want on your comic strip (max. 6)? "))

        if num_boxes > 6 or num_boxes < 1:
            raise Exception()
        return num_boxes

    except:
        print("\n Please, choose a valid number!")


def save_comic(full_comic):
    try:
        option = input("Do you want to save this comic?\n 1. Yes\n 2. No\n ")
        if option == "1":
            name = input("Write your comic name: ")
            full_comic.save(name+".png")
            print("Your comic is saved")
        elif option == "2":
            print("Your comic is forever lost :(")
        elif option != "1" or option != "2":
            raise Exception()

    except:
        print("\n Please, choose option 1 or 2!")


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


def even_comic_constructor(number_boxes, full_comic, comic_dictionary):
    def first_row(first_box, last_box, full, comic_dict):
        coord = 0
        index = first_box
        while index <= last_box:
            full.paste(comic_dict["box" + str(index)], (coord, 0))
            coord += 1024
            index += 1
        return full

    def second_row(first_box, last_box, full, comic_dict):
        coord = 0
        index = first_box
        while index <= last_box:
            full.paste(comic_dict["box" + str(index)], (coord, 1024))
            coord += 1024
            index += 1
        return full

    if number_boxes == 2:
        return first_row(1, 2, full_comic, comic_dictionary)

    elif number_boxes == 4:
        first_row(1, 2, full_comic, comic_dictionary)
        second_row(3, 4, full_comic, comic_dictionary)
        return full_comic

    else:
        first_row(1, 3, full_comic, comic_dictionary)
        second_row(4, 6, full_comic, comic_dictionary)
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

    #box_num = 1
    #while box_num <= box_qty:
    #    description = input("Describe what do you want to appear in comic box num. " + str(box_num) + ": ")
    #    generate_box_art(description, box_num)
    #    box_num += 1

    comic_boxes_dict = {}
    box_id = 1
    for each_box in enumerate(range(box_qty)):
        comic_boxes_dict["box{}".format(box_id)] = Image.open("comicBox" + str(box_id) + ".png")
        box_id += 1

    comic = initiate_comic(box_qty)
    if box_qty % 2 != 0:
        odd_comic_constructor(box_qty, comic, comic_boxes_dict)
        save_comic(comic)
    else:
        even_comic_constructor(box_qty, comic, comic_boxes_dict)
        save_comic(comic)