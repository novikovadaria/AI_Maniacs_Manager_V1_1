from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

class YouTubeService:
    def __init__(self, client_secrets_file, scopes):
        self.client_secrets_file = client_secrets_file
        self.scopes = scopes
        self.youtube = None

    def authenticate(self):

        if not os.path.exists(self.client_secrets_file):
            raise FileNotFoundError(f"Client secrets file not found: {self.client_secrets_file}")

        flow = InstalledAppFlow.from_client_secrets_file(self.client_secrets_file, self.scopes)
        credentials = flow.run_local_server(port=0)
        self.youtube = build("youtube", "v3", credentials=credentials)

        return self.youtube

    def get_service(self):
        
        if self.youtube is None:
            self.authenticate()
        return self.youtube


class Video:
    def __init__(self, categoryId, title, description, privacyStatus, path):
        self.categoryId = categoryId
        self.title = title
        self.description = description
        self.privacyStatus = privacyStatus
        self.path = path

class VideoUploader:
    def __init__(self, youtube_service, video):

        self.youtube_service = youtube_service
        self.video = video

    def upload_video(self):

        upload_body = {
            'snippet': {
                'categoryId': self.video.categoryId,
                'title': self.video.title,
                'description': self.video.description
            },
            'status': {
                'privacyStatus': self.video.privacyStatus
            }
        }

        media = MediaFileUpload(self.video.path, chunksize=-1, resumable=True)
        response_upload = self.youtube_service.videos().insert(
            part='snippet,status',
            body=upload_body,
            media_body=media
        ).execute()

        return response_upload
