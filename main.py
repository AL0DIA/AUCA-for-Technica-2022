from utils import *

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
