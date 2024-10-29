from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def backup_database(file_path):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    file = drive.CreateFile({'title': 'inventory_backup.sqlite'})
    file.SetContentFile(file_path)
    file.Upload()
