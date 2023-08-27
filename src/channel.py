from googleapiclient.discovery import build
import json
import os


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API."""

        api_key: str = os.getenv('API_KEY')
        # создан специальный объект для работы с API
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.youtube = youtube
        self.__channel_id = channel_id
        # получаем данные о канале
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        channel_list = channel["items"]
        for item in channel_list:
            self.title = item['snippet']['title']
            self.description = item['snippet']['description']
            self.url = 'https://www.youtube.com/channel/' + self.__channel_id
            self.subscriber = item['statistics']['subscriberCount']
            self.video_count = item['statistics']['viewCount']
            self.view_count = item['statistics']['videoCount']

    """
    Реализуем сложение, вычитание и сравнение подписчиков двух YouTube каналов
    """
    def __str__(self):
        return str(f'{self.title} ({self.url})')

    def __add__(self, other):
        return int(self.subscriber) + int(other.subscriber)

    def __sub__(self, other):
        return int(self.subscriber) - int(other.subscriber)

    def __gt__(self, other):
        return int(self.subscriber) > int(other.subscriber)

    def __ge__(self, other):
        return int(self.subscriber) >= int(other.subscriber)

    @property
    def channel_id(self):
        """
        Возвращает приватное имя канала
        """
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """
        Возвращаюет объект для работы с YouTube API
        """
        api_key: str = os.getenv('API_KEY')
        # создан специальный объект для работы с API
        youtube_new = build('youtube', 'v3', developerKey=api_key)
        return youtube_new


    def to_json(self, name_dict):
        """
        Получает имя файла json и создает файл со значениями атрибутов экземпляра `Channel`
        """
        self.name_dict = name_dict
        name_dict = {
            'channel_id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber': self.subscriber,
            'video_count': self.video_count,
            'view_count': self.view_count,
        }

        print(json.dumps(name_dict, ensure_ascii=False, indent=4))

        with open(self.name_dict, 'w') as file:
            json.dump(name_dict, file)
