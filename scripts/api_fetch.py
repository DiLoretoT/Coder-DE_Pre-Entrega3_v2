import requests
import pandas as pd
from datetime import datetime, timedelta
import pytz
from utils import read_api_credentials

def fetch_and_process_data(endpoint: str, description: str) -> pd.DataFrame:
    headers = {
        'Authorization': f'Bearer {read_api_credentials("config.ini", "api_bcra")["api_token"]}'
    }
    url = f'https://api.estadisticasbcra.com{endpoint}'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        df.rename(columns={'d': 'Date', 'v': 'Value'}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize('America/Buenos_Aires')
        df['Concept'] = description
        
        return df
    
    else:
        print(f'Failed to fetch data from {endpoint}. Status code: {response.status_code}')
        return pd.DataFrame()  