import requests
import urllib.request
from PIL import Image

if __name__ == '__main__':

    genArt1 = requests.post(
        "https://api.deepai.org/api/text2img",
        data={
            'text': 'cute cat fighting against capitalism',
        },
        headers={'api-key': 'df27bb07-656a-4446-8ce6-c3dc50f387a6'}
    )
    art1 = genArt1.json()
    art1URL = art1["output_url"]

    urllib.request.urlretrieve(art1URL, "art1.png")
    img1 = Image.open("art1.png")
    img1.show()


    
    

    def get_num_boxes():
        try:
            num_boxes = input("How many boxes do you want on your comic strip (max. 6)? ")

            if (num_boxes > 6 or num_boxes < 1):
                raise Exception() 
            return num_boxes

        except:
            print("\n Please, choose a valid number!")


