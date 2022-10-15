import requests


if __name__ == '__main__':

    genArt1 = requests.post(
        "https://api.deepai.org/api/text2img",
        data={
            'text': 'cute cat fighting against dinosaurs',
        },
        headers={'api-key': 'df27bb07-656a-4446-8ce6-c3dc50f387a6'}
    )
    print(genArt1.json())
    art1 = genArt1.json()
    print(art1["output_url"])

