import streamlit as st
from pdf2image import convert_from_bytes
import pytesseract
from fpdf import FPDF
import os

# Function to perform OCR on images and return extracted text
def ocr_from_images(images):
    extracted_text = ""
    for image in images:
        text = pytesseract.image_to_string(image)
        extracted_text += text + "\n"
    return extracted_text

# Function to create a PDF from the extracted text
def create_pdf(text, output_filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Split the text into lines and add them to the PDF
    for line in text.split('\n'):
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.output(output_filename)

# Streamlit app layout
st.title("Image-Based PDF to Text Converter")

# File uploader for PDF files
uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")

if uploaded_file is not None:
    # Convert PDF pages to images
    images = convert_from_bytes(uploaded_file.read())
    
    # Perform OCR on the images to extract text
    extracted_text = ocr_from_images(images)
    
    # Display extracted text in the app
    st.subheader("Extracted Text:")
    st.text_area("Extracted Text", extracted_text, height=300)

    # Button to create and download the output PDF
    if st.button("Create PDF"):
        output_pdf_filename = "extracted_text.pdf"
        create_pdf(extracted_text, output_pdf_filename)
        
        # Provide a download link for the generated PDF
        with open(output_pdf_filename, "rb") as f:
            st.download_button(
                label="Download PDF",
                data=f,
                file_name=output_pdf_filename,
                mime="application/pdf"
            )

        # Clean up by removing the generated file after download
        os.remove(output_pdf_filename)
