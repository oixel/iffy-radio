from google_images_search import GoogleImagesSearch

img_search = GoogleImagesSearch('AIzaSyAUUX4kOOfgVPKgiTLHCRvMFtNlh5A8vVA', 'e438e2cccb581489e')

_search_params = {
    'num': 1,
    'fileType': 'png',
    'imgColorType': 'color' ##
}

def download_cover(album_name):
    _search_params['q'] = album_name + " album art"

    # Searches...
    img_search.search(search_params=_search_params, custom_image_name=album_name)
    for image in img_search.results():
        
        image.url  # image direct url
        image.referrer_url  # image referrer url (source) 
        
        image.download('album_covers/')  # download image
        image.resize(500, 500)  # resize downloaded image

        image.path  # downloaded local file path

#ab = input("What is album name? ")
#download_cover(ab)

download_cover("the rise and fall of a midwestern princess")