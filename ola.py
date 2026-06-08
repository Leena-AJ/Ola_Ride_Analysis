import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import pymysql

def get_connection():
    return pymysql.connect(
    host="localhost",               
    user="root",            
    password="Aro788n4",              
    database="Ola_dataset"  
    )

def execute_query(query):
    conn = get_connection()
    df = pd.read_sql(query,conn)
    conn.close()
    return df

page = st.sidebar.radio(
    "Ola Ride Analytics",
    ["Overview", "Insights"]
)   

if page == "Overview":

    st.title("Ola Ride Analytics")
    st.header("Dashboard Overview")

    TOTAL_RIDES = execute_query("""
    SELECT COUNT(*) AS TOTAL_RIDES
    FROM Ola_dataset
    """).iloc[0,0]

    SUCCESSFULL_RIDES = execute_query("""
    SELECT COUNT(*) AS SUCCESSFULL_RIDES
    FROM Ola_dataset
    WHERE Booking_Status = 'Success'                                  
    """).iloc[0,0]

    INCOMPLETE_RIDES = execute_query("""
    SELECT COUNT(*)
    FROM Ola_dataset
    WHERE Incomplete_Rides = 'Yes'                                                            
    """).iloc[0,0]

    MOST_BOOKED_VEHICLE_TYPE = execute_query("""
    SELECT Vehicle_Type
    FROM Ola_dataset 
    GROUP BY Vehicle_Type
    ORDER BY COUNT(*) DESC
    LIMIT 1
    """).iloc[0,0]


    col1, col2, col3 = st.columns(3)

    col1.metric("TOTAL RIDES ", f"{TOTAL_RIDES :,}")
    col2.metric("SUCCESSFULL RIDES", f"{int(SUCCESSFULL_RIDES):,}")
    col3.metric("INCOMPLETE RIDES ",f"{int(INCOMPLETE_RIDES):,}")

    st.info(f"MOST BOOKED VEHICLE TYPE: {MOST_BOOKED_VEHICLE_TYPE}")

elif page == "Insights":

    st.title("Ola Ride Analytics")
    st.header("SQL Insights")

    queries = {
    "Successfull Bookings": """
    select Booking_Status,count(*) 
    from Ola_dataset
    where Booking_Status = 'Success';
    """,

    "Average ride distance for each vehicle type": """
    select Vehicle_Type,avg(Ride_Distance) as Avg_Ride_Distance
    from Ola_dataset
    Group By Vehicle_Type;
    """,

    "Total number of cancelled rides by customers": """
    select Canceled_Rides_by_Customer,count(*)
    from Ola_dataset
    where Canceled_Rides_by_Customer != 'Not Cancelled By Customer'
    group by Canceled_Rides_by_Customer;
    """,

    "Top 5 customers who booked the highest number of rides": """
    select Customer_ID,count(*) as No_of_rides
    from Ola_dataset                   
    Group By Customer_ID
    order by No_of_rides desc
    limit 5; 
    """,

    "The number of rides cancelled by drivers due to personal and car-related issues": """
    select Canceled_Rides_by_Driver,count(*) as No_of_rides
    from Ola_dataset
    where Canceled_Rides_by_Driver = 'Personal & Car related issue'                  
    Group By Canceled_Rides_by_Driver
    ; 
    """,

    "The maximum and minimum driver ratings for Prime Sedan bookings": """
    select Vehicle_Type,max(Driver_Ratings) as Max_rating,min(Driver_Ratings) as Min_rating
    from Ola_dataset
    where Vehicle_Type= 'Prime Sedan' ;
    """,

    "All rides where payment was made using UPI": """
    select Booking_ID,Payment_Method
    from Ola_dataset
    where Payment_Method= 'UPI'                  
    ; 
    """,

    
    "The average customer rating per vehicle type": """
    select Vehicle_Type,round(avg(Customer_Rating),2) as avg_rating
    from Ola_dataset
    group by Vehicle_Type
    order by avg_rating desc                                    
    ; 
    """,

    "Total booking value of rides completed successfully": """
    select Booking_Status,sum(Booking_Value) as Total_booking_value
    from Ola_dataset
    where Booking_Status ='Success'                                                     
    ; 
    """,

    "All incomplete rides along with the reason": """
    select Booking_ID,Incomplete_Rides,Incomplete_Rides_Reason 
    from Ola_dataset
    where Incomplete_Rides = 'Yes'                                                 
    ; 
    """
    }


    selected_query = st.selectbox("Select a query:",list(queries.keys()))

    if st.button("Run Query"):
        with st.spinner("Fetching Data..."):
            df = execute_query(queries[selected_query])
            st.success("Query executed successfully")

            if selected_query =="All Successfull Bookings":
                st.info("Out of total bookings,63967 are successfull")

            elif selected_query ==" Average ride distance for each vehicle type":
                st.info("Among the six vehicles,Prime sedan has covered more distance and Auto has covered the least")

            elif selected_query ==" Total number of cancelled rides by customers":
                st.info("Out of 13024 bookings,10499 rides have been cancelled by the customers")

            elif selected_query =="Top 5 customers who booked the highest number of rides":
                st.info("These are the five customers who have booked more number of rides")

            elif selected_query =="The number of rides cancelled by drivers due to personal and car-related issues":
                st.info("About 6k rides have been cancelled by drivers for personal and car related")

            elif selected_query =="The maximum and minimum driver ratings for Prime Sedan bookings":
                st.info("Drivers have given maximum of 5 for this particular booking")

            elif selected_query =="All rides where payment was made using UPI":
                st.info("Out of total bookings,25881 payments are made by UPI")

            elif selected_query =="The average customer rating per vehicle type":
                st.info("Out of all ,Prime Sedan has been rated highest and Prime SUV has scored least rating")

            elif selected_query =="Total booking value of rides completed successfully":
                st.info("3,50,80,467 is the total value for all the completed rides")  

            elif selected_query =="All incomplete rides along with the reason":
                st.info("Totally there are 3926 incomplete rides with various reasons")          

            st.dataframe(df)      

            st.subheader("Power BI Dashboard")

            st.link_button(
            "Open Power BI Dashboard",
            "https://app.powerbi.com/reportEmbed?reportId=61bafb81-2b94-4448-81f1-d22ab7dabc5a&autoAuth=true&ctid=220a3f1b-1bd1-4767-895e-a92a6ffb9530",
            )