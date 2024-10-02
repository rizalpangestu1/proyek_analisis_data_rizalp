import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# Load the data
day_df = pd.read_csv("https://raw.githubusercontent.com/rizalpangestu1/belajar-analisis-data-python-rizal-dicoding/refs/heads/main/day_df_cleaned.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/rizalpangestu1/belajar-analisis-data-python-rizal-dicoding/refs/heads/main/hour_df_cleaned.csv")

# Convert 'dteday' to datetime for filtering
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Set page layout
st.set_page_config(layout="wide")

# Sidebar selection for different visualizations
visualization = st.sidebar.selectbox(
    "Choose Visualization",
    ["Overview", "Time Series - Working Day vs. Holiday", "Hourly Distribution - Hour Data", "Pie Chart - User Types", "Regression Analysis", "All Visualizations Combined"]
)

# Define a date range filter for each visualization except "Regression Analysis"
if visualization != "Regression Analysis":
    start_date = st.sidebar.date_input("Start Date", day_df['dteday'].min())
    end_date = st.sidebar.date_input("End Date", day_df['dteday'].max())
    
    # Validate the date input
    if start_date > end_date:
        st.error("Error: End Date must fall after Start Date.")
        st.stop()

    # Apply the filter to day_df and hour_df based on selected date range
    filtered_day_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & (day_df['dteday'] <= pd.to_datetime(end_date))]
    filtered_hour_df = hour_df[(hour_df['dteday'] >= pd.to_datetime(start_date)) & (hour_df['dteday'] <= pd.to_datetime(end_date))]
else:
    filtered_day_df = day_df
    filtered_hour_df = hour_df

# Pre-compute hourly distribution for all visualizations
hourly_usage_cnt = filtered_hour_df.groupby('hr')['cnt'].sum().reset_index()
hourly_usage_casual = filtered_hour_df.groupby('hr')['casual'].sum().reset_index()
hourly_usage_registered = filtered_hour_df.groupby('hr')['registered'].sum().reset_index()

# Overview of the datasets
if visualization == "Overview":
    st.title('Bike Sharing Data Dashboard 🚴')
    st.caption("Made by: Rizal Pangestu/rizal.pangestu0601@mail.ugm.ac.id/rizal-pangestu0601")
    st.image("https://github.com/rizalpangestu1/belajar-analisis-data-python-rizal-dicoding/blob/main/image1_hH9B4gs.width-1300.jpg?raw=true")
    st.caption("Source image: Google/Andrew Hyatt")
    st.write('''
        Bike sharing systems automate the process of bike rentals, allowing users to easily rent and return bikes at different locations.
        With over 500 programs globally, these systems are important for addressing traffic, environmental, and health issues.
        The data generated from bike sharing, such as travel duration and location details, makes it valuable for research,
        acting as a virtual sensor network to monitor city mobility and detect significant urban events.
    ''')
    st.write('''
        The bike-sharing rental patterns are closely linked to environmental and seasonal factors such as weather, precipitation,
        day of the week, season, and time of day. The dataset contains two years of historical records from the Capital Bikeshare
        system in Washington D.C. (2011-2012), available at the Capital Bikeshare website. The data has been aggregated into two-hour
        and daily intervals, with corresponding weather and seasonal details added, sourced from freemeteo.com.
    ''')

    st.header("Overview of Bike Sharing Datasets")
    st.subheader("📝 Notes: ")
    st.write("1. day.csv: Bike sharing counts aggregated on daily basis.")
    st.write("2. hour.csv: Bike sharing counts aggregated on hourly basis.")
    st.write(" ")
    st.write("📊 These are the first 5 rows of each dataset within the selected date range.")
    st.subheader("Day Data")
    st.write(filtered_day_df.head())

    st.subheader("Hour Data")
    st.write(filtered_hour_df.head())

# Line plot of bike usage
elif visualization == "Time Series - Working Day vs. Holiday":
    st.header("Trends of Bike Usage Over Time: Working Days vs Holidays")

    # Create line plot for bike usage over time
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.lineplot(x='dteday', y='cnt', hue='workingday', data=filtered_day_df, ax=ax)

    ax.set_xlabel('Date')
    ax.set_ylabel('Total Bike Usage (cnt)')
    ax.set_title('Trends of Bike Usage Over Time: Working Days vs Holidays')
    ax.legend(title='Working Day', labels=['Holiday', 'Working Day'])
    st.pyplot(fig)

# Bar plot for hourly distribution
elif visualization == "Hourly Distribution - Hour Data":
    st.header("Distribution of Bike Usage by Hour")
    
    # Plot cnt vs hr
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    sns.barplot(x='hr', y='cnt', data=hourly_usage_cnt, palette='YlOrRd', ax=ax1)
    ax1.set_xlabel('Hour of the Day')
    ax1.set_ylabel('Total Bike Rentals (cnt)')
    ax1.set_title('Distribution of Bike Rentals by Hour of the Day')
    ax1.set_xticks(range(0, 24))
    st.pyplot(fig1)

    # Plot casual vs hr
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.barplot(x='hr', y='casual', data=hourly_usage_casual, palette='YlGnBu', ax=ax2)
    ax2.set_xlabel('Hour of the Day')
    ax2.set_ylabel('Unregistered Bike Rentals (casual)')
    ax2.set_title('Distribution of Bike for Unregistered User Usage by Hour of the Day')
    ax2.set_xticks(range(0, 24))
    st.pyplot(fig2)

    # Plot registered vs hr
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    sns.barplot(x='hr', y='registered', data=hourly_usage_registered, palette='BuPu', ax=ax3)
    ax3.set_xlabel('Hour of the Day')
    ax3.set_ylabel('Registered Bike Rentals (registered)')
    ax3.set_title('Distribution of Bike for Registered User Usage by Hour of the Day')
    ax3.set_xticks(range(0, 24))
    st.pyplot(fig3)

# Pie chart for user type distribution
elif visualization == "Pie Chart - User Types":
    st.header("Distribution of Bike Usage Between Unregistered and Registered Bike Users")

    # Calculate the total usage by user type based on the filtered data
    usage_counts = [filtered_day_df['casual'].sum(), filtered_day_df['registered'].sum()]

    # Create pie chart
    fig4, ax4 = plt.subplots(figsize=(8, 8))
    ax4.pie(usage_counts, labels=['Unregistered', 'Registered'], autopct='%1.1f%%', colors=['orange', 'green'])
    ax4.set_title('Distribution of Bike Usage Between Unregistered and Registered Bike Users')
    st.pyplot(fig4)

# Regression analysis section without date filter
elif visualization == "Regression Analysis":
    st.header("Regression Analysis on Bike Usage and Weather Variables")

    # Create a copy of day_df to transform 'cnt' without affecting the original
    reg_day_df = day_df.copy()
    reg_day_df['cnt'] = np.log(reg_day_df['cnt'])

    # Define independent and dependent variables for the model
    independent_var = reg_day_df[['weathersit', 'temp', 'hum', 'windspeed']]
    dependent_var = reg_day_df['cnt']

    # Add a constant to the features for intercept
    independent_var_with_constant = sm.add_constant(independent_var)

    # Build the OLS regression model
    model = sm.OLS(dependent_var, independent_var_with_constant).fit()

    # Display the model summary
    st.subheader("OLS Regression Model Summary")
    st.text(model.summary())

    # Create scatter plots to visualize the relationship between weather conditions and bike rentals
    st.subheader("Scatter Plots of Weather Variables vs. Bike Rentals (Log-Transformed)")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Scatter plot for 'weathersit'
    axes[0, 0].scatter(reg_day_df['weathersit'], reg_day_df['cnt'], alpha=0.5)
    axes[0, 0].set_xlabel('Weathersit')
    axes[0, 0].set_ylabel('Total Bike Rentals (log(cnt))')
    axes[0, 0].set_title('Effect of Weather Situation on Bike Rentals')
    sns.regplot(x='weathersit', y='cnt', data=reg_day_df, scatter=False, ax=axes[0, 0], color='blue', line_kws={"linewidth": 1.5})

    # Scatter plot for 'temp'
    axes[0, 1].scatter(reg_day_df['temp'], reg_day_df['cnt'], alpha=0.5, color='orange')
    axes[0, 1].set_xlabel('Temperature')
    axes[0, 1].set_ylabel('Total Bike Rentals (log(cnt))')
    axes[0, 1].set_title('Effect of Temperature on Bike Rentals')
    sns.regplot(x='temp', y='cnt', data=reg_day_df, scatter=False, ax=axes[0, 1], color='blue', line_kws={"linewidth": 1.5})

    # Scatter plot for 'hum'
    axes[1, 0].scatter(reg_day_df['hum'], reg_day_df['cnt'], alpha=0.5, color='green')
    axes[1, 0].set_xlabel('Humidity')
    axes[1, 0].set_ylabel('Total Bike Rentals (log(cnt))')
    axes[1, 0].set_title('Effect of Humidity on Bike Rentals')
    sns.regplot(x='hum', y='cnt', data=reg_day_df, scatter=False, ax=axes[1, 0], color='blue', line_kws={"linewidth": 1.5})

    # Scatter plot for 'windspeed'
    axes[1, 1].scatter(reg_day_df['windspeed'], reg_day_df['cnt'], alpha=0.5, color='red')
    axes[1, 1].set_xlabel('Windspeed')
    axes[1, 1].set_ylabel('Total Bike Rentals (log(cnt))')
    axes[1, 1].set_title('Effect of Windspeed on Bike Rentals')
    sns.regplot(x='windspeed', y='cnt', data=reg_day_df, scatter=False, ax=axes[1, 1], color='blue', line_kws={"linewidth": 1.5})

    # Adjust layout and display the plots
    plt.tight_layout()
    st.pyplot(fig)

