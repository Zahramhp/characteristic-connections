import streamlit as st
import pandas as pd
from io import BytesIO

# Function to convert DataFrame to Excel for download
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, header=True)
    return output.getvalue()

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
