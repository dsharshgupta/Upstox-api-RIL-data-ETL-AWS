import json
from datetime import datetime, timedelta
import requests
import boto3
def lambda_handler(event, context):
    end = str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2)
    da = datetime.now() - timedelta(days=365*5)
    start = str(da.year) + "-" + str(da.month).zfill(2) + "-" + str(da.day).zfill(2)

    url = f'https://api.upstox.com/v2/historical-candle/NSE_EQ%7CINE002A01018/day/{end}/{start}'
    headers = {
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        
    cilent = boto3.client('s3')
    
    filename = "upstox_raw_" + str(datetime.now()) + ".json"
    
    cilent.put_object(
        Bucket="upstocks-api-data",
        Key="raw_data/to_processed/" + filename,
        Body=json.dumps(data)
        )
    
    
    
