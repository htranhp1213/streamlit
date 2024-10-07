import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on Oct 7th")

# Load and display data
st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# 1.Add a drop-down for Category using st.selectbox
selected_category = st.selectbox(
    label="Select a Category",
    options=df['Category'].unique(),
    placeholder="Choose a Category"
)

# 2. Add a multi-select for Sub-Category filtered by selected Category
filtered_subcategories = df[df['Category'] == selected_category]['Sub_Category'].unique()
selected_subcategories = st.multiselect(
    label="Select Sub-Categories",
    options=filtered_subcategories,
    placeholder="Choose Sub_Categories"
)

# 3. Show a line chart of sales for the selected items in 
# Filter the data based on selected sub-categories
filtered_data = df[df['Sub_Category'].isin(selected_subcategories)]
if not filtered_data.empty:
    # Aggregating by time
    # Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    filtered_data["Order_Date"] = pd.to_datetime(filtered_data["Order_Date"])
    # Set Order_Date as the index for both df and filtered_data
    filtered_data.set_index('Order_Date', inplace=True)
    # Group sales data by month
    sales_by_month_filtered = filtered_data.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
    #sales_by_month_filtered = filtered_data.resample('M', on='Order_Date').sum()
    
    # Show the line chart
    st.line_chart(sales_by_month_filtered['Sales'])

    # 4. Show the metrics for the selected sub-categories
    total_sales = filtered_data['Sales'].sum()
    total_profit = filtered_data['Profit'].sum()
    overall_profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

    # Calculate the average profit margin across all categories
    total_sales_all = df['Sales'].sum()
    total_profit_all = df['Profit'].sum()
    overall_profit_margin_all = (total_profit_all / total_sales_all) * 100 if total_sales_all != 0 else 0

    # Show metrics with a delta for overall profit margin
    st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
    st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
    st.metric(label="Profit Margin (%)", value=f"{overall_profit_margin:.2f}%", delta=f"{overall_profit_margin - overall_profit_margin_all:.2f}%")

else:
    st.write("Please select one sub-category")
    

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum().reset_index())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
#sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
sales_by_month = df.resample('M')['Sales'].sum()
st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
