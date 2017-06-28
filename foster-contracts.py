from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from datetime import date, timedelta

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_drive_files():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    # get yesterday's date (actually day before yesterday)
    yesterday = date.today() - timedelta(2)
    yesterday_date = yesterday.strftime('%Y-%m-%dT00:00:00')

    results = service.files().list(
        q="modifiedTime >= '%s'" % yesterday_date, supportsTeamDrives='true', includeTeamDriveItems='true', corpora='teamDrive',
        teamDriveId='0AJBuyjEDVhtZUk9PVA', pageSize=30, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    with open('drive_files.txt', 'w') as drive_file:
        if not items:
            print('No files found.')
            drive_file.write('0')
        else:
            print('Files:')
            drive_file.write('%s\n' % len(items))
            for item in items:
                print('{0} ({1})'.format(item['name'], item['id']))
                drive_file.write(item['name'] + '(' + item['id'] + ')\n')

if __name__ == '__main__':
    get_drive_files()
