import streamlit as st
import pandas as pd
import os
from io import BytesIO


st.set_page_config(page_title="Data Sweeper", layout='wide')
 
# Sidebar for user input and file upload
st.sidebar.title("User Input")
user_name = st.sidebar.text_input("Enter Your Name")


uploaded_files = st.sidebar.file_uploader(
    "Upload your files (CSV or Excel):", 
    type=["csv", "xlsx"], 
    accept_multiple_files=True
)

if user_name:
    st.sidebar.success(f"Welcome, {user_name}!")

# Custom CSS
st.markdown(
    """
    <style>
    .stApp{
        background-color: black;
        color: white;
    }   
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description on Main page
st.title("💿 Data Sweeper by Nimra Rasheed")
st.write("Transform your CSV and Excel files with built-in data cleaning and visualization.")

if uploaded_files:
    st.subheader(f"Uploaded files by {user_name}")

    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # file information
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB")

        # File detail preview
        st.write(f"🔍 Preview of {file.name}")
        st.dataframe(df, height=300)

        # Data Cleaning Options
        st.subheader(f"🛠️ Data Cleaning Options for {file.name}")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from {file.name}", key=f"dedup_{file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates Removed!")

            with col2:
                if st.button(f"Fill missing values for {file.name}", key=f"fillna_{file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing values filled!")

        # Select columns to keep 
        st.subheader(f"🎯 Select Columns to Keep in {file.name}")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader(f"📊 Data Visualizations for {file.name}")
        if st.checkbox(f"Show visualizations for {file.name}", key=f"viz_{file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Conversion Options
        st.subheader(f"🔄 Conversion Options for {file.name}")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine='openpyxl')
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉 All files processed successfully!")