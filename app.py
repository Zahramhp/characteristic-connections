import streamlit as st
import pandas as pd

# Title
st.title("Characteristic Connection Explorer")

# Upload Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Read Excel file
    xls = pd.ExcelFile(uploaded_file)
    connections = {}

    # Store characteristic connections
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
        connections[sheet_name] = set(df[0].dropna())

    # Select multiple characteristics
    selected_chars = st.multiselect("Select Characteristics", list(connections.keys()))

    if selected_chars:
        # Find common connections
        common_connections = set.intersection(*(connections[char] for char in selected_chars))
        st.write(f"Characteristics connected to **{', '.join(selected_chars)}**:")
        st.write(common_connections if common_connections else "No common connections found.")
