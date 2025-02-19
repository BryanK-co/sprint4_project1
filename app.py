
# app.py

def main():
    print("Hello, World!")



import streamlit as st
import pandas as pd
import plotly.express as px

# Read the dataset's CSV file into a Pandas DataFrame
#df = pd.read_csv('vehicles_us.csv') 
vehicles = pd.read_csv('vehicles_us.csv')

# Create a header
st.header("My Streamlit App")



if __name__ == "__main__":
    main()

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