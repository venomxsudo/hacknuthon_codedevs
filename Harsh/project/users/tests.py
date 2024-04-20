# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from datetime import datetime, timedelta

# # Define the scopes required
# SCOPES = ['https://www.googleapis.com/auth/fitness.activity.read']

# def authenticate():
#     # Set up the OAuth 2.0 flow for authorization
#     flow = InstalledAppFlow.from_client_secrets_file(
#         'credentials.json', SCOPES)
#     credentials = flow.run_local_server(port=0)

#     return credentials

# def fetch_step_data(credentials):
#     # Build the Google Fit service
#     fit_service = build('fitness', 'v1', credentials=credentials)

#     # Define the start and end times for the query
#     start_time = datetime.today() - timedelta(days=7)  # Fetch data for the last 7 days
#     end_time = datetime.today()

#     # Convert time to nanoseconds (required by Google Fit API)
#     start_time_nanos = int(start_time.timestamp()) * 1e9
#     end_time_nanos = int(end_time.timestamp()) * 1e9

#     # Fetch step count data
#     response = fit_service.users().dataset().aggregate(
#         userId='me',
#         body={
#             "aggregateBy": [{
#                 "dataTypeName": "com.google.step_count.delta",
#                 "dataSourceId": "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
#             }],
#             "bucketByTime": {"durationMillis": 86400000},
#             "startTimeMillis": str(start_time_nanos),
#             "endTimeMillis": str(end_time_nanos)
#         }).execute()

#     # Process the response and extract step count data
#     if 'bucket' in response:
#         for bucket in response['bucket']:
#             if 'dataset' in bucket:
#                 for dataset in bucket['dataset']:
#                     if 'point' in dataset:
#                         for point in dataset['point']:
#                             if 'value' in point:
#                                 for value in point['value']:
#                                     if 'intVal' in value:
#                                         print(f"Steps: {value['intVal']}")
#     else:
#         print('No data available')

# if __name__ == '__main__':
#     credentials = authenticate()
#     fetch_step_data(credentials)



# import mysql.connector

# # Establishing the connection
# try:
#     conn = mysql.connector.connect(
#         host='localhost',  # e.g., 'localhost' or '127.0.0.1'
#         database='hacknuthon',
#         user='root',
#         password='Harsh@2454'
#     )

#     if conn.is_connected():
#         print('Connected to MySQL database')

#         # Perform database operations here
#         # For example, executing a query
#         cursor = conn.cursor()
        
#         # cursor.execute("Create table users_user (id int, name varchar(255), email varchar(255), phone varchar(20), password varchar(128), otp varchar(200), created_at datetime);")
#         # i want to insert data into the table
#         # cursor.execute("INSERT INTO users_user (id, name, email, phone, password, otp, created_at) VALUES (1, 'Harsh', 'harshmavani@gmail.com', '1234567890', '123456', '123456', '2021-09-25 00:00:00');")
#         # rows = cursor.fetchall()
#         # i want to delete the data from the table
#         cursor.execute("use hacknuthon;")
#         # cursor.execute("create table users_user1 (id int, name varchar(255), email varchar(255), phone varchar(20), password varchar(128), otp varchar(200), created_at datetime);")
#         # # i want to commit the changes
#         # conn.commit()
#         # cursor.execute("INSERT INTO users_user1 (id, name, email, phone, password, otp, created_at) VALUES (1, 'Harsh', 'harsh@gmail.com', '123456789', '123456', '123456', '2021-09-25 00:00:00');")
#         # conn.commit()
#         # cursor.execute("select * from users_user1;")
#         cursor.execute("create table users_user2a (id int, name varchar(255), email varchar(255), phone varchar(20), password varchar(128), otp varchar(200), created_at datetime);")
        
# except mysql.connector.Error as e:
#     print(f"Error connecting to MySQL database: {e}")

# finally:
#     # Closing the connection
#     if conn.is_connected():
#         cursor.close()
#         conn.close()
#         print('MySQL connection closed')


import re

def detect_sql_code_blocks(input_string):
    # Define a regular expression pattern to match code blocks starting with ```sql
    pattern = r'```sql(.*?)```'

    # Use regex to find all code blocks matching the pattern
    code_blocks = re.findall(pattern, input_string, re.DOTALL)

    return code_blocks

# Example usage
input_text = """
Here's an SQL query that should meet your requirements:

```sql
SELECT name, department
FROM Employees
WHERE salary < 20000;```"""

print(detect_sql_code_blocks(input_text))