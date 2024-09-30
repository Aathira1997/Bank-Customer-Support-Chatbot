from faker import Faker
import mysql.connector

fake = Faker()

try:
    conn = mysql.connector.connect(
        host="",
        user="",  
        password="",  
        database=""  
    )
    cursor = conn.cursor()

    def insert_customer_data(cursor, num_records):
        for _ in range(num_records):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.email()
            phone_number = fake.phone_number()[:15]
            account_number = fake.bban()
            balance = round(fake.random_number(digits=5), 2)
            
            account_type = fake.random_choices(elements=('Saving', 'Current', 'Salary'), length=1)[0]

            created_at = fake.date_time_this_decade()

            cursor.execute("""
                INSERT INTO customers (first_name, last_name, email, phone_number, account_number, balance, account_type, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (first_name, last_name, email, phone_number, account_number, balance, account_type, created_at))

    
    print("Starting data insertion...")
    insert_customer_data(cursor, 2000)
    
    
    conn.commit()
    print("Data insertion completed.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
