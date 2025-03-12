import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Function to convert DataFrame to Excel for download
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, header=True)
    return output.getvalue()

# Title
st.title("Characteristic Connection Explorer")

# Upload CSV files
uploaded_files = st.file_uploader("Upload your CSV files", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    connections = {}

    # Read each uploaded CSV file
    for uploaded_file in uploaded_files:
        char_name = os.path.splitext(uploaded_file.name)[0]  # Use the file name as the characteristic name
        df = pd.read_csv(uploaded_file, header=None)
        connections[char_name] = set(df[0].dropna())

    # Select multiple characteristics
    selected_chars = st.multiselect("Select Characteristics", list(connections.keys()))

    if selected_chars:
        # Find common connections
        common_connections = set.intersection(*(connections[char] for char in selected_chars))

        # Display results
        if common_connections:
            st.write(f"Characteristics connected to **{', '.join(selected_chars)}**:")
            st.write(common_connections)

            # Convert results to DataFrame for export
            result_df = pd.DataFrame(common_connections, columns=["Connected Characteristics"])

            # Create dynamic filename based on selected characteristics
            file_name = "_and_".join(selected_chars) + "_connections.xlsx"

            # Add download button
            st.download_button(
                label="Download as Excel",
                data=to_excel(result_df),
                file_name=file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.write("No common connections found.")
