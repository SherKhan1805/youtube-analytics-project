from functools import reduce
import operator
import isodate
from googleapiclient.discovery import build
import os


class PlayList:

    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id

        """
        Получаем данные по плейлисту в формате json
        """
        api_key: str = os.getenv('API_KEY')
        # создан специальный объект для работы с API
        youtube = build('youtube', 'v3', developerKey=api_key)
        playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                                       part='snippet, contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        """
        Получаем имя плейлиста
        """
        for playlist in playlist_videos['items']:
            title = playlist['snippet']['title'].split('.')
            self.title = title[0]

        self.playlist_videos = playlist_videos

        """
        Получаем информацию по видео плейлиста в формате json
        """
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()

        """
        Получаем время всех видео на канале и получаем общую сумму их времени
        """
        videos_time_list = []
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            videos_time_list.append(duration)

        total_time = reduce(operator.add, videos_time_list)

        self.total_time = total_time

        """
        Получаем ссылку на самое популярное видео
        """
        video_likes_dict = {}

        for video in video_response['items']:
            key = int(video['statistics']['likeCount'])
            value = video['id']
            new_dict = {key: value}
            video_likes_dict.update(new_dict)

        a = sorted(video_likes_dict)[-1]

        for key, value in video_likes_dict.items():
            if key == a:
                self.url_video = "https://youtu.be/" + value


    @property
    def total_duration(self):
        """
        Возвращает объект класса datetime.timedelta с суммарной длительность плейлиста
        """

        return self.total_time

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео
        """
        return self.url_video

