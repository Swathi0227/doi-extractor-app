import streamlit as st
import zipfile, os, re, io
import PyPDF2
import pandas as pd

def extract_doi_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = " ".join(page.extract_text() or "" for page in reader.pages)
    return re.findall(r'\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b', text, re.I)

st.title("📄 DOI Extractor from PDFs in ZIP")
uploaded_zip = st.file_uploader("Upload a ZIP file containing PDFs", type="zip")

if uploaded_zip:
    with zipfile.ZipFile(uploaded_zip, "r") as z:
        doi_data = []
        for file in z.namelist():
            if file.endswith(".pdf"):
                with z.open(file) as pdf_file:
                    try:
                        dois = extract_doi_from_pdf(pdf_file)
                        for doi in dois:
                            doi_data.append({"PDF File": file, "DOI": doi})
                    except:
                        doi_data.append({"PDF File": file, "DOI": "Error reading PDF"})

        if doi_data:
            df = pd.DataFrame(doi_data)
            st.dataframe(df)

            # Excel download
            excel_buffer = io.BytesIO()
            df.to_excel(excel_buffer, index=False)
            st.download_button("📥 Download Excel Report", excel_buffer.getvalue(), "doi_report.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        else:
            st.warning("No DOI numbers found in the uploaded PDFs.")
