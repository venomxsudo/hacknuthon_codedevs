from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Define the scopes required
SCOPES = ['https://www.googleapis.com/auth/fitness.activity.read']

def authenticate():
    # Set up the OAuth 2.0 flow for authorization
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    credentials = flow.run_local_server(port=0)

    return credentials

def fetch_step_data(credentials):
    # Build the Google Fit service
    fit_service = build('fitness', 'v1', credentials=credentials)

    # Define the start and end times for the query
    start_time = datetime.today() - timedelta(days=7)  # Fetch data for the last 7 days
    end_time = datetime.today()

    # Convert time to nanoseconds (required by Google Fit API)
    start_time_nanos = int(start_time.timestamp()) * 1e9
    end_time_nanos = int(end_time.timestamp()) * 1e9

    # Fetch step count data
    response = fit_service.users().dataset().aggregate(
        userId='me',
        body={
            "aggregateBy": [{
                "dataTypeName": "com.google.step_count.delta",
                "dataSourceId": "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
            }],
            "bucketByTime": {"durationMillis": 86400000},
            "startTimeMillis": str(start_time_nanos),
            "endTimeMillis": str(end_time_nanos)
        }).execute()

    # Process the response and extract step count data
    if 'bucket' in response:
        for bucket in response['bucket']:
            if 'dataset' in bucket:
                for dataset in bucket['dataset']:
                    if 'point' in dataset:
                        for point in dataset['point']:
                            if 'value' in point:
                                for value in point['value']:
                                    if 'intVal' in value:
                                        print(f"Steps: {value['intVal']}")
    else:
        print('No data available')

if __name__ == '__main__':
    credentials = authenticate()
    fetch_step_data(credentials)
