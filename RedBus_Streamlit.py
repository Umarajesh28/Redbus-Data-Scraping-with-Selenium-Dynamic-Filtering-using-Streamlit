import streamlit as st
import pandas as pd
import mysql.connector
from streamlit_option_menu import option_menu
from datetime import datetime

# Filtering each bus and appending to list

# Andhra Pradesh
APSRTC = []
df_APSRTC = pd.read_csv(r'C:\Users\user\Desktop\RED_BUS\venv\Scripts\df_APSRTC.csv')
for i, r in df_APSRTC.iterrows():
    APSRTC.append(r['Route_name'])

# Telangana
TSRTC = []
df_TSRTC = pd.read_csv(r'C:\Users\user\Desktop\RED_BUS\venv\Scripts\df_TSRTC.csv')
for i, r in df_TSRTC.iterrows():
    TSRTC.append(r['Route_name'])

# Kerala
KSRTC = []
df_KSRTC = pd.read_csv(r'C:\Users\user\Desktop\RED_BUS\venv\Scripts\df_KSRTC.csv')
for i, r in df_KSRTC.iterrows():
    KSRTC.append(r['Route_name'])

# South Bengal
SBSTC = []
df_SBSTC = pd.read_csv(r'C:\Users\user\Desktop\RED_BUS\venv\Scripts\df_SBSTC.csv')
for i, r in df_SBSTC.iterrows():
    SBSTC.append(r['Route_name'])

# West Bengal
WBTC = []
df_WBTC = pd.read_csv(r'C:\Users\user\Desktop\RED_BUS\venv\Scripts\df_WBTC.csv')
for i, r in df_WBTC.iterrows():
    WBTC.append(r['Route_name'])

# Bihar
BSRTC = []
df_BSRTC = pd.read_csv(r'C:\Users\user\Desktop\RED_BUS\venv\Scripts\df_BSRTC.csv')
for i, r in df_BSRTC.iterrows():
    BSRTC.append(r['Route_name'])

# Himachal
HRTC = []
df_HRTC = pd.read_csv(r'C:\Users\user\Desktop\RED_BUS\venv\Scripts\df_HRTC.csv')
for i, r in df_HRTC.iterrows():
    HRTC.append(r['Route_name'])

# Assam
ASTC = []
df_ASTC = pd.read_csv(r'C:\Users\user\Desktop\RED_BUS\venv\Scripts\df_ASTC.csv')
for i, r in df_ASTC.iterrows():
    ASTC.append(r['Route_name'])

# Rajasthan
RSRTC = []
df_RSRTC = pd.read_csv(r'C:\Users\user\Desktop\RED_BUS\venv\Scripts\df_RSRTC.csv')
for i, r in df_RSRTC.iterrows():
    RSRTC.append(r['Route_name'])

# Uttar Pradesh
UPSRTC = []
df_UPSRTC = pd.read_csv(r'C:\Users\user\Desktop\RED_BUS\venv\Scripts\df_UPSRTC.csv')
for i, r in df_UPSRTC.iterrows():
    UPSRTC.append(r['Route_name'])

# Streamlit page layout
st.set_page_config(page_title="Redbus Application", layout="wide", initial_sidebar_state="expanded")
st.markdown("<h2 style='color: Black;'>Welcome to RedBus Application</h2>", unsafe_allow_html=True)

# Sidebar navigation 
with st.sidebar:
    st.image(r'C:\Users\user\Downloads\RedBuslogo.jpg', width=200)
    menu = option_menu("Main Menu", ["Home", 'Bus Routes'], 
                       icons=['house', 'gear'], menu_icon="cast", default_index=0,
                       styles={"icon": {"font-size": "21px"},
                               "nav-link-selected": {"background-color": "#f58169 "}})

if menu == "Home":
    st.markdown("<h1 style='color: red;'>Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit</h1>", unsafe_allow_html=True)
    st.text("")
    st.markdown("""
        ### Objective of the Project
        The Redbus Data Scraping and Filtering with Streamlit Application seeks to transform the 
        transportation sector by offering a robust solution for the collection, analysis, and visualization of bus travel data. 
        Leveraging Selenium for web scraping, this project automates the extraction of detailed information from Redbus, 
        encompassing bus routes, schedules, prices, and seat availability. By streamlining the data collection process 
        and providing powerful analytical tools, this project aims to enhance operational efficiency and strategic planning 
        within the transportation industry.
    """)

