import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload

from odoo import http
from odoo.http import request, Response
from odoo.modules.module import get_module_resource

# Define the auth scopes to request.
scopes = ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/drive.file']
KEY_FILE_NAME = 'KEY_FILE_NAME.json'
key_file_location = get_module_resource('odoo_googledrive_files', 'static/files/', KEY_FILE_NAME)


def get_service(api_name, api_version):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.

    Returns:
        A service that is connected to the specified API.
    """

    credentials = service_account.Credentials.from_service_account_file(key_file_location)
    scoped_credentials = credentials.with_scopes(scopes)

    # Build the service object.
    service = build(api_name, api_version, credentials=scoped_credentials)

    return service


class GoogleDriveController(http.Controller):
    @http.route('/api/v1/upload-file', type='http', auth='user', methods=['POST'], csrf=False, cors="*")
    def upload_file(self, **kwargs):
        try:
            # Authenticate and construct service.
            service = get_service(
                api_name='drive',
                api_version='v3'
            )
            uploaded_file = request.httprequest.files.get('file')
            if not uploaded_file:
                return Response(
                    json.dumps(
                        {'success': False, 'error': 'No file found with.'}, indent=4,
                        sort_keys=False,
                        default=str
                    ),
                    content_type='application/json;charset=utf-8',
                    status=204
                )

            content_type = uploaded_file.content_type
            filename = uploaded_file.filename
            file_metadata = {'name': filename, 'mimeType': content_type, 'visibility': 'public'}

            media = MediaIoBaseUpload(uploaded_file, mimetype=content_type)

            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name'
            ).execute()

            permission = {
                'type': 'anyone',
                'role': 'reader'
            }
            service.permissions().create(fileId=file.get('id'), body=permission).execute()

            file_name = file.get('name')
            file_id = file.get('id')
            download_url = "https://drive.google.com/uc?id=%s&export=download" % file.get('id')

            return Response(
                json.dumps(
                    {
                        'success': True,
                        'result': {
                            'id': file_id,
                            'file_name': file_name,
                            'download_url': download_url
                        }
                    },
                    indent=4,
                    sort_keys=False,
                    default=str
                ),
                content_type='application/json;charset=utf-8',
                status=200
            )

        except HttpError as error:
            print(f'An error occurred: {error}')
            return Response(
                json.dumps(
                    {'success': False, 'error': str(error)}, indent=4,
                    sort_keys=False,
                    default=str
                ),
                content_type='application/json;charset=utf-8',
                status=error.status_code
            )

    @http.route('/api/v1/drive-files', type='http', auth='user')
    def retrieve_files(self, **kwargs):
        try:
            # Authenticate and construct service.
            service = get_service(
                api_name='drive',
                api_version='v3'
            )

            # Call the Drive v3 API
            results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])

            downloadable_files = []
            for item in items:
                file_name = item['name']
                file_id = item['id']
                download_url = "https://drive.google.com/uc?id=%s&export=download" % item['id']
                downloadable_files.append({
                    'id': file_id,
                    'file_name': file_name,
                    'download_url': download_url
                })

            return Response(
                json.dumps(
                    {'success': True, 'result': downloadable_files}, indent=4,
                    sort_keys=False,
                    default=str
                ),
                content_type='application/json;charset=utf-8',
                status=200
            )

        except HttpError as error:
            print(f'An error occurred: {error}')
            return Response(
                json.dumps(
                    {'success': False, 'error': str(error)}, indent=4,
                    sort_keys=False,
                    default=str
                ),
                content_type='application/json;charset=utf-8',
                status=error.status_code
            )
