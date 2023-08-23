import requests
import datetime
import pandas as pd
import credential
import uuid



def runner():
    today = datetime.date.today()
    start_date = str(today - datetime.timedelta(days=2))
    end_date = str(today)

    url = f'https://newsapi.org/v2/everything?q=bitcoin&from={start_date}&to={end_date}&language=en&sortBy=publishedAt'

    # Your API key
    api_key = credential.api_key


    # Construct the Authorization header
    headers = {
        "Authorization": f"Bearer {api_key}"
    }


    # Make the API request
    response = requests.get(url, headers=headers)

    # Check the response
    if response.status_code != 200: print("API request failed with status code:", response.status_code, "\n", "Error message:", response.text)
    data = response.json()
    print("API response:", response.status_code)
    
    df = pd.DataFrame(columns=['newsTitle', 'timestamp', 'urlSource', 'content', 'source', 'author', 'urlToImage'])

    for news in data['articles']:

        # extract all values
        newsTitle = news['title']
        timestamp = news['publishedAt']
        urlSource = news['url']
        source = news['source']['name']
        author = news['author']
        urlToImage = news['urlToImage']

        # clean content value
        content = news['content']
        if news['content'] is not None:
            content = news['content'][:199]
        if '.' in content:
            content = content[:content.rindex('.')]
        else:
            content = ''

        # add to dataframe
        df = pd.concat([df, 
                        pd.DataFrame({ 'newsTitle': newsTitle, 
                                'timestamp': timestamp,
                                'urlSource': urlSource,
                                'content': content,
                                'author': author,
                                'source': source,
                                'urlToImage': urlToImage
        }, index = ['article'])], ignore_index=True)


    df1 = df.drop_duplicates()

    filename = str(uuid.uuid4())
    dir = '/Users/tomiwa/Desktop/DE/DataEngineering/main_projects/news-data-pipeline-airflow-snowflake-aws/dataset/' # correct path for ec2 '/home/ubuntu/'

    output_file = f'{dir+filename}.parquet'
    
    df1.to_parquet(output_file)

    return output_file

