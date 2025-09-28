import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

# ---------- DB CONNECTION ---------- #
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="123456",
            database="olaride_db"
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Database connection error: {err}")
        return None

def run_query(query):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            data = cursor.fetchall()
            cols = [desc[0] for desc in cursor.description]
            return pd.DataFrame(data, columns=cols)
        except Exception as e:
            st.error(f"❌ Query failed: {e}")
            return pd.DataFrame()
        finally:
            conn.close()
    return pd.DataFrame()


# ---------- PREDEFINED QUERIES ---------- #
queries = {
    "1. Retrieve all successful bookings":
        "SELECT * FROM ola_dataset WHERE Booking_Status = 'Success';",

    "2. Find the average ride distance for each vehicle type":
        "SELECT Vehicle_Type, AVG(Ride_Distance) AS avg_ride_distance FROM ola_dataset GROUP BY Vehicle_Type;",

    "3. Get the total number of cancelled rides by customers":
        "SELECT SUM(Canceled_Rides_by_Customer) AS total_cancelled_by_customers FROM ola_dataset;",

    "4. Top 5 customers by number of rides":
        "SELECT Customer_ID, COUNT(Booking_ID) AS total_rides FROM ola_dataset GROUP BY Customer_ID ORDER BY total_rides DESC LIMIT 5;",

    "5. Incomplete rides due to vehicle/personal issues":
        '''SELECT Incomplete_Rides_Reason, 
       COUNT(Canceled_Rides_by_Driver) AS total_cancelled_by_driver
FROM ola_dataset
WHERE Incomplete_Rides_Reason in ('Vehicle Breakdown','Customer Demand')
GROUP BY Incomplete_Rides_Reason;''',
    "6. Max & Min driver ratings for Prime Sedan":
        "SELECT Vehicle_Type, MAX(CAST(Driver_Ratings AS DECIMAL(3,1))) AS max_rating, MIN(CAST(Driver_Ratings AS DECIMAL(3,1))) AS min_rating FROM ola_dataset WHERE Vehicle_Type = 'Prime Sedan';",

    "7. Count rides paid using UPI":
        "SELECT COUNT(*) AS total_upi_rides FROM ola_dataset WHERE Payment_Method = 'UPI';",

    "8. Avg customer rating per vehicle type":
        "SELECT Vehicle_Type, AVG(Customer_Rating) AS avg_rating FROM ola_dataset GROUP BY Vehicle_Type;",

    "9. Total booking value of successful rides":
        "SELECT SUM(Booking_Value) AS total_booking_value FROM ola_dataset WHERE Booking_Status = 'Success';",

    "10. List all incomplete rides with reason":
        "SELECT Incomplete_Rides, Incomplete_Rides_Reason FROM ola_dataset WHERE Incomplete_Rides = 'Yes';"
}


# ---------- STREAMLIT APP ---------- #
st.title("🚖 Ola Ride Insights - SQL Playground")

menu = ["Run Custom Query", "Predefined Queries", "CRUD Operations"]
choice = st.sidebar.radio("Choose an Option", menu)


# ---- CUSTOM QUERY ----
if choice == "Run Custom Query":
    query = st.text_area("Write your SQL query:", "SELECT * FROM ola_dataset LIMIT 10;")
    if st.button("Run Custom Query"):
        df = run_query(query)
        if not df.empty:
            st.dataframe(df)
        else:
            st.warning("No results found.")


# ---- PREDEFINED QUERIES ----
elif choice == "Predefined Queries":
    st.subheader("📊 Choose a Predefined Query")
    selected_query = st.selectbox("Select Query", list(queries.keys()))

    if st.button("Run Selected Query"):
        query = queries[selected_query]
        df = run_query(query)
        if not df.empty:
            st.dataframe(df)
        else:
            st.warning("No results found.")


