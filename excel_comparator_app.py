# excel_comparator_app.py

import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Excel Comparator", layout="centered")

st.title("📊 Excel File Comparator")
st.write("Upload two Excel files (same structure) to compare Sheet1 contents.")

# Upload files
file1 = st.file_uploader("Upload File 1", type=["xlsx"])
file2 = st.file_uploader("Upload File 2", type=["xlsx"])

if file1 and file2:
    try:
        df1 = pd.read_excel(file1, sheet_name=0)
        df2 = pd.read_excel(file2, sheet_name=0)

        df1 = df1.drop_duplicates()
        df2 = df2.drop_duplicates()

        diff_1_to_2 = pd.concat([df1, df2, df2]).drop_duplicates(keep=False)
        diff_2_to_1 = pd.concat([df2, df1, df1]).drop_duplicates(keep=False)

        st.success("Comparison completed!")

        # Show previews
        with st.expander("📁 Rows in File 1 but not in File 2"):
            st.dataframe(diff_1_to_2)
        with st.expander("📁 Rows in File 2 but not in File 1"):
            st.dataframe(diff_2_to_1)

        # Save to Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            diff_1_to_2.to_excel(writer, sheet_name="In File1 not in File2", index=False)
            diff_2_to_1.to_excel(writer, sheet_name="In File2 not in File1", index=False)
        output.seek(0)

        st.download_button(
            label="📥 Download Comparison Excel",
            data=output,
            file_name="comparison_result.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
