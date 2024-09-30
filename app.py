import streamlit as st
import base64

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

image_path = ""  
base64_image = encode_image(image_path)

# Streamlit app 
st.markdown(
    f"""
    <style>
    .main {{
        background-image: url("data:image/jpeg;base64,{base64_image}");
        background-size: cover;
        background-position: center;
    }}
    .title {{
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        color: white;
    }}
    .subheader {{
        font-size: 20px;
        text-align: center;
        color: white;
    }}
    .stButton>button {{
        background-color: white;
        color: black;
        border: 2px solid #007BFF;
    }}
    .stTextInput>div>input {{
        font-size: 16px;
    }}
    .customer-box {{
        background-color: white;
        border: 2px solid #007BFF;
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
        margin-bottom: 30px;
        max-width: 400px;
        text-align: left;
    }}
    .button-container {{
        display: flex;
        justify-content: start;
        gap: 10px;
        margin-top: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Welcome to Bank Chatbot")


if 'customer_name' not in st.session_state:
    st.session_state.customer_name = None
if 'account_number' not in st.session_state:
    st.session_state.account_number = None
if 'question_mode' not in st.session_state:
    st.session_state.question_mode = False

# Step 1: Enter Account Number
if st.session_state.customer_name is None:
    st.subheader("Please enter your account number:")
    account_number = st.text_input("", placeholder="Account Number", key="account_number_input")  # Empty label

    
    if st.button("Submit", key="submit_account_number"):
        if account_number:
            
            find_name_query = f"SELECT customer_name FROM gems_customers WHERE account_number = '{account_number}'"
            sql_query = generate_sql_query(find_name_query)
            results = execute_sql_query(sql_query)
            formatted_results = format_results(results)
            if formatted_results:
                st.session_state.customer_name = formatted_results[0]['customer_name']
                st.session_state.account_number = account_number
                st.session_state.question_mode = True
                
                st.markdown(f"<div class='customer-box'>Customer Name: {st.session_state.customer_name}</div>", unsafe_allow_html=True)
            else:
                st.write("Account number not found. Please try again.")
        else:
            st.write("Please enter an account number.")
    
# Step 2: Display Customer Name and Ask for Query
if st.session_state.customer_name and st.session_state.question_mode:
    st.markdown("<h2 style='color:white;'>How can I help you?</h2>", unsafe_allow_html=True)
    user_query = st.text_input("Please type your question:", key="user_query_input")

    if st.button("Submit", key="submit_user_query"):
        if user_query:
            
            sql_query = generate_sql_query(user_query)
            sql_query = sql_query.replace('Customer Name', st.session_state.customer_name)  
            results = execute_sql_query(sql_query)
            formatted_results = format_results(results)

            # Display results in a table 
            if formatted_results:
                st.write("Result:")
                df = pd.DataFrame(formatted_results)
                df.index = df.index + 1  
                df.index.name = 'Sl.No'  
                st.dataframe(df, use_container_width=True, height=300) 

                # Display the generated SQL query below the output
                st.write("Generated SQL Query:")
                st.code(sql_query)

                # Option to proceed to next question
                if st.button("Next Question", key="next_question"):
                    st.session_state.question_mode = True
                
                # Instruction to close the tab below the Next Question button
                st.markdown("<h4 style='color:red;'>Once you are done, please close the tab.</h4>", unsafe_allow_html=True)

