from googleapiclient.discovery import build
import json
import os


class Video:
    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео.
        Дальше все данные будут подтягиваться по API."""

        api_key: str = os.getenv('API_KEY')
        # создан специальный объект для работы с API
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.__video_id = video_id
        # получаем данные о канале
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        # printj(video_response)
        video_title: str = video_response['items'][0]['snippet']['title']
        view_count: int = video_response['items'][0]['statistics']['viewCount']
        like_count: int = video_response['items'][0]['statistics']['likeCount']

        self.video_title = video_title
        self.view_count = view_count
        self.like_count = like_count
        self.url = 'https://www.youtube.com//watch?v=' + self.__video_id

    def __str__(self):
        """
        Выводит название видео
        """
        return self.video_title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        """
        Экземпляр инициализируется id видео и id плейлиста
        """
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        """
        Выводит название видео
        """
        return self.video_title