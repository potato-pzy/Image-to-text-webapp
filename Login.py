import streamlit as st

import base64
import cv2
import sqlite3


# ================ Background image ===

st.markdown(f'''
    <h1 style="color:#00008B;text-align: center;font-size:36px;font-family:'Times New Roman', Times, serif;text-shadow:2px 2px 5px #000000;font-weight:bold;text-transform: uppercase;">
        Photo to Text Converter App for the Visually Impaired
    </h1>
''', unsafe_allow_html=True)
st.markdown("""
    <style>
        .stTextInput input {
            font-family: 'Goudy Old Style', serif;
            font-size: 16px;
            color: #FFFFFF;  /* White text color */
            background: linear-gradient(45deg, #000000, #FFFFFF); /* Mixed black and white gradient background */
            border: 1px solid #3498DB;  /* Border color */
        }
        .stTextInput label {
            font-family: 'Goudy Old Style', serif;
            font-size: 18px;
            color: #FFFFFF; /* White label text color */
        }
        .stPassword input {
            font-family: 'Goudy Old Style', serif;
            font-size: 16px;
            color: #FFFFFF;  /* White text color */
            background: linear-gradient(45deg, #000000, #FFFFFF); /* Mixed black and white gradient background */
            border: 1px solid #3498DB;  /* Border color */
        }
        .stTextInput input:focus, .stPassword input:focus {
            border: 2px solid #FF6347; /* Change border color on focus */
        }
    </style>
""", unsafe_allow_html=True)

def add_bg_from_local(image_file):
    import base64
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpeg"};base64,{encoded_string.decode()});
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

add_bg_from_local('neww.jpg')

# ----------------------
st.markdown(f'<h1 style="color:black;text-align: center;font-size:24px;font-family:Garamond;font-weight:bold;">{"LOGIN HERE !!!"}</h1>', unsafe_allow_html=True)



# Function to create a database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

# Function to create a new user
def create_user(conn, user):
    sql = ''' INSERT INTO users(name, password, email, phone)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid

# Function to validate user credentials
def validate_user(conn, name, password):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE name=? AND password=?", (name, password))
    user = cur.fetchone()
    if user:
        return True, user[1]  # Return True and user name
    return False, None

# Main function
def main():
    # st.title("User Login")
    


    # Create a database connection
    conn = create_connection("dbs.db")

    if conn is not None:
        # Create users table if it doesn't exist
        conn.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY,
                     name TEXT NOT NULL,
                     password TEXT NOT NULL,
                     email TEXT NOT NULL UNIQUE,
                     phone TEXT NOT NULL);''')

        st.write("Enter your credentials to login:")
        name = st.text_input("User name")
        password = st.text_input("Password", type="password")

        col1, col2 = st.columns(2)

        with col1:
                
            aa = st.button("Login")
            
            if aa:


        # # if st.button("Login"):
                is_valid, user_name = validate_user(conn, name, password)
                if is_valid:
                    st.success(f"Welcome back, {user_name}! Login successful!")
                    
                    import subprocess
                    subprocess.run(['python','-m','streamlit','run','app.py'])
                    
                    
                    
                    
                    
                else:
                    st.error("Invalid user name or password!")
                    
       
                  # st.success('Successfully Registered !!!')          
                    
                    
        # if st.button("Change Password"):
        #     import subprocess
        #     subprocess.run(['streamlit','run','CP.py'])


        # Close the database connection
        conn.close()
    else:
        st.error("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
    
        
        
        
        
        
        
        
        
        
        
        
        