from googleapiclient.discovery import build
import os

# Replace with your own API key
YOUTUBE_API_KEY = 'AIzaSyBkFWSAz7LkcusEsOTzkbzegWBy8bPIl4o'

def get_youtube_categories(api_key, region_code='IN'):
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Call the API to get video categories
    request = youtube.videoCategories().list(
        part="snippet",
        regionCode=region_code
    )
    response = request.execute()

    categories = []
    for item in response.get('items', []):
        category = {
            "category_id": item['id'],
            "title": item['snippet']['title']
        }
        categories.append(category)

    return categories

if __name__ == "__main__":
    categories = get_youtube_categories(YOUTUBE_API_KEY)
    for category in categories:
        print(f"Category ID: {category['category_id']}, Title: {category['title']}")
