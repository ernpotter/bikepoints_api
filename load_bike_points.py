import os
import boto3
from dotenv import load_dotenv


# creating load fucntion
def load_bikes():
    
    load_dotenv()

    aws_access = os.getenv('ACCESS_KEY')
    aws_secret = os.getenv('SECRET_ACCESS_KEY')
    bucket = os.getenv('AWS_BUCKET_NAME')

    # setting up client object
    s3_client = boto3.client(
        's3',
        aws_access_key_id = aws_access,
        aws_secret_access_key = aws_secret
    )

    # figuring out the file to upload to s3
    try: 
        file = os.listdir('data')[0] # tell us what is in the data folder. checking if its a file. looking for the first one.
        filename = 'data/'+file
        s3file = 'bike-point/'+file
        try:
            # uploading file to s3  (filename, bucket, key). key = where it's going in s3
            s3_client.upload_file(filename, bucket, s3file)
            print('Uplaod successful')
            os.remove(filename) #removing file once its uploaded successfully to s3
        except: 
            print('Could not upload')
    except:
        print('No files :(')
