# Importing Libraries
import json
import os
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import plotly.express as px

import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
   
)

print(mydb)
mycursor = mydb.cursor(buffered=True)

mycursor.execute("USE phonepe")

# Setting up page configuration
img=Image.open("C:\\Users\\Admin\\Desktop\\vscode\\phonepe pulse project\\phonepe-logo-icon.png")
st.set_page_config(page_title="PhonePe Pulse", page_icon=img, layout="wide", )
icons = {
    "Home": "🏠",
    "Basic insights": "🔄",
    "Top Charts" :"📈",              
    "ABOUT": "📊",
    "Readme":"👥"
}
SELECT = st.sidebar.selectbox("Choose an option", list(icons.keys()), format_func=lambda option: f'{icons[option]} {option}', key='selectbox')

# MENU 1 - HOME
if SELECT == "Home":
    col1,col2 = st.columns(2)
    col1.image(Image.open("C:\\Users\\Admin\\Desktop\\vscode\\phonepe pulse project\\phonepe-logo-icon.png"),width = 300)
    with col1:
        st.subheader("PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
          st.video("C:\\Users\\Admin\\Desktop\\vscode\\phonepe pulse project\\upi.mp4")


# MENU 2 - Basic insights:
if SELECT == "Basic insights":
    st.title("BASIC INSIGHTS")
    st.write("----")
    st.subheader("Let's know some basic insights about the data")
    options = ["--select--",
               "1. Top 10 states based on year and amount of transaction",
               "2. Least 10 states based on type and amount of transaction",
               "3. Top 10 mobile brands based on percentage of transaction",
               "4. Least 10 mobile brands based on percentage of transaction",
               "5. Top 10 Registered-users based on States and District",
               "6. Least 10 registered-users based on Districts and states",
               "7. Top 10 Districts based on states and amount of transaction",
               "8. Least 10 Districts based on states and amount of transaction",
               "9. Top 10 Districts based on states and registeredUsers",
               "10. Least 10 Districts based on states and registeredUsers"]
    SELECTED = st.selectbox("Select the option",options)
    

    if SELECTED=="1. Top 10 states based on year and amount of transaction":
        mycursor.execute("SELECT  State, Year, SUM(top_amount) AS Total_Transaction_Amount FROM top_transaction GROUP BY State, Year ORDER BY Total_Transaction_Amount DESC LIMIT 10")
        df = pd.DataFrame(mycursor.fetchall(),columns=['State','Year','top_amount'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 states based on type and amount of transaction")
            
            st.bar_chart(data=df,x="State",y="top_amount")
            
            fig = px.sunburst(df, path=['State', 'top_amount' ], title='"Top 10 states based on type and amount of transaction"')
            st.plotly_chart(fig)

    elif SELECTED=="2. Least 10 states based on type and amount of transaction":
        mycursor.execute("SELECT DISTINCT State, SUM(top_count) as Total FROM top_transaction GROUP BY State ORDER BY Total ASC LIMIT 10")
        df = pd.DataFrame(mycursor.fetchall(),columns=['State','top_amount'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Least 10 states based on type and amount of transaction")
            fig = px.bar(df, x='State', y='top_amount', title="Top 10 states based on type and amount of transaction")
            st.plotly_chart(fig)
            fig = px.sunburst(df, path=['State', 'top_amount' ], title='"Least 10 states based on type and amount of transaction"')
            st.plotly_chart(fig)

    elif SELECTED=="3. Top 10 mobile brands based on percentage of transaction":
        mycursor.execute("SELECT DISTINCT user_brand,SUM(user_percentage) as Total_Percentage FROM aggregated_user GROUP BY user_brand ORDER BY Total_Percentage DESC LIMIT 10")
        df = pd.DataFrame(mycursor.fetchall(),columns=['user_brand','user_percentage'])
        col1,col2 = st.columns(2)
    
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 mobile brands based on percentage of transaction")
            st.bar_chart(data=df,x="user_brand",y="user_percentage")

            fig = px.sunburst(df, path=['user_brand', 'user_percentage' ], title='"Top 10 mobile brands based on percentage of transaction"')
            st.plotly_chart(fig)
            fig_scatter = px.scatter(df, x='user_brand', y='user_percentage', title="Top 10 mobile brands based on percentage of transaction")
            st.plotly_chart(fig_scatter)

    elif SELECTED=="4. Least 10 mobile brands based on percentage of transaction":
        mycursor.execute("SELECT DISTINCT user_brand,SUM(user_percentage) as Total_Percentage FROM aggregated_user GROUP BY user_brand ORDER BY Total_Percentage ASC LIMIT 10")
        df = pd.DataFrame(mycursor.fetchall(),columns=['user_brand','user_percentage'])
        st.title("Least 10 mobile brands based on percentage of transaction")
        col1,col2 = st.columns(2)
    
        with col1:
            st.write(df)
        with col2:
            st.title("Least 10 mobile brands based on percentage of transaction")
            fig = px.bar(df, x='user_brand', y='user_percentage', title="Least 10 mobile brands based on percentage of transaction")
            st.plotly_chart(fig)

            fig = px.sunburst(df, path=['user_brand', 'user_percentage' ], title='"Least 10 mobile brands based on percentage of transaction"')
            st.plotly_chart(fig)
            fig_scatter = px.scatter(df, x='user_brand', y='user_percentage', title="Least 10 mobile brands based on percentage of transaction")
            st.plotly_chart(fig_scatter)

    elif SELECTED=="5. Top 10 Registered-users based on States and District":
        mycursor.execute("SELECT DISTINCT State,district_pincode,SUM(registeredUsers) as Users FROM top_user GROUP BY State ORDER BY Users DESC LIMIT 10")
        df = pd.DataFrame(mycursor.fetchall(),columns=['State','district_pincode','registeredUsers'])

        st.title("Top 10 Registered-users based on States and district_pincode")
        col1,col2 = st.columns(2)
    
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 Registered-users based on States and district_pincode")
            fig = px.bar(df, x='district_pincode', y='registeredUsers', title="Top 10 Registered-users based on States and district_pincode")
            st.plotly_chart(fig)

            fig1 = px.sunburst(df, path=['district_pincode', 'registeredUsers' ], title='"Top 10 Registered-users based on States and district_pincode"')
            st.plotly_chart(fig1)

    elif SELECTED=="6. Least 10 registered-users based on Districts and states":
        mycursor.execute("SELECT DISTINCT State,district_pincode,SUM(registeredUsers) AS Users FROM top_user GROUP BY State,district_pincode ORDER BY Users ASC LIMIT 10")
        df = pd.DataFrame(mycursor.fetchall(),columns=['State','district_pincode','registeredUsers'])
        st.title("Least 10 registered-users based on Districts and states")
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Least 10 registered-users based on Districts and states")
            fig = px.bar(df, x='district_pincode', y='registeredUsers', title="Least 10 registered-users based on Districts and states")
            st.plotly_chart(fig)

            fig1 = px.sunburst(df, path=['district_pincode', 'registeredUsers' ], title='"Least 10 registered-users based on Districts and states"')
            st.plotly_chart(fig1)

    elif SELECTED=="7. Top 10 Districts based on states and amount of transaction":
        mycursor.execute("SELECT DISTINCT State,district_pincode,SUM(top_amount) AS Total  FROM top_transaction GROUP BY State,district_pincode ORDER BY Total  ASC LIMIT 10")
        df = pd.DataFrame(mycursor.fetchall(),columns=['State','district_pincode','top_amount'])
        st.title("Top 10 Districts based on states and amount of transaction")
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 Districts based on states and amount of transaction")
            fig = px.bar(df, x='district_pincode', y='top_amount', title="Top 10 Districts based on states and amount of transaction")
            st.plotly_chart(fig)

            fig1 = px.sunburst(df, path=['district_pincode', 'top_amount' ], title='"Top 10 Districts based on states and amount of transaction"')
            st.plotly_chart(fig1)


    elif SELECTED=="8. Least 10 Districts based on states and amount of transaction":
        mycursor.execute("SELECT DISTINCT State,district_pincode,SUM(top_amount) as Total FROM top_transaction GROUP BY State,district_pincode ORDER BY Total ASC LIMIT 10")
        df = pd.DataFrame(mycursor.fetchall(),columns=['State','district_pincode','top_amount'])
        st.title("Least 10 Districts based on states and amount of transaction")
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Least 10 Districts based on states and amount of transaction")
            fig = px.bar(df, x='district_pincode', y='top_amount', title="Least 10 Districts based on states and amount of transaction")
            st.plotly_chart(fig)

            fig1 = px.sunburst(df, path=['district_pincode', 'top_amount' ], title='"Least 10 Districts based on states and amount of transaction"')
            st.plotly_chart(fig1)


    elif SELECTED=="9. Top 10 Districts based on states and registeredUsers":
        mycursor.execute("SELECT DISTINCT State,district,SUM(registeredUsers) AS Total FROM map_user GROUP BY State,district ORDER BY Total DESC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(),columns=['State','district','registeredUsers'])
        st.title("Top 10 Districts based on states and registeredUsers")
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 Districts based on states and registeredUsers")
            fig = px.bar(df, x='district', y='registeredUsers', title="Top 10 Districts based on states and registeredUsers")
            st.plotly_chart(fig)

            fig1 = px.sunburst(df, path=['district', 'registeredUsers' ], title='"Top 10 Districts based on states and registeredUsers"')
            st.plotly_chart(fig1)


    elif SELECTED=="10. Least 10 Districts based on states and registeredUsers":
        mycursor.execute("SELECT DISTINCT State,district,SUM(registeredUsers) as Total FROM map_user GROUP BY State,district ORDER BY Total ASC LIMIT 10")
        df = pd.DataFrame(mycursor.fetchall(),columns=['State','district','registeredUsers'])
        st.title("Least 10 Districts based on states and registeredUsers")
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Least 10 Districts based on states and registeredUsers")
            fig = px.bar(df, x='district', y='registeredUsers', title="Least 10 Districts based on states and registeredUsers")
            st.plotly_chart(fig)

            fig1 = px.sunburst(df, path=['district', 'registeredUsers' ], title='"Least 10 Districts based on states and registeredUsers"')
            st.plotly_chart(fig1)


# MENU 3 - TOP CHARTS            
if SELECT == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)

    with colum2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """,icon="🔍"
            )
        
    # Top Charts - TRANSACTIONS    
    if Type == "Transactions":
        col1,col2,col3 = st.columns([1,1,1],gap="small")

        with col1:
            st.markdown("### :violet[State]")
            mycursor.execute(f"SELECT State, SUM(Transaction_count) as Total_Transactions_Count, SUM(Transaction_amount) as Total FROM aggregated_transaction WHERE Year = '{Year}' AND Quarter = '{Quarter}' GROUP BY State ORDER BY Total DESC LIMIT 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transaction_count','Transaction_amount'])
            fig = px.pie(df, values='Transaction_amount',
                            names='State',
                            title='Top 10',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Transaction_count'],
                            labels={'Transaction_count':'Transaction_count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        with col2:
                st.markdown("### :violet[District]")
                mycursor.execute(f"SELECT district , SUM(map_count) as Total_Count, SUM(map_amount) as Total from map_transaction WHERE Year = '{Year}' AND Quarter = '{Quarter}' GROUP BY district ORDER BY Total DESC LIMIT 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'map_count','map_amount'])

                fig = px.pie(df, values='map_amount',
                                names='District',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['map_count'],
                                labels={'map_count':'map_count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)

        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(f"SELECT district_pincode, SUM(top_count) as Total_Transactions_Count, SUM(top_amount) as Total from top_transaction WHERE Year = '{Year}' AND Quarter = '{Quarter}' GROUP BY district_pincode ORDER BY Total DESC LIMIT 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['district_pincode', 'top_count','top_amount'])
            fig = px.pie(df, values='top_amount',
                                names='district_pincode',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['top_count'],
                                labels={'top_count':'top_count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

    # Top Charts - USERS          
    if Type == "Users":
        col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")
        
        with col1:
            st.markdown("### :violet[Brands]")
            if Year == 2022 and Quarter in [2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
            else:
                mycursor.execute(f"SELECT user_brand, SUM(user_count) AS Total_Count, AVG(user_percentage)*100 AS Avg_Percentage FROM aggregated_user WHERE Year = '{Year}' AND Quarter = '{Quarter}' GROUP BY user_brand order by Total_Count DESC LIMIT 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['user_brand', 'user_count','Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10',
                             x="user_count",
                             y="user_brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)   

        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"SELECT district, SUM(RegisteredUserS) as Total_Users FROM map_user WHERE Year = '{Year}' AND Quarter = '{Quarter}' GROUP BY district ORDER BY Total_Users DESC LIMIT 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)                        

        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(f"SELECT district_pincode, SUM(registeredUsers) AS Total_Users FROM top_user WHERE Year = '{Year}' AND Quarter = '{Quarter}' GROUP BY district_pincode ORDER BY Total_Users DESC LIMIT 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['district_pincode', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='district_pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        with col4:
            st.markdown("### :violet[State]")
            mycursor.execute(f"SELECT State, SUM(registeredUsers) AS Total_Users  FROM map_user WHERE Year = '{Year}' AND Quarter = '{Quarter}' GROUP BY State ORDER BY Total_Users DESC LIMIT 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users'])
            fig = px.pie(df, values='Total_Users',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Users'],
                             labels={'Total_Users':'Total_Users'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

# MENU 4 - ABOUT  
if SELECT == "ABOUT":
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("")
        st.markdown("") 
        st.markdown("")
        st.markdown("")
        st.markdown("")              
        st.video("C:\\Users\\Admin\\Desktop\\vscode\\phonepe pulse project\\phonepe video_ (1080p).mp4")
        st.image(Image.open("C:\\Users\\Admin\\Desktop\\vscode\\phonepe pulse project\\phonepe-logo-icon.png"),width = 200)
        st.write("---")
        st.subheader("The Indian digital payments story has truly captured the world's imagination."
                " From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and state-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government."
                " Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. "
                "PhonePe Pulse is our way of giving back to the digital payments ecosystem.")
    st.write("---")
    st.title("THE BEAT OF PHONEPE")
    col1,col2 = st.columns(2)    
    with col1:        
        st.write("---")
        st.subheader("Third ET BFSI Innovation Tribe Virtual Summit & Awards")
        st.image(Image.open("C:\\Users\\Admin\\Desktop\\vscode\\phonepe pulse project\\phonepe award img.jpg"),width = 300)
    with col2:
        st.write("---")
        st.subheader("Phonepe became a leading digital payments company")
        st.image(Image.open("C:\\Users\\Admin\\Desktop\\vscode\\phonepe pulse project\\phonepe img.jpg"),width = 500)

# MENU 5 - Readme
if SELECT=="Readme":
    st.title('Phonepe Pulse Data Visualization and Exploration:A User-Friendly Tool Using Streamlit and Plotly')
    st.subheader('Problem Statement')
    st.caption('The Phonepe pulse Github repository contains a large amount of data related to various metrics and statistics.' 
               'The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.' 
               'Extract data from the Phonepe pulse Github repository through scripting and clone it.' 
               'Transform the data into a suitable format and perform any necessary cleaning and pre-processing steps.' 
               'Insert the transformed data into a MySQL database for efficient storage and retrieval.'
               'Create a live geo visualization dashboard using Streamlit and Plotly in Python to display the data in an interactive and visually appealing manner.'
                'Fetch the data from the MySQL database to display in the dashboard.'
                'Provide at least 10 different dropdown options for users to select different facts and figures to display on the dashboard.'
                'The solution must be secure, efficient, and user-friendly.'
                'The dashboard must be easily accessible and provide valuable insights and information about the data in the Phonepe pulse Github repository.')

    st.subheader('Technology Stack Used')

    st.text('1.Python.')
    st.text('2.JSON.')
    st.text('3.MY SQL.')
    st.text('4.OS.')
    st.text('5.Pandas Library.')
    st.text('6.Streamlit.') 
    st.text('7.Plotly Library.')
    st.text('8.image Library.')

    st.subheader('Approach')

    st.caption('1. Data extraction: Clone the Github using scripting to fetch the data from the Phonepe pulse Github repository and store it in a suitable format such as CSV or JSON.')
    
    st.caption('2.Data transformation: Use a scripting language such as Python, along with libraries such as Pandas, to manipulate and pre-process the data. This may include cleaning the data, handling missing values, and transforming the data into a format suitable for analysis and visualization.')           
    
    st.caption('3. Database insertion: Use the "mysql-connector-python" library in Python to connect to a MySQL database and insert the transformed data using SQL commands.')           
    
    st.caption('''4. Dashboard creation: Use the Streamlit and Plotly libraries in Python to create
                    an interactive and visually appealing dashboard. Plotly's built-in geo map
                    functions can be used to display the data on a map and Streamlit can be used
                    to create a user-friendly interface with multiple dropdown options for users to
                    select different facts and figures to display.''')           
    st.caption('''5. Data retrieval: Use the "mysql-connector-python" library to connect to the
                    MySQL database and fetch the data into a Pandas dataframe. Use the data in
                    the dataframe to update the dashboard dynamically.''')          

    st.caption('''6. Deployment: Ensure the solution is secure, efficient, and user-friendly. Test
                        the solution thoroughly and deploy the dashboard publicly, making it
                        accessible to users.''')
    
    st.caption('''7. This approach leverages the power of Python and its numerous libraries to extract,
                    transform, and analyze data, and to create a user-friendly dashboard for visualizing
                    the insights obtained from the data.''')