if menu == "Bus Routes":
    st.title("🚍 Filter Your Bus")
         
    col1, col2 = st.columns(2)
    with col1:
        state = st.selectbox("Select State", ["Andhra Pradesh", "Telangana", "Kerala", "Rajasthan", "Himachal", "South Bengal", "Assam", "West Bengal", "Uttar Pradesh", "Bihar"])
    with col2:
        bus_type = st.selectbox("Choose Bus type", ["A/C", "NON A/C", "Sleeper", "Semi-sleeper", "Seater", "others"])
    with col1:
        fare_range = st.radio("Choose Price range", ("50-1000", "1000-2000", "2000 and above"))
    with col2:
        rating_range = st.slider("Choose rating", min_value=1, max_value=5, value=5, step=1)
    with col1:
        seats = st.selectbox("Seat Availability", ("0-10", "10-20", "20-30", "30 and above"))
    with col1:
        time = st.time_input("Select Time")

     # Function to filter data from the SQL database
    def filter_data(bus_type, fare_range, rating_range, seats, APSRTC, time):
        conn = mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="Uma@1728", 
            database="RED_BUS_ROUTES", 
            auth_plugin='mysql_native_password'
        )
        my_cursor = conn.cursor()

        # Filtration for rating
        rate_min, rate_max = 0, 5  # Default range
        if rating_range == 5:
            rate_min, rate_max = 4.0, 5
        elif rating_range == 4:
            rate_min, rate_max = 3.0, 4.0
        elif rating_range == 3:
            rate_min, rate_max = 2.0, 3.0
        elif rating_range == 2:
            rate_min, rate_max = 1.0, 2.0
        elif rating_range == 1:
            rate_min, rate_max = 0, 1.0

        # Define bus type condition
        if bus_type == "Sleeper":
            bus_type_option = "Bus_type LIKE '%Sleeper%'"
        elif bus_type == "Semi-sleeper":
            bus_type_option = "Bus_type LIKE '%Semi Sleeper%'"
        elif bus_type == "A/C":
            bus_type_option = "Bus_type LIKE '% A/C %'"
        elif bus_type == "NON A/C":
            bus_type_option = "Bus_type LIKE '% NON A/C%'"
        elif bus_type == "Seater":
            bus_type_option = "Bus_type LIKE '% Seater%'"
        else:
            bus_type_option = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-sleeper%' AND Bus_type NOT LIKE '%Seater%' AND Bus_type NOT LIKE '%A/C%' AND Bus_type NOT LIKE '%NON A/C%'"

        # Define fare range
        if fare_range == "50-1000":
            fare_min, fare_max = 50, 1000
        elif fare_range == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000

        # Define seat availability condition
        if seats == "0-10":
            seat_condition = "Seats_Available BETWEEN 0 AND 10"
        elif seats == "10-20":
            seat_condition = "Seats_Available BETWEEN 11 AND 20"
        elif seats == "20-30":
            seat_condition = "Seats_Available BETWEEN 21 AND 30"
        else:
            seat_condition = "Seats_Available >= 30"

        # Build the SQL query
        sql_query = f'''
            SELECT * FROM bus_details
            WHERE price BETWEEN {fare_min} AND {fare_max}
            AND route_name = %s
            AND {bus_type_option}
            AND Start_time >= %s
            AND star_rating BETWEEN {rate_min} AND {rate_max}
            AND {seat_condition}
            ORDER BY price, Start_time DESC
        '''

        my_cursor.execute(sql_query, (APSRTC, time))  # Use parameterized query to prevent SQL injection
        out2 = my_cursor.fetchall()
        conn.close()

        # Convert query result to DataFrame
        df = pd.DataFrame(out2, columns=[
            "ID", "Bus_name", "Route_name", "Bus_type", "Start_time", "Duration", "End_time", "Ratings", "Price", "Seats_available", "Route_link"
        ])
        return df

    #1 Andhra Pradesh
    if state=="Andhra Pradesh":
        with col2:
         APSRTC=st.selectbox("List of routes",APSRTC)
        
        # Function to filter data from the SQL database
    def filter_data(bus_type, fare_range, rating_range, seats, APSRTC, time):
        conn = mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="Uma@1728", 
            database="RED_BUS_ROUTES", 
            auth_plugin='mysql_native_password'
        )
        my_cursor = conn.cursor()

        # Filtration for rating
        rate_min, rate_max = 0, 5  # Default range
        if rating_range == 5:
            rate_min, rate_max = 4.0, 5
        elif rating_range == 4:
            rate_min, rate_max = 3.0, 4.0
        elif rating_range == 3:
            rate_min, rate_max = 2.0, 3.0
        elif rating_range == 2:
            rate_min, rate_max = 1.0, 2.0
        elif rating_range == 1:
            rate_min, rate_max = 0, 1.0

        # Define bus type condition
        if bus_type == "Sleeper":
            bus_type_option = "Bus_type LIKE '%Sleeper%'"
        elif bus_type == "Semi-sleeper":
            bus_type_option = "Bus_type LIKE '%Semi Sleeper%'"
        elif bus_type == "A/C":
            bus_type_option = "Bus_type LIKE '% A/C %'"
        elif bus_type == "NON A/C":
            bus_type_option = "Bus_type LIKE '% NON A/C%'"
        elif bus_type == "Seater":
            bus_type_option = "Bus_type LIKE '% Seater%'"
        else:
            bus_type_option = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-sleeper%' AND Bus_type NOT LIKE '%Seater%' AND Bus_type NOT LIKE '%A/C%' AND Bus_type NOT LIKE '%NON A/C%'"

        # Define fare range
        if fare_range == "50-1000":
            fare_min, fare_max = 50, 1000
        elif fare_range == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000

        # Define seat availability condition
        if seats == "0-10":
            seat_condition = "Seats_Available BETWEEN 0 AND 10"
        elif seats == "10-20":
            seat_condition = "Seats_Available BETWEEN 11 AND 20"
        elif seats == "20-30":
            seat_condition = "Seats_Available BETWEEN 21 AND 30"
        else:
            seat_condition = "Seats_Available >= 30"

        # Build the SQL query
        sql_query = f'''
            SELECT * FROM bus_details
            WHERE price BETWEEN {fare_min} AND {fare_max}
            AND route_name = %s
            AND {bus_type_option}
            AND Start_time >= %s
            AND star_rating BETWEEN {rate_min} AND {rate_max}
            AND {seat_condition}
            ORDER BY price, Start_time DESC
        '''

        my_cursor.execute(sql_query, (APSRTC, time))  # Use parameterized query to prevent SQL injection
        out2 = my_cursor.fetchall()
        conn.close()

        # Convert query result to DataFrame
        df = pd.DataFrame(out2, columns=[
            "ID", "Bus_name", "Route_name", "Bus_type", "Start_time", "Duration", "End_time", "Ratings", "Price", "Seats_available", "Route_link"
        ])
        return df

     

   #2 Telangana
    if state=="Telangana":
      with col2:
            TSRTC=st.selectbox("List of routes",TSRTC)
        
        # Function to filter data from the SQL database
    def filter_data(bus_type, fare_range, rating_range, seats, APSRTC, time):
        conn = mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="Uma@1728", 
            database="RED_BUS_ROUTES", 
            auth_plugin='mysql_native_password'
        )
        my_cursor = conn.cursor()

        # Filtration for rating
        rate_min, rate_max = 0, 5  # Default range
        if rating_range == 5:
            rate_min, rate_max = 4.0, 5
        elif rating_range == 4:
            rate_min, rate_max = 3.0, 4.0
        elif rating_range == 3:
            rate_min, rate_max = 2.0, 3.0
        elif rating_range == 2:
            rate_min, rate_max = 1.0, 2.0
        elif rating_range == 1:
            rate_min, rate_max = 0, 1.0

        # Define bus type condition
        if bus_type == "Sleeper":
            bus_type_option = "Bus_type LIKE '%Sleeper%'"
        elif bus_type == "Semi-sleeper":
            bus_type_option = "Bus_type LIKE '%Semi Sleeper%'"
        elif bus_type == "A/C":
            bus_type_option = "Bus_type LIKE '% A/C %'"
        elif bus_type == "NON A/C":
            bus_type_option = "Bus_type LIKE '% NON A/C%'"
        elif bus_type == "Seater":
            bus_type_option = "Bus_type LIKE '% Seater%'"
        else:
            bus_type_option = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-sleeper%' AND Bus_type NOT LIKE '%Seater%' AND Bus_type NOT LIKE '%A/C%' AND Bus_type NOT LIKE '%NON A/C%'"

        # Define fare range
        if fare_range == "50-1000":
            fare_min, fare_max = 50, 1000
        elif fare_range == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000

        # Define seat availability condition
        if seats == "0-10":
            seat_condition = "Seats_Available BETWEEN 0 AND 10"
        elif seats == "10-20":
            seat_condition = "Seats_Available BETWEEN 11 AND 20"
        elif seats == "20-30":
            seat_condition = "Seats_Available BETWEEN 21 AND 30"
        else:
            seat_condition = "Seats_Available >= 30"

        # Build the SQL query
        sql_query = f'''
            SELECT * FROM bus_details
            WHERE price BETWEEN {fare_min} AND {fare_max}
            AND route_name = %s
            AND {bus_type_option}
            AND Start_time >= %s
            AND star_rating BETWEEN {rate_min} AND {rate_max}
            AND {seat_condition}
            ORDER BY price, Start_time DESC
        '''

        my_cursor.execute(sql_query, (TSRTC, time))  # Use parameterized query to prevent SQL injection
        out2 = my_cursor.fetchall()
        conn.close()

        # Convert query result to DataFrame
        df = pd.DataFrame(out2, columns=[
            "ID", "Bus_name", "Route_name", "Bus_type", "Start_time", "Duration", "End_time", "Ratings", "Price", "Seats_available", "Route_link"
        ])
        return df


    #3 Kerala
    if state=="Kerala":
       with col2:
        KSRTC=st.selectbox("List of routes",KSRTC)
        
       # Function to filter data from the SQL database
    def filter_data(bus_type, fare_range, rating_range, seats, APSRTC, time):
        conn = mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="Uma@1728", 
            database="RED_BUS_ROUTES", 
            auth_plugin='mysql_native_password'
        )
        my_cursor = conn.cursor()

        # Filtration for rating
        rate_min, rate_max = 0, 5  # Default range
        if rating_range == 5:
            rate_min, rate_max = 4.0, 5
        elif rating_range == 4:
            rate_min, rate_max = 3.0, 4.0
        elif rating_range == 3:
            rate_min, rate_max = 2.0, 3.0
        elif rating_range == 2:
            rate_min, rate_max = 1.0, 2.0
        elif rating_range == 1:
            rate_min, rate_max = 0, 1.0

        # Define bus type condition
        if bus_type == "Sleeper":
            bus_type_option = "Bus_type LIKE '%Sleeper%'"
        elif bus_type == "Semi-sleeper":
            bus_type_option = "Bus_type LIKE '%Semi Sleeper%'"
        elif bus_type == "A/C":
            bus_type_option = "Bus_type LIKE '% A/C %'"
        elif bus_type == "NON A/C":
            bus_type_option = "Bus_type LIKE '% NON A/C%'"
        elif bus_type == "Seater":
            bus_type_option = "Bus_type LIKE '% Seater%'"
        else:
            bus_type_option = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-sleeper%' AND Bus_type NOT LIKE '%Seater%' AND Bus_type NOT LIKE '%A/C%' AND Bus_type NOT LIKE '%NON A/C%'"

        # Define fare range
        if fare_range == "50-1000":
            fare_min, fare_max = 50, 1000
        elif fare_range == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000

        # Define seat availability condition
        if seats == "0-10":
            seat_condition = "Seats_Available BETWEEN 0 AND 10"
        elif seats == "10-20":
            seat_condition = "Seats_Available BETWEEN 11 AND 20"
        elif seats == "20-30":
            seat_condition = "Seats_Available BETWEEN 21 AND 30"
        else:
            seat_condition = "Seats_Available >= 30"

        # Build the SQL query
        sql_query = f'''
            SELECT * FROM bus_details
            WHERE price BETWEEN {fare_min} AND {fare_max}
            AND route_name = %s
            AND {bus_type_option}
            AND Start_time >= %s
            AND star_rating BETWEEN {rate_min} AND {rate_max}
            AND {seat_condition}
            ORDER BY price, Start_time DESC
        '''

        my_cursor.execute(sql_query, (KSRTC, time))  # Use parameterized query to prevent SQL injection
        out2 = my_cursor.fetchall()
        conn.close()

        # Convert query result to DataFrame
        df = pd.DataFrame(out2, columns=[
            "ID", "Bus_name", "Route_name", "Bus_type", "Start_time", "Duration", "End_time", "Ratings", "Price", "Seats_available", "Route_link"
        ])
        return df


   #4 South Bengal
    if state=="South Bengal":

         with col2:
            SBSTC=st.selectbox("List of routes",SBSTC)
        
       # Function to filter data from the SQL database
    def filter_data(bus_type, fare_range, rating_range, seats, APSRTC, time):
        conn = mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="Uma@1728", 
            database="RED_BUS_ROUTES", 
            auth_plugin='mysql_native_password'
        )
        my_cursor = conn.cursor()

        # Filtration for rating
        rate_min, rate_max = 0, 5  # Default range
        if rating_range == 5:
            rate_min, rate_max = 4.0, 5
        elif rating_range == 4:
            rate_min, rate_max = 3.0, 4.0
        elif rating_range == 3:
            rate_min, rate_max = 2.0, 3.0
        elif rating_range == 2:
            rate_min, rate_max = 1.0, 2.0
        elif rating_range == 1:
            rate_min, rate_max = 0, 1.0

        # Define bus type condition
        if bus_type == "Sleeper":
            bus_type_option = "Bus_type LIKE '%Sleeper%'"
        elif bus_type == "Semi-sleeper":
            bus_type_option = "Bus_type LIKE '%Semi Sleeper%'"
        elif bus_type == "A/C":
            bus_type_option = "Bus_type LIKE '% A/C %'"
        elif bus_type == "NON A/C":
            bus_type_option = "Bus_type LIKE '% NON A/C%'"
        elif bus_type == "Seater":
            bus_type_option = "Bus_type LIKE '% Seater%'"
        else:
            bus_type_option = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-sleeper%' AND Bus_type NOT LIKE '%Seater%' AND Bus_type NOT LIKE '%A/C%' AND Bus_type NOT LIKE '%NON A/C%'"

        # Define fare range
        if fare_range == "50-1000":
            fare_min, fare_max = 50, 1000
        elif fare_range == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000

        # Define seat availability condition
        if seats == "0-10":
            seat_condition = "Seats_Available BETWEEN 0 AND 10"
        elif seats == "10-20":
            seat_condition = "Seats_Available BETWEEN 11 AND 20"
        elif seats == "20-30":
            seat_condition = "Seats_Available BETWEEN 21 AND 30"
        else:
            seat_condition = "Seats_Available >= 30"

        # Build the SQL query
        sql_query = f'''
            SELECT * FROM bus_details
            WHERE price BETWEEN {fare_min} AND {fare_max}
            AND route_name = %s
            AND {bus_type_option}
            AND Start_time >= %s
            AND star_rating BETWEEN {rate_min} AND {rate_max}
            AND {seat_condition}
            ORDER BY price, Start_time DESC
        '''

        my_cursor.execute(sql_query, (SBSTC, time))  # Use parameterized query to prevent SQL injection
        out2 = my_cursor.fetchall()
        conn.close()

        # Convert query result to DataFrame
        df = pd.DataFrame(out2, columns=[
            "ID", "Bus_name", "Route_name", "Bus_type", "Start_time", "Duration", "End_time", "Ratings", "Price", "Seats_available", "Route_link"
        ])
        return df


    #5 West Bengal
    if state=="West Bengal":
        with col2:
         WBTC=st.selectbox("List of routes",WBTC)
        
       # Function to filter data from the SQL database
    def filter_data(bus_type, fare_range, rating_range, seats, APSRTC, time):
        conn = mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="Uma@1728", 
            database="RED_BUS_ROUTES", 
            auth_plugin='mysql_native_password'
        )
        my_cursor = conn.cursor()

        # Filtration for rating
        rate_min, rate_max = 0, 5  # Default range
        if rating_range == 5:
            rate_min, rate_max = 4.0, 5
        elif rating_range == 4:
            rate_min, rate_max = 3.0, 4.0
        elif rating_range == 3:
            rate_min, rate_max = 2.0, 3.0
        elif rating_range == 2:
            rate_min, rate_max = 1.0, 2.0
        elif rating_range == 1:
            rate_min, rate_max = 0, 1.0

        # Define bus type condition
        if bus_type == "Sleeper":
            bus_type_option = "Bus_type LIKE '%Sleeper%'"
        elif bus_type == "Semi-sleeper":
            bus_type_option = "Bus_type LIKE '%Semi Sleeper%'"
        elif bus_type == "A/C":
            bus_type_option = "Bus_type LIKE '% A/C %'"
        elif bus_type == "NON A/C":
            bus_type_option = "Bus_type LIKE '% NON A/C%'"
        elif bus_type == "Seater":
            bus_type_option = "Bus_type LIKE '% Seater%'"
        else:
            bus_type_option = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-sleeper%' AND Bus_type NOT LIKE '%Seater%' AND Bus_type NOT LIKE '%A/C%' AND Bus_type NOT LIKE '%NON A/C%'"

        # Define fare range
        if fare_range == "50-1000":
            fare_min, fare_max = 50, 1000
        elif fare_range == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000

        # Define seat availability condition
        if seats == "0-10":
            seat_condition = "Seats_Available BETWEEN 0 AND 10"
        elif seats == "10-20":
            seat_condition = "Seats_Available BETWEEN 11 AND 20"
        elif seats == "20-30":
            seat_condition = "Seats_Available BETWEEN 21 AND 30"
        else:
            seat_condition = "Seats_Available >= 30"

        # Build the SQL query
        sql_query = f'''
            SELECT * FROM bus_details
            WHERE price BETWEEN {fare_min} AND {fare_max}
            AND route_name = %s
            AND {bus_type_option}
            AND Start_time >= %s
            AND star_rating BETWEEN {rate_min} AND {rate_max}
            AND {seat_condition}
            ORDER BY price, Start_time DESC
        '''

        my_cursor.execute(sql_query, (WBTC, time))  # Use parameterized query to prevent SQL injection
        out2 = my_cursor.fetchall()
        conn.close()

        # Convert query result to DataFrame
        df = pd.DataFrame(out2, columns=[
            "ID", "Bus_name", "Route_name", "Bus_type", "Start_time", "Duration", "End_time", "Ratings", "Price", "Seats_available", "Route_link"
        ])
        return df


    #6 Bihar
    if state=="Bihar":
       with col2:
        BSRTC=st.selectbox("List of routes",BSRTC)
        
        # Function to filter data from the SQL database
    def filter_data(bus_type, fare_range, rating_range, seats, APSRTC, time):
        conn = mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="Uma@1728", 
            database="RED_BUS_ROUTES", 
            auth_plugin='mysql_native_password'
        )
        my_cursor = conn.cursor()

        # Filtration for rating
        rate_min, rate_max = 0, 5  # Default range
        if rating_range == 5:
            rate_min, rate_max = 4.0, 5
        elif rating_range == 4:
            rate_min, rate_max = 3.0, 4.0
        elif rating_range == 3:
            rate_min, rate_max = 2.0, 3.0
        elif rating_range == 2:
            rate_min, rate_max = 1.0, 2.0
        elif rating_range == 1:
            rate_min, rate_max = 0, 1.0

        # Define bus type condition
        if bus_type == "Sleeper":
            bus_type_option = "Bus_type LIKE '%Sleeper%'"
        elif bus_type == "Semi-sleeper":
            bus_type_option = "Bus_type LIKE '%Semi Sleeper%'"
        elif bus_type == "A/C":
            bus_type_option = "Bus_type LIKE '% A/C %'"
        elif bus_type == "NON A/C":
            bus_type_option = "Bus_type LIKE '% NON A/C%'"
        elif bus_type == "Seater":
            bus_type_option = "Bus_type LIKE '% Seater%'"
        else:
            bus_type_option = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-sleeper%' AND Bus_type NOT LIKE '%Seater%' AND Bus_type NOT LIKE '%A/C%' AND Bus_type NOT LIKE '%NON A/C%'"

        # Define fare range
        if fare_range == "50-1000":
            fare_min, fare_max = 50, 1000
        elif fare_range == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000

        # Define seat availability condition
        if seats == "0-10":
            seat_condition = "Seats_Available BETWEEN 0 AND 10"
        elif seats == "10-20":
            seat_condition = "Seats_Available BETWEEN 11 AND 20"
        elif seats == "20-30":
            seat_condition = "Seats_Available BETWEEN 21 AND 30"
        else:
            seat_condition = "Seats_Available >= 30"

        # Build the SQL query
        sql_query = f'''
            SELECT * FROM bus_details
            WHERE price BETWEEN {fare_min} AND {fare_max}
            AND route_name = %s
            AND {bus_type_option}
            AND Start_time >= %s
            AND star_rating BETWEEN {rate_min} AND {rate_max}
            AND {seat_condition}
            ORDER BY price, Start_time DESC
        '''

        my_cursor.execute(sql_query, (BSRTC, time))  # Use parameterized query to prevent SQL injection
        out2 = my_cursor.fetchall()
        conn.close()

        # Convert query result to DataFrame
        df = pd.DataFrame(out2, columns=[
            "ID", "Bus_name", "Route_name", "Bus_type", "Start_time", "Duration", "End_time", "Ratings", "Price", "Seats_available", "Route_link"
        ])
        return df


    #7 Himachal
    if state=="Himachal":
        with col2:
            HRTC=st.selectbox("List of routes",HRTC)
        
        # Function to filter data from the SQL database
    def filter_data(bus_type, fare_range, rating_range, seats, APSRTC, time):
        conn = mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="Uma@1728", 
            database="RED_BUS_ROUTES", 
            auth_plugin='mysql_native_password'
        )
        my_cursor = conn.cursor()

        # Filtration for rating
        rate_min, rate_max = 0, 5  # Default range
        if rating_range == 5:
            rate_min, rate_max = 4.0, 5
        elif rating_range == 4:
            rate_min, rate_max = 3.0, 4.0
        elif rating_range == 3:
            rate_min, rate_max = 2.0, 3.0
        elif rating_range == 2:
            rate_min, rate_max = 1.0, 2.0
        elif rating_range == 1:
            rate_min, rate_max = 0, 1.0

        # Define bus type condition
        if bus_type == "Sleeper":
            bus_type_option = "Bus_type LIKE '%Sleeper%'"
        elif bus_type == "Semi-sleeper":
            bus_type_option = "Bus_type LIKE '%Semi Sleeper%'"
        elif bus_type == "A/C":
            bus_type_option = "Bus_type LIKE '% A/C %'"
        elif bus_type == "NON A/C":
            bus_type_option = "Bus_type LIKE '% NON A/C%'"
        elif bus_type == "Seater":
            bus_type_option = "Bus_type LIKE '% Seater%'"
        else:
            bus_type_option = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-sleeper%' AND Bus_type NOT LIKE '%Seater%' AND Bus_type NOT LIKE '%A/C%' AND Bus_type NOT LIKE '%NON A/C%'"

        # Define fare range
        if fare_range == "50-1000":
            fare_min, fare_max = 50, 1000
        elif fare_range == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000

        # Define seat availability condition
        if seats == "0-10":
            seat_condition = "Seats_Available BETWEEN 0 AND 10"
        elif seats == "10-20":
            seat_condition = "Seats_Available BETWEEN 11 AND 20"
        elif seats == "20-30":
            seat_condition = "Seats_Available BETWEEN 21 AND 30"
        else:
            seat_condition = "Seats_Available >= 30"

        # Build the SQL query
        sql_query = f'''
            SELECT * FROM bus_details
            WHERE price BETWEEN {fare_min} AND {fare_max}
            AND route_name = %s
            AND {bus_type_option}
            AND Start_time >= %s
            AND star_rating BETWEEN {rate_min} AND {rate_max}
            AND {seat_condition}
            ORDER BY price, Start_time DESC
        '''

        my_cursor.execute(sql_query, (HRTC, time))  # Use parameterized query to prevent SQL injection
        out2 = my_cursor.fetchall()
        conn.close()

        # Convert query result to DataFrame
        df = pd.DataFrame(out2, columns=[
            "ID", "Bus_name", "Route_name", "Bus_type", "Start_time", "Duration", "End_time", "Ratings", "Price", "Seats_available", "Route_link"
        ])
        return df


   #8 Assam
    if state=="Assam":
    
         with col2:
          ASTC=st.selectbox("List of routes",ASTC)
        
        # Function to filter data from the SQL database
    def filter_data(bus_type, fare_range, rating_range, seats, APSRTC, time):
        conn = mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="Uma@1728", 
            database="RED_BUS_ROUTES", 
            auth_plugin='mysql_native_password'
        )
        my_cursor = conn.cursor()

        # Filtration for rating
        rate_min, rate_max = 0, 5  # Default range
        if rating_range == 5:
            rate_min, rate_max = 4.0, 5
        elif rating_range == 4:
            rate_min, rate_max = 3.0, 4.0
        elif rating_range == 3:
            rate_min, rate_max = 2.0, 3.0
        elif rating_range == 2:
            rate_min, rate_max = 1.0, 2.0
        elif rating_range == 1:
            rate_min, rate_max = 0, 1.0

        # Define bus type condition
        if bus_type == "Sleeper":
            bus_type_option = "Bus_type LIKE '%Sleeper%'"
        elif bus_type == "Semi-sleeper":
            bus_type_option = "Bus_type LIKE '%Semi Sleeper%'"
        elif bus_type == "A/C":
            bus_type_option = "Bus_type LIKE '% A/C %'"
        elif bus_type == "NON A/C":
            bus_type_option = "Bus_type LIKE '% NON A/C%'"
        elif bus_type == "Seater":
            bus_type_option = "Bus_type LIKE '% Seater%'"
        else:
            bus_type_option = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-sleeper%' AND Bus_type NOT LIKE '%Seater%' AND Bus_type NOT LIKE '%A/C%' AND Bus_type NOT LIKE '%NON A/C%'"

        # Define fare range
        if fare_range == "50-1000":
            fare_min, fare_max = 50, 1000
        elif fare_range == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000

        # Define seat availability condition
        if seats == "0-10":
            seat_condition = "Seats_Available BETWEEN 0 AND 10"
        elif seats == "10-20":
            seat_condition = "Seats_Available BETWEEN 11 AND 20"
        elif seats == "20-30":
            seat_condition = "Seats_Available BETWEEN 21 AND 30"
        else:
            seat_condition = "Seats_Available >= 30"

        # Build the SQL query
        sql_query = f'''
            SELECT * FROM bus_details
            WHERE price BETWEEN {fare_min} AND {fare_max}
            AND route_name = %s
            AND {bus_type_option}
            AND Start_time >= %s
            AND star_rating BETWEEN {rate_min} AND {rate_max}
            AND {seat_condition}
            ORDER BY price, Start_time DESC
        '''

        my_cursor.execute(sql_query, (ASTC, time))  # Use parameterized query to prevent SQL injection
        out2 = my_cursor.fetchall()
        conn.close()

        # Convert query result to DataFrame
        df = pd.DataFrame(out2, columns=[
            "ID", "Bus_name", "Route_name", "Bus_type", "Start_time", "Duration", "End_time", "Ratings", "Price", "Seats_available", "Route_link"
        ])
        return df

    
    #10 Uttar Pradesh
    if state=="Uttar Pradesh":
        with col2:
            UPSRTC=st.selectbox("List of routes",UPSRTC)
        
       # Function to filter data from the SQL database
    def filter_data(bus_type, fare_range, rating_range, seats, APSRTC, time):
        conn = mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="Uma@1728", 
            database="RED_BUS_ROUTES", 
            auth_plugin='mysql_native_password'
        )
        my_cursor = conn.cursor()

        # Filtration for rating
        rate_min, rate_max = 0, 5  # Default range
        if rating_range == 5:
            rate_min, rate_max = 4.0, 5
        elif rating_range == 4:
            rate_min, rate_max = 3.0, 4.0
        elif rating_range == 3:
            rate_min, rate_max = 2.0, 3.0
        elif rating_range == 2:
            rate_min, rate_max = 1.0, 2.0
        elif rating_range == 1:
            rate_min, rate_max = 0, 1.0

        # Define bus type condition
        if bus_type == "Sleeper":
            bus_type_option = "Bus_type LIKE '%Sleeper%'"
        elif bus_type == "Semi-sleeper":
            bus_type_option = "Bus_type LIKE '%Semi Sleeper%'"
        elif bus_type == "A/C":
            bus_type_option = "Bus_type LIKE '% A/C %'"
        elif bus_type == "NON A/C":
            bus_type_option = "Bus_type LIKE '% NON A/C%'"
        elif bus_type == "Seater":
            bus_type_option = "Bus_type LIKE '% Seater%'"
        else:
            bus_type_option = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-sleeper%' AND Bus_type NOT LIKE '%Seater%' AND Bus_type NOT LIKE '%A/C%' AND Bus_type NOT LIKE '%NON A/C%'"

        # Define fare range
        if fare_range == "50-1000":
            fare_min, fare_max = 50, 1000
        elif fare_range == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000

        # Define seat availability condition
        if seats == "0-10":
            seat_condition = "Seats_Available BETWEEN 0 AND 10"
        elif seats == "10-20":
            seat_condition = "Seats_Available BETWEEN 11 AND 20"
        elif seats == "20-30":
            seat_condition = "Seats_Available BETWEEN 21 AND 30"
        else:
            seat_condition = "Seats_Available >= 30"

        # Build the SQL query
        sql_query = f'''
            SELECT * FROM bus_details
            WHERE price BETWEEN {fare_min} AND {fare_max}
            AND route_name = %s
            AND {bus_type_option}
            AND Start_time >= %s
            AND star_rating BETWEEN {rate_min} AND {rate_max}
            AND {seat_condition}
            ORDER BY price, Start_time DESC
        '''

        my_cursor.execute(sql_query, (UPSRTC, time))  # Use parameterized query to prevent SQL injection
        out2 = my_cursor.fetchall()
        conn.close()

        # Convert query result to DataFrame
        df = pd.DataFrame(out2, columns=[
            "ID", "Bus_name", "Route_name", "Bus_type", "Start_time", "Duration", "End_time", "Ratings", "Price", "Seats_available", "Route_link"
        ])
        return df



    #9 Rajasthan
    if state=="Rajasthan":
        with col2:
            RSRTC=st.selectbox("List of routes",RSRTC)
        
        # Function to filter data from the SQL database
    def filter_data(bus_type, fare_range, rating_range, seats, APSRTC, time):
        conn = mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="Uma@1728", 
            database="RED_BUS_ROUTES", 
            auth_plugin='mysql_native_password'
        )
        my_cursor = conn.cursor()

        # Filtration for rating
        rate_min, rate_max = 0, 5  # Default range
        if rating_range == 5:
            rate_min, rate_max = 4.0, 5
        elif rating_range == 4:
            rate_min, rate_max = 3.0, 4.0
        elif rating_range == 3:
            rate_min, rate_max = 2.0, 3.0
        elif rating_range == 2:
            rate_min, rate_max = 1.0, 2.0
        elif rating_range == 1:
            rate_min, rate_max = 0, 1.0

        # Define bus type condition
        if bus_type == "Sleeper":
            bus_type_option = "Bus_type LIKE '%Sleeper%'"
        elif bus_type == "Semi-sleeper":
            bus_type_option = "Bus_type LIKE '%Semi Sleeper%'"
        elif bus_type == "A/C":
            bus_type_option = "Bus_type LIKE '% A/C %'"
        elif bus_type == "NON A/C":
            bus_type_option = "Bus_type LIKE '% NON A/C%'"
        elif bus_type == "Seater":
            bus_type_option = "Bus_type LIKE '% Seater%'"
        else:
            bus_type_option = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-sleeper%' AND Bus_type NOT LIKE '%Seater%' AND Bus_type NOT LIKE '%A/C%' AND Bus_type NOT LIKE '%NON A/C%'"

        # Define fare range
        if fare_range == "50-1000":
            fare_min, fare_max = 50, 1000
        elif fare_range == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000

        # Define seat availability condition
        if seats == "0-10":
            seat_condition = "Seats_Available BETWEEN 0 AND 10"
        elif seats == "10-20":
            seat_condition = "Seats_Available BETWEEN 11 AND 20"
        elif seats == "20-30":
            seat_condition = "Seats_Available BETWEEN 21 AND 30"
        else:
            seat_condition = "Seats_Available >= 30"

        # Build the SQL query
        sql_query = f'''
            SELECT * FROM bus_details
            WHERE price BETWEEN {fare_min} AND {fare_max}
            AND route_name = %s
            AND {bus_type_option}
            AND Start_time >= %s
            AND star_rating BETWEEN {rate_min} AND {rate_max}
            AND {seat_condition}
            ORDER BY price, Start_time DESC
        '''

        my_cursor.execute(sql_query, (RSRTC, time))  # Use parameterized query to prevent SQL injection
        out2 = my_cursor.fetchall()
        conn.close()

        # Convert query result to DataFrame
        df = pd.DataFrame(out2, columns=[
            "ID", "Bus_name", "Route_name", "Bus_type", "Start_time", "Duration", "End_time", "Ratings", "Price", "Seats_available", "Route_link"
        ])
        return df
