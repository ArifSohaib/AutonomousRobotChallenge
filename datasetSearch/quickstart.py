import requests 
from PIL import Image
import matplotlib.pyplot as plt 
from io import BytesIO


def show(thumbnail_urls):
    
    f,axis = plt.subplots(4,4)
    for i in range(4):
        for j in range(4):
            image_data = requests.get(thumbnail_urls[i+4*j])
            image_data.raise_for_status()
            image = Image.open(BytesIO(image_data.content))
            axis[i][j].imshow(image)
            axis[i][j].axis('off')
    plt.show()

if __name__ == "__main__":
    subscription_key = 'df4f1dd5672b44c3876ea0edf55463cd'
    assert subscription_key 
    headers = {"Ocp-Apim-Subscription-Key":subscription_key}
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
    search_term = "phytophthora"
    params = {"q":search_term, "license":"public", "imageType":"photo"}
    response = requests.get(search_url, headers=headers,params=params)
    response.raise_for_status()
    search_results = response.json()

    thumbnail_urls = [img["thumbnailUrl"] for img in search_results["value"][:16]]
    num_results = len(search_results["value"])
    print("returned {} results".format(num_results))
    if num_results >= 16:
        show(thumbnail_urls)