# Combined visualization section
elif visualization == "All Visualizations Combined":
    st.header("Bike Sharing Dashboard")

    # Add metrics for the mean of 'cnt', 'casual', and 'registered' for data day_df
    st.subheader("Metrics for day.csv Data")
    mean_cnt_day = filtered_day_df['cnt'].mean()
    mean_casual_day = filtered_day_df['casual'].mean()
    mean_registered_day = filtered_day_df['registered'].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Average Total Rentals (cnt) - Day Data", f"{mean_cnt_day:.2f}")
    col2.metric("Average Casual Rentals - Day Data", f"{mean_casual_day:.2f}")
    col3.metric("Average Registered Rentals - Day Data", f"{mean_registered_day:.2f}")

    # Add metrics for the mean of 'cnt', 'casual', and 'registered' for data hour_df
    st.subheader("Metrics for hour.csv Data")
    mean_cnt_hour = filtered_hour_df['cnt'].mean()
    mean_casual_hour = filtered_hour_df['casual'].mean()
    mean_registered_hour = filtered_hour_df['registered'].mean()

    col4, col5, col6 = st.columns(3)
    col4.metric("Average Total Rentals (cnt) - Hour Data", f"{mean_cnt_hour:.2f}")
    col5.metric("Average Casual Rentals - Hour Data", f"{mean_casual_hour:.2f}")
    col6.metric("Average Registered Rentals - Hour Data", f"{mean_registered_hour:.2f}")

    # Combined - Time Series
    st.subheader("Trends of Bike Usage Over Time: Working Days vs Holidays")
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.lineplot(x='dteday', y='cnt', hue='workingday', data=filtered_day_df, ax=ax)
    ax.set_xlabel('Date')
    ax.set_ylabel('Total Bike Usage (cnt)')
    ax.set_title('Trends of Bike Usage Over Time: Working Days vs Holidays')
    ax.legend(title='Working Day', labels=['Holiday', 'Working Day'])
    st.pyplot(fig)

    # Combined - Hourly Distribution
    st.subheader("Distribution of Bike Usage by Hour")
    col7, col8, col9 = st.columns(3)

    with col7:
        st.write("Total Rentals by Hour")
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        sns.barplot(x='hr', y='cnt', data=hourly_usage_cnt, palette='YlOrRd', ax=ax1)
        ax1.set_xlabel('Hour')
        ax1.set_ylabel('Total Rentals')
        ax1.set_title('Total Rentals by Hour')
        ax1.set_xticks(range(0, 24))
        st.pyplot(fig1)

    with col8:
        st.write("Casual Rentals by Hour")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.barplot(x='hr', y='casual', data=hourly_usage_casual, palette='YlGnBu', ax=ax2)
        ax2.set_xlabel('Hour')
        ax2.set_ylabel('Casual Rentals')
        ax2.set_title('Casual Rentals by Hour')
        ax2.set_xticks(range(0, 24))
        st.pyplot(fig2)

    with col9:
        st.write("Registered Rentals by Hour")
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        sns.barplot(x='hr', y='registered', data=hourly_usage_registered, palette='BuPu', ax=ax3)
        ax3.set_xlabel('Hour')
        ax3.set_ylabel('Registered Rentals')
        ax3.set_title('Registered Rentals by Hour')
        ax3.set_xticks(range(0, 24))
        st.pyplot(fig3)

    # Combined - Pie Chart
    st.subheader("Distribution of Bike Usage Between Unregistered and Registered Bike Users")
    usage_counts = [filtered_day_df['casual'].sum(), filtered_day_df['registered'].sum()]
    fig4, ax4 = plt.subplots(figsize=(8, 8))
    ax4.pie(usage_counts, labels=['Unregistered', 'Registered'], autopct='%1.1f%%', colors=['orange', 'green'])
    ax4.set_title('Distribution of Bike Usage Between Unregistered and Registered Bike Users')
    st.pyplot(fig4)

    # Create scatter plots to visualize the relationship between weather conditions and bike rentals
    st.subheader("Scatter Plots of Weather Variables vs. Bike Rentals (Log-Transformed)")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Scatter plot for 'weathersit'
    axes[0, 0].scatter(day_df['weathersit'], day_df['cnt'], alpha=0.5)
    axes[0, 0].set_xlabel('Weathersit')
    axes[0, 0].set_ylabel('Total Bike Rentals (log(cnt))')
    axes[0, 0].set_title('Effect of Weather Situation on Bike Rentals')
    sns.regplot(x='weathersit', y='cnt', data=day_df, scatter=False, ax=axes[0, 0], color='blue', line_kws={"linewidth": 1.5})

    # Scatter plot for 'temp'
    axes[0, 1].scatter(day_df['temp'], day_df['cnt'], alpha=0.5, color='orange')
    axes[0, 1].set_xlabel('Temperature')
    axes[0, 1].set_ylabel('Total Bike Rentals (log(cnt))')
    axes[0, 1].set_title('Effect of Temperature on Bike Rentals')
    sns.regplot(x='temp', y='cnt', data=day_df, scatter=False, ax=axes[0, 1], color='blue', line_kws={"linewidth": 1.5})

    # Scatter plot for 'hum'
    axes[1, 0].scatter(day_df['hum'], day_df['cnt'], alpha=0.5, color='green')
    axes[1, 0].set_xlabel('Humidity')
    axes[1, 0].set_ylabel('Total Bike Rentals (log(cnt))')
    axes[1, 0].set_title('Effect of Humidity on Bike Rentals')
    sns.regplot(x='hum', y='cnt', data=day_df, scatter=False, ax=axes[1, 0], color='blue', line_kws={"linewidth": 1.5})

    # Scatter plot for 'windspeed'
    axes[1, 1].scatter(day_df['windspeed'], day_df['cnt'], alpha=0.5, color='red')
    axes[1, 1].set_xlabel('Windspeed')
    axes[1, 1].set_ylabel('Total Bike Rentals (log(cnt))')
    axes[1, 1].set_title('Effect of Windspeed on Bike Rentals')
    sns.regplot(x='windspeed', y='cnt', data=day_df, scatter=False, ax=axes[1, 1], color='blue', line_kws={"linewidth": 1.5})

    # Adjust layout and display the plots
    plt.tight_layout()
    st.pyplot(fig)

# Caption for references
st.caption('''References:
    Fanaee-T, Hadi, and Gama, Joao, "Event labeling combining ensemble detectors and background knowledge", 
    Progress in Artificial Intelligence (2013): pp. 1-15, Springer Berlin Heidelberg, doi:10.1007/s13748-013-0040-3.
''')