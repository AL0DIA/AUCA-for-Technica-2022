import requests
import urllib.request
from PIL import Image


def generate_box_art(art_description, box_number):
    request_name = 'reqArt' + box_number
    response_name = 'getArt' + box_number
    url_name = 'artBox' + box_number
    output_name = 'comicBox' + box_number + '.png'
    comic_box_name = 'box' + box_number

    request_name = requests.post(
        "https://api.deepai.org/api/text2img",
        data={
            'text': art_description,
        },
        headers={'api-key': 'df27bb07-656a-4446-8ce6-c3dc50f387a6'}
    )

    response_name = request_name.json()
    url_name = response_name["output_url"]
    urllib.request.urlretrieve(url_name, output_name)
    comic_box_name = Image.open(output_name)
    comic_box_name.show()


if __name__ == '__main__':

    artDescription = 'cats sharing a pizza on a cozy room'
    boxNum = '6'

    generate_box_art(artDescription, boxNum)


    
    

    def get_num_boxes():
        try:
            num_boxes = input("How many boxes do you want on your comic strip (max. 6)? ")

            if (num_boxes > 6 or num_boxes < 1):
                raise Exception() 
            return num_boxes

        except:
            print("\n Please, choose a valid number!")


