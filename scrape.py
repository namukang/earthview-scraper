import sys
import json
import requests


seen_photos = {}
url = 'https://earthview.withgoogle.com/_api/polanczyk-poland-5484.json'
count = 0


def scrape():
    # The API seems to link the images in a loop, so we can stop once we see an
    # image we have already seen.
    global url
    seen_photos[url] = True

    page = requests.get(url)
    photo_json = page.json()

    photo = {
        "id": photo_json['id'],
        "earthLink": photo_json['earthLink'],
    }
    if 'country' in photo_json:
        photo['country'] = photo_json['country']
    if 'region' in photo_json:
        photo['region'] = photo_json['region']

    url = 'https://earthview.withgoogle.com/_api/' + \
        photo_json['nextSlug'] + '.json'
    return photo


if __name__ == "__main__":
    with open('earthview.json', 'w+') as f:
        f.write('[')
        while True:
            if url in seen_photos:
                break
            photo_json = json.dumps(scrape())
            print(count)
            print(photo_json)
            f.write(photo_json)
            f.write(',')  # remove last comma before using file for proper JSON
            count += 1
        f.write(']')
