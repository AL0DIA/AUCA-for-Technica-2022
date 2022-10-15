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

