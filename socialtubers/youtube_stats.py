import requests
import json
from tqdm import tqdm
import re

class YTstats:
    def __init__(self, api_key, channel_id):
        self.api_key = api_key
        self.channel_id = channel_id
        self.channel_statistics = None
        self.video_data = None

    def get_channel_statistics(self):
        url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}"
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data["items"][0]["statistics"]
        except:
            data = None

        self.channel_statistics = data
        return data

    def get_channel_video_data(self):
        # Fetch video ids, ensuring we only get exactly 10 long videos
        filtered_videos = {}
        fetched_videos = 0
        next_page_token = None

        while fetched_videos < 10:  # Fetch more if we don't have 10 yet
            channel_videos, next_page_token = self._get_channel_videos(limit=10, page_token=next_page_token)
            if not channel_videos:
                break  # No more videos to fetch

            parts = ["snippet", "statistics", "contentDetails"]
            for video_id in tqdm(channel_videos):
                video_info = {}
                for part in parts:
                    data = self._get_single_video_data(video_id, part)
                    video_info.update({part: data})

                # Check if the video is longer than 60 seconds (i.e., not a Short)
                duration = video_info.get('contentDetails', {}).get('duration', '')
                if self._is_short(duration):
                    continue  # Skip Shorts

                filtered_videos[video_id] = video_info
                fetched_videos += 1

                if fetched_videos == 10:
                    break  # Stop once we have 10 long videos

            if not next_page_token or fetched_videos == 10:
                break  # Stop fetching more pages if we reached 10 videos

        self.video_data = filtered_videos
        print(f"****** FILTERED CHANNEL VIDEOS: {len(filtered_videos)} videos ******")
        return filtered_videos

    def _is_short(self, duration):
        match = re.match(r'PT(?:(\d+)M)?(?:(\d+)S)?', duration)
        if not match:
            return False  # Assume not a short if format is unexpected
        
        minutes = int(match.group(1)) if match.group(1) else 0
        seconds = int(match.group(2)) if match.group(2) else 0
        
        total_seconds = minutes * 60 + seconds
        return total_seconds < 60

    def _get_single_video_data(self, video_id, part):
        url = f"https://www.googleapis.com/youtube/v3/videos?part={part}&id={video_id}&key={self.api_key}"
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data["items"][0][part]
        except:
            print("ERROR")
            data = dict()
        return data

    def _get_channel_videos(self, limit=None, page_token=None):
        url = f"https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=id&order=date"

        if limit is not None and isinstance(limit, int):
            url += "&maxResults=" + str(limit)
        if page_token:
            url += "&pageToken=" + page_token

        vid, npt = self._get_channel_videos_per_page(url)
        return vid, npt

    def _get_channel_videos_per_page(self, url):
        json_url = requests.get(url)
        data = json.loads(json_url.text)

        channel_videos = dict()
        if "items" not in data:
            return channel_videos, None

        item_data = data["items"]
        nextPageToken = data.get("nextPageToken", None)
        for item in item_data:
            try:
                kind = item["id"]["kind"]
                if kind == "youtube#video":
                    video_id = item["id"]["videoId"]
                    channel_videos[video_id] = dict()
            except KeyError:
                print(" ERROR ")

        return channel_videos, nextPageToken
