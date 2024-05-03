import json
import boto3
from datetime import datetime
from io import StringIO
import pandas as pd 


def transform(candels):
    candels_list = []
    for row in candels:
      date = row[0]
      open = row[1]
      high = row[2]
      low = row[3]
      close = row[4]
      volume = row[5]
      ele = {"date":date,"open":open,"high":high,"low":low,"close":close,"volume":volume}
      candels_list.append(ele)
    return candels_list


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    Bucket = "upstocks-api-data"
    Key = "raw_data/to_processed/"
    
    upstox_data = []
    upstox_keys = []
    for file in s3.list_objects(Bucket=Bucket, Prefix=Key)['Contents']:
        file_key = file['Key']
        if file_key.split('.')[-1] == "json":
            response = s3.get_object(Bucket = Bucket, Key = file_key)
            content = response['Body']
            jsonObject = json.loads(content.read())
            upstox_data.append(jsonObject)
            upstox_keys.append(file_key)
            
    
    for data in upstox_data:
        candels = data['data']['candles']
        RIL_list = transform(candels)
        
        data_df = pd.DataFrame.from_dict(RIL_list)
        data_df = data_df.drop_duplicates(subset=['date'])
        
        
        RIL_key = "transformed_data/RIL_data/RIL_transformed_" + str(datetime.now()) + ".csv"
        RIL_buffer=StringIO()
        data_df.to_csv(RIL_buffer, index=False)
        RIL_content = RIL_buffer.getvalue()
        s3.put_object(Bucket=Bucket, Key=RIL_key, Body=RIL_content)
        
        
    s3_resource = boto3.resource('s3')
    for key in upstox_keys:
        copy_source = {
            'Bucket': Bucket,
            'Key': key
        }
        s3_resource.meta.client.copy(copy_source, Bucket, 'raw_data/processed/' + key.split("/")[-1])    
        s3_resource.Object(Bucket, key).delete()
        
