import streamlit as st
import pandas as pd
from io import BytesIO

# Function to convert DataFrame to Excel for download
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, header=True)
    return output.getvalue()

# Streamlit App Title
st.title("Variant Table Explorer")

# File uploader (Excel)
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Read the Excel file
    df = pd.read_excel(uploaded_file, dtype=str)

    # Extract characteristics (excluding the first column "Variant Table")
    characteristic_columns = df.columns[1:]
    
    # Get a list of all unique characteristics
    all_characteristics = set(df[characteristic_columns].stack().dropna().unique())

    # User selects characteristics
    selected_chars = st.multiselect("Select Characteristics", sorted(all_characteristics))

    if selected_chars:
        # Filter rows where ALL selected characteristics are present
        filtered_df = df[df[characteristic_columns].apply(lambda row: all(char in row.values for char in selected_chars), axis=1)]

        if not filtered_df.empty:
            st.write(f"Variant Tables that contain: **{', '.join(selected_chars)}**")

            # Prepare data for export
            result_data = []

            for _, row in filtered_df.iterrows():
                variant_table = row.iloc[0]  # First column = Variant Table name
                
                # Find other connected characteristics
                other_chars = [char for char in row[1:].dropna().values if char not in selected_chars]

                # Display results
                st.write(f"### Variant Table: {variant_table}")
                if other_chars:
                    st.write("Other Connected Characteristics:")
                    for char in other_chars:
                        st.write(f"- {char}")
                else:
                    st.write("_No additional connections._")

                # Store results for Excel export
                result_data.append([variant_table, ", ".join(selected_chars), ", ".join(other_chars)])

            # Convert results to DataFrame
            result_df = pd.DataFrame(result_data, columns=["Variant Table", "Selected Characteristics", "Other Connected Characteristics"])

            # Generate dynamic file name
            file_name = "_and_".join(selected_chars) + "_variant_tables.xlsx"

            # Download button for the filtered results
            st.download_button(
                label="Download as Excel",
                data=to_excel(result_df),
                file_name=file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        else:
            st.write("No matching Variant Tables found.")
