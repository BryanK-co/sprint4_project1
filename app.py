
# app.py

def main():
    print("Hello, World!")



import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Read the dataset's CSV file into a Pandas DataFrame
#df = pd.read_csv('vehicles_us.csv') 
vehicles = pd.read_csv('vehicles_us.csv')

# Create a header
st.header("My 1st Streamlit App")



if __name__ == "__main__":
    main()


# Fill missing 'odometer' values for vehicles ten years old or less with the mean for that group
mean_odometer_younger = vehicles.loc[vehicles['model_year'] >= 2013, 'odometer'].mean()
vehicles.loc[vehicles['model_year'] >= 2013, 'odometer'] = vehicles.loc[vehicles['model_year'] >= 2013, 'odometer'].fillna(mean_odometer_younger)

# Fill missing 'odometer' values for vehicles 11 years old or more with the mean for that group
mean_odometer_older = vehicles.loc[vehicles['model_year'] < 2013, 'odometer'].mean()
vehicles.loc[vehicles['model_year'] < 2013, 'odometer'] = vehicles.loc[vehicles['model_year'] < 2013, 'odometer'].fillna(mean_odometer_older)

print(vehicles['odometer'].isnull().sum())

# Group by 'model' and fill missing values with the median
for col in ['model_year', 'cylinders', 'odometer']:
    vehicles[col] = vehicles.groupby('model')[col].transform(lambda x: x.fillna(x.median()))

# Convert to integers, handling potential non-integer values
vehicles['model_year'] = vehicles['model_year'].astype(int).astype('Int64')  
vehicles['cylinders'] = vehicles['cylinders'].astype(int).astype('Int64')  
vehicles['odometer'] = vehicles['odometer'].astype(int)  

print(vehicles['model_year'].isnull().sum())

# Drop duplicates
vehicles.drop_duplicates(inplace=True)

vehicles['paint_color'] = vehicles['paint_color'].fillna(np.nan)


# Convert 'date_posted' to datetime
vehicles['date_posted'] = pd.to_datetime(vehicles['date_posted'])

# Convert 'price' to float
vehicles['price'] = vehicles['price'].astype('float64')

# Group by 'model' and fill missing 'cylinders' with the median for each group
vehicles['cylinders'] = vehicles.groupby('model')['cylinders'].transform(lambda x: x.fillna(x.median()))

# Group by 'model' and fill missing 'odometer' with the median for each group
vehicles['odometer'] = vehicles.groupby('model')['odometer'].transform(lambda x: x.fillna(x.median()))

# Convert 'model_year' and 'cylinders' to Int64 (if all NaNs handled)
vehicles['model_year'] = vehicles['model_year'].astype('Int64')
vehicles['cylinders'] = vehicles['cylinders'].astype('Int64')



#convert odometer to int
vehicles['odometer'] = vehicles['odometer'].astype('int64')

vehicles['is_4wd'] = vehicles['is_4wd'].fillna(0)
vehicles['is_4wd'] = vehicles['is_4wd'].astype(int)  # Convert to integer type

high_mileage_vehicles = vehicles[vehicles['odometer'] >= 101000]  # Filter for high mileage

# Now calculate the mean model year
mean_model_year_high_mileage = high_mileage_vehicles['model_year'].mean()
print(f"Mean model year for vehicles with 101,000 miles or more: {mean_model_year_high_mileage:.2f}")

low_mileage_vehicles = vehicles[vehicles['odometer'] <= 100000]  # Filter for low mileage

# Now calculate the mean model year
mean_model_year_low_mileage = low_mileage_vehicles['model_year'].mean()
print(f"Mean model year for vehicles with 100,000 miles or less: {mean_model_year_low_mileage:.2f}")

# Fill 'model_year' for vehicles with 101,000 miles or more with 2007
vehicles.loc[vehicles['odometer'] >= 101000, 'model_year'] = vehicles.loc[vehicles['odometer'] >= 101000, 'model_year'].fillna(2007)

# Fill 'model_year' for vehicles with 100,000 miles or less with 2013
vehicles.loc[vehicles['odometer'] <= 100000, 'model_year'] = vehicles.loc[vehicles['odometer'] <= 100000, 'model_year'].fillna(2013)

current_year = pd.Timestamp.now().year

# Calculate the age of each vehicle
vehicles['age'] = current_year - vehicles['model_year']

# Calculate the age of each vehicle
vehicles['age'] = current_year - vehicles['model_year']

  # Calculate Q1 (25th percentile) and Q3 (75th percentile) for model_year and price
Q1_model_year = vehicles['model_year'].quantile(0.25)
Q3_model_year = vehicles['model_year'].quantile(0.75)
IQR_model_year = Q3_model_year - Q1_model_year

Q1_price = vehicles['price'].quantile(0.25)
Q3_price = vehicles['price'].quantile(0.75)
IQR_price = Q3_price - Q1_price

# Define the lower and upper bounds for model_year and price
lower_bound_model_year = Q1_model_year - 1.5 * IQR_model_year
upper_bound_model_year = Q3_model_year + 1.5 * IQR_model_year

lower_bound_price = Q1_price - 1.5 * IQR_price
upper_bound_price = Q3_price + 1.5 * IQR_price

# Filter out the outliers
vehicles_filtered = vehicles[
    (vehicles['model_year'] >= lower_bound_model_year) & 
    (vehicles['model_year'] <= upper_bound_model_year) & 
    (vehicles['price'] >= lower_bound_price) & 
    (vehicles['price'] <= upper_bound_price)
]











# Create a checkbox to control histogram visibility
show_histogram = st.checkbox("Show Histogram")

# Create a histogram using Plotly Express
if show_histogram:
    fig_hist = px.histogram(vehicles, x="days_listed")  # Replace "column_name" with the desired column
    st.plotly_chart(fig_hist)

# Create a scatter plot using Plotly Express
fig_scatter = px.scatter(vehicles, x="odometer", y="days_listed")  # Replace "column1" and "column2" with desired columns
st.plotly_chart(fig_scatter)

# Checkbox to control scatter plot color
change_color = st.checkbox("Change Scatter Plot Color")

# Change scatter plot color based on checkbox
if change_color:
    fig_scatter.update_traces(marker=dict(color="red"))  # Change color to red
    st.plotly_chart(fig_scatter)

  