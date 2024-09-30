import pandas as pd
from sqlalchemy import create_engine
import mysql.connector


bank_customers_conn = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)
fease_conn = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)


bank_customers_engine = create_engine('')
fease_engine = create_engine('')


df = pd.read_sql('SELECT * FROM customers LIMIT 2000', con=bank_customers_engine)


def convert_to_gems(data):
    
    data['gems_customer_name'] = data['first_name'] + ' ' + data['last_name']
    
    data['gems_account'] = data['account_type'].apply(lambda x: 'GEMS-' + x)
    
    gems_data = data[['gems_customer_name', 'gems_account', 'account_number', 'balance', 'created_at']]
    
    
    gems_data = gems_data.rename(columns={
        'gems_customer_name': 'customer_name',
        'gems_account': 'account_type',
        'account_number': 'account_number',
        'balance': 'balance',  
        'created_at': 'created_at'  
    })
    
    return gems_data


gems_data = convert_to_gems(df)

gems_data.to_sql('gems_customers', con=fease_engine, if_exists='replace', index=False)

print("Data has been converted to GEMS format and stored in the Fease database.")
