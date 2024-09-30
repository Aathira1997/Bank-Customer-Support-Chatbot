import mysql.connector
from datetime import datetime
from transformers import pipeline
from langchain_core.prompts import PromptTemplate
import pandas as pd
from huggingface_hub import login, whoami

# Hugging Face Authentication
HF_TOKEN = ''

try:
    login(token=HF_TOKEN)
    whoami()  
except ValueError as e:
    st.error(f"Authentication failed: {e}")

# Prompt template for SQL query generation
template = """
You are a SQL query generator for the `gems_customers` table with the following columns:
- customer_name (TEXT)
- account_type (TEXT)
- account_number (TEXT)
- balance (FLOAT)
- created_at (TIMESTAMP)

The user will first provide an account number. Your task is to:
1. Find the `customer_name` for the provided `account_number`.
2. After identifying the customer name, the user will ask a question. Generate an accurate SQL query based on the user's question. The questions and their corresponding SQL queries are:

   - **Question: "What is my balance?"**
     SQL Query: `SELECT balance FROM gems_customers WHERE customer_name = 'Customer Name';`
   - **Question: "What is my account type?"**
     SQL Query: `SELECT account_type FROM gems_customers WHERE customer_name = 'Customer Name';`
   - **Question: "When was my account created?"**
     SQL Query: `SELECT created_at FROM gems_customers WHERE customer_name = 'Customer Name';`
   - **Question: "What is the creation date and time of my account?"**
     SQL Query: `SELECT created_at FROM gems_customers WHERE customer_name = 'Customer Name';`

**User Query:**
{query}
"""

prompt = PromptTemplate(template=template, input_variables=["query"])

# Model pipeline
pipe = pipeline("text2text-generation", model="google/flan-t5-small")

def generate_sql_query(user_query):
    formatted_prompt = prompt.format(query=user_query)
    result = pipe(formatted_prompt, max_new_tokens=100)
    sql_query = result[0]['generated_text'].strip()
    return sql_query

def get_db_connection():
    return mysql.connector.connect(
        host="",
        port="",
        user="", 
        password="",  
        database=""
    )

def execute_sql_query(sql_query):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as err:
        st.error(f"Error executing SQL query: {err}")
        return []
    finally:
        cursor.close()
        connection.close()

def format_results(results):
    formatted_results = []
    for row in results:
        formatted_row = {}
        for key, value in row.items():
            if isinstance(value, datetime):
                formatted_row[key] = value.strftime('%Y-%m-%d %H:%M:%S')
            elif key == 'account_type':  # Check if the key is account_type
                formatted_row[key] = value.replace("GEMS-", "")  # Remove "Gems-" prefix
            else:
                formatted_row[key] = value
        formatted_results.append(formatted_row)
    return formatted_results

