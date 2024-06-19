import requests

# Takes in image source URL and downloads it at parameterized path
def download_image(url, path) -> None:
    image_data = requests.get(url).content
    open(path, "wb").write(image_data)