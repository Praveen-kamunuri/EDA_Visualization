import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import os
import warnings

warnings.filterwarnings('ignore')

# Function to read the uploaded file into a DataFrame
def read_file(file):
    ext = os.path.splitext(file.name)[-1].lower()
    if ext in ['.csv', '.txt']:
        df = pd.read_csv(file)
    elif ext in ['.xlsx', '.xls']:
        df = pd.read_excel(file)
    else:
        raise ValueError("Unsupported file format. Please upload a CSV, TXT, XLSX, or XLS file.")
    return df

# Main function
def main():
    st.set_page_config(page_title="Dynamic EDA App", page_icon=":bar_chart:", layout="wide")
    st.title(":bar_chart: Dynamic Exploratory Data Analysis App")
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

    # Allow the user to upload a dataset
    file = st.file_uploader("Upload a dataset", type=["csv", "txt", "xlsx", "xls"])

    # If the user uploads a dataset, read it into a DataFrame
    if file is not None:
        df = read_file(file)
        st.success("Dataset loaded successfully!")

        # Summary Statistics
        st.subheader("Summary Statistics")
        st.write(df.describe())

        # Data Visualization
        st.subheader("Data Visualization")
        st.write("Select columns for visualization:")
        columns = st.multiselect("Select columns", df.columns)

        if columns:
            plot_type = st.selectbox("Select plot type", ["Line Chart", "Bar Chart", "Pie Chart", "Scatter Plot", "Treemap"])

            if plot_type == "Line Chart":
                fig = px.line(df, x=columns[0], y=columns[1], title="Line Chart")
                st.plotly_chart(fig, use_container_width=True)

            elif plot_type == "Bar Chart":
                x_axis = st.selectbox("Select X-axis", columns)
                fig = px.bar(df, x=x_axis, y=columns[1], title="Bar Chart")
                st.plotly_chart(fig, use_container_width=True)

            elif plot_type == "Pie Chart":
                fig = px.pie(df, names=columns[0], values=columns[1], title="Pie Chart")
                st.plotly_chart(fig, use_container_width=True)

            elif plot_type == "Scatter Plot":
                x_axis = st.selectbox("Select X-axis", columns)
                y_axis = st.selectbox("Select Y-axis", columns)
                fig = px.scatter(df, x=x_axis, y=y_axis, title="Scatter Plot")
                st.plotly_chart(fig, use_container_width=True)

            elif plot_type == "Treemap":
                x = st.selectbox("Select X-axis", columns)
                fig = px.treemap(df, path=[x], values=columns[1], title="Treemap")
                st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("Please select at least one column for visualization.")

        # Category and Subcategory-wise Pie Charts
        if 'Category' in df.columns and 'Sub-Category' in df.columns:
            st.subheader("Category-wise Sales")
            category_sales = df.groupby('Category')['Sales'].sum().reset_index()
            fig_category_pie = px.pie(category_sales, values='Sales', names='Category', title="Category-wise Sales")
            st.plotly_chart(fig_category_pie, use_container_width=True)

            st.subheader("Sub-Category-wise Sales")
            subcategory_sales = df.groupby('Sub-Category')['Sales'].sum().reset_index()
            fig_subcategory_pie = px.pie(subcategory_sales, values='Sales', names='Sub-Category', title="Sub-Category-wise Sales")
            st.plotly_chart(fig_subcategory_pie, use_container_width=True)

if __name__ == "__main__":
    main()
