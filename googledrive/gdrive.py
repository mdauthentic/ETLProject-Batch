from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pathlib import Path


class GoogleDriveAPI:
    def __init__(self) -> None:
        self.drive = self.__auth()

    def __auth(self) -> GoogleDrive:
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        return GoogleDrive(gauth)

    def create_folder(self, parent_folder_id: str, subfolder_name: str):
        new_folder = self.drive.CreateFile(
            {
                "title": subfolder_name,
                "parents": [{"kind": "drive#fileLink", "id": parent_folder_id}],
                "mimeType": "application/vnd.google-apps.folder",
            }
        )
        new_folder.Upload()
        return new_folder

    def upload_file(self, dir: str):
        basepath = Path(dir)
        for x in basepath.iterdir():
            if x.is_file():
                f = self.drive.CreateFile({"title": x})
                f.SetContentFile(x)
                f.Upload()