# ---- CRUD OPERATIONS ----
elif choice == "CRUD Operations":
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [t[0] for t in cursor.fetchall()]
        conn.close()

        selected_table = st.selectbox("Select Table", tables)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"DESCRIBE {selected_table}")
        columns = [col[0] for col in cursor.fetchall()]

        operation = st.radio("Select Operation", ["Create", "Read", "Update", "Delete"])

        # ---- CREATE ----
        if operation == "Create":
            st.subheader(f"Insert into {selected_table}")
            values = []
            for col in columns:
                val = st.text_input(f"Enter {col}")
                values.append(val)
            if st.button("Insert"):
                placeholders = ", ".join(["%s"] * len(values))
                sql = f"INSERT INTO {selected_table} ({', '.join(columns)}) VALUES ({placeholders})"
                cursor.execute(sql, tuple(values))
                conn.commit()
                st.success("✅ Record inserted successfully")

        # ---- READ ----
        elif operation == "Read":
            st.subheader(f"View data from {selected_table}")
            df = run_query(f"SELECT * FROM {selected_table}")
            st.dataframe(df)

        # ---- UPDATE ----
        elif operation == "Update":
            st.subheader(f"Update {selected_table}")
            id_col = columns[0]
            record_id = st.text_input(f"Enter {id_col} of record to update")
            updates = {}
            for col in columns[1:]:
                new_val = st.text_input(f"New {col} (leave blank to skip)")
                if new_val:
                    updates[col] = new_val
            if st.button("Update"):
                set_clause = ", ".join([f"{col}=%s" for col in updates.keys()])
                sql = f"UPDATE {selected_table} SET {set_clause} WHERE {id_col}=%s"
                cursor.execute(sql, tuple(updates.values()) + (record_id,))
                conn.commit()
                st.success("✅ Record updated successfully")

        # ---- DELETE ----
        elif operation == "Delete":
            st.subheader(f"Delete from {selected_table}")
            id_col = columns[0]
            record_id = st.text_input(f"Enter {id_col} of record to delete")
            if st.button("Delete"):
                sql = f"DELETE FROM {selected_table} WHERE {id_col}=%s"
                cursor.execute(sql, (record_id,))
                conn.commit()
                st.success("Record deleted successfully")

        conn.close()

import streamlit as st

st.title("🚖 Ola Ride Insights - Dashboard Preview")

# Dictionary mapping pages to images
dashboard_images = {
    "Overview": "C:/Users/shrut/Pictures/Screenshots/dasboard_overview.png",
    "Booking Status Breakdown": "C:/Users/shrut/Pictures/Screenshots/piecart.png",
    "Top 5 vehicle by ride distance": "C:/Users/shrut/Pictures/Screenshots/Screenshot 2025-09-25 124221.png",
    "Average Customer Ratings": "C:/Users/shrut/Pictures/Screenshots/Screenshot 2025-09-25 124328.png",
    "Total Ride": "C:/Users/shrut/Pictures/Screenshots/Screenshot 2025-09-25 124548.png",
    "Total Revenue": "C:/Users/shrut/Pictures/Screenshots/Screenshot 2025-09-25 155821.png",
    "Total Revenue": "C:/Users/shrut/Pictures/Screenshots/Screenshot 2025-09-25 155821.png",
    "Revenue per Ride": "C:/Users/shrut/Pictures/Screenshots/Screenshot 2025-09-25 160100.png",
    "Revenue per Ride": "C:/Users/shrut/Pictures/Screenshots/Screenshot 2025-09-25 160100.png",
    "Ride Volume Over Time": "C:/Users/shrut/Pictures/Screenshots/Screenshot 2025-09-25 160302.png",
    "Average of Customer_Rating by Vehicle_Type": "C:/Users/shrut/Pictures/Screenshots/Screenshot 2025-09-25 160554.png",
    "Dashboard filtered by Booking Status": "C:/Users/shrut/Pictures/Screenshots/Screenshot 2025-09-26 134636.png"

}

# Sidebar menu to select dashboard page
selected_page = st.sidebar.selectbox("Select Dashboard Page:", list(dashboard_images.keys()))

# Display the selected dashboard image
st.image(dashboard_images[selected_page], caption=f"Dashboard - {selected_page}", use_container_width=True)


#st.title("📊 Ola Ride Analytics Dashboard (Power BI Preview)")

# Show Power BI dashboard images
#st.image("C:\\Users\\shrut\Pictures\\Screenshots\\dasboard_overview.png", caption="Dashboard - Page 1", use_column_width=True)
#st.image("assets/dashboard_page2.png", caption="Dashboard - Page 2", use_column_width=True)
#st.image("C:\\Users\\shrut\\Pictures\\Screenshots\\piecart.png", caption="Dashboard - Page 1", use_column_width=True)

# If you exported PDF instead of images
#st.download_button("Download Dashboard PDF", "assets/dashboard.pdf", file_name="Ola_Ride_Dashboard.pdf")

import streamlit as st

# --- Apply Light Theme Styles Globally ---
def apply_global_styles():
    st.markdown(
        """
        <style>
        /* Set app background */
        .stApp {
            background-color: #ffffff !important; /* White background */
            color: #1a1a1a !important;           /* Dark text */
        }

        /* Input fields and text areas */
        .stTextInput > div > div > input,
        .stNumberInput input,
        .stTextArea textarea,
        .stSelectbox > div > div {
            background-color: #fff !important;
            color: #000 !important;
            border: 1px solid #ccc !important;
            border-radius: 6px !important;
            padding: 6px !important;
        }

        /* Radio button labels */
        .stRadio label {
            color: #1a1a1a !important;
            font-weight: 500;
        }

        /* Buttons */
        div.stButton > button {
            background-color: #28a745 !important;  /* Green */
            color: white !important;
            border-radius: 6px !important;
            padding: 8px 20px !important;
            font-weight: bold !important;
            border: none;
        }
        div.stButton > button:hover {
            background-color: #218838 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

