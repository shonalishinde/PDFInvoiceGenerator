import pandas as pd
import streamlit as st
import os
from fpdf import FPDF
from datetime import date

st.title("Generate PDF Invoices")
st.info("""Introducing our new web application designed to streamline your invoicing process! 
With our user-friendly interface, simply input the required details such as your company name, 
address, and item descriptions into our intuitive form. Our app will then generate professional 
PDF invoices with ease, saving you time and effort. Say goodbye to manual invoicing and hello 
to efficiency with our convenient web app.""")

st.text_input(label="Company Name", placeholder="Your company name", key="name")
st.text_area(label="Company Address", placeholder="Your company address", key="addr")
st.text_input(label="Customer Name", key="cname")
st.text_area(label="Customer Address", key="caddr")

file_input = st.file_uploader("""Upload a excel (xlsx) file (File should contain columns as Srno, 
                              Item Description, Quantity, Unit Price)"""
                              , type="xlsx")

dt = date.today().strftime('%m/%d/%y')

click = st.button("Generate Invoice", key="clicked")

comp_name = st.session_state["name"]
comp_addr = st.session_state["addr"]
cust_name = st.session_state["cname"]
cust_addr = st.session_state["caddr"]

sum = 0

if click:

    pdf = FPDF(orientation="P", unit="mm", format="A4")

    pdf.add_page()

    pdf.set_text_color(255, 0, 0)
    pdf.set_font(family="Arial", size=40, style="B")
    pdf.cell(w=200, h=20, txt=comp_name, align="C", ln=1)

    pdf.set_text_color(255, 0, 0)
    pdf.set_font(family="Arial", size=12, style="I")
    pdf.multi_cell(w=200, h=5, txt=comp_addr, align="C")

    pdf.cell(w=200, h=5, txt="", align="C", ln=4)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font(family="Arial", size=14)
    pdf.cell(w=130, h=7, txt=f"To: {cust_name}", border=1)
    pdf.cell(w=50, h=7, txt=f"Date: {dt}", border=1, ln=1)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font(family="Arial", size=14)
    pdf.multi_cell(w=180, h=5, txt=f"Address: {cust_addr}", border=1)

    pdf.cell(w=200, h=5, txt="", align="C", ln=4)

    if file_input:
        df = pd.read_excel(file_input)

        columns = list(df.columns)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font(family="Arial", size=14, style="B")
        pdf.cell(w=15, h=10, txt=columns[0], align="C", border=1)
        pdf.cell(w=70, h=10, txt=columns[1], align="C", border=1)
        pdf.cell(w=30, h=10, txt=columns[2], align="C", border=1)
        pdf.cell(w=30, h=10, txt=columns[3], align="C", border=1)
        pdf.cell(w=35, h=10, txt="Total Price", align="C", border=1, ln=1)

        for index, row in df.iterrows():
            total_price = int(row[columns[2]] * row[columns[3]])
            sum += total_price
            pdf.set_font(family="Arial", size=14)
            pdf.cell(w=15, h=10, txt=str(row[columns[0]]), border=1)
            pdf.cell(w=70, h=10, txt=str(row[columns[1]]), border=1)
            pdf.cell(w=30, h=10, txt=str(row[columns[2]]), border=1)
            pdf.cell(w=30, h=10, txt=str(row[columns[3]]), border=1)
            pdf.cell(w=35, h=10, txt=str(total_price), border=1, ln=1)

        pdf.set_font(family="Arial", size=14, style="B")
        pdf.cell(w=145, h=10, txt="Total Amount", align="R", border=1)
        pdf.set_font(family="Arial", size=14)
        pdf.cell(w=35, h=10, txt=str(sum), border=1, ln=1)

        pdf.cell(w=200, h=5, txt="", align="C", ln=2)

        pdf.set_font(family="Arial", size=14, style="B")
        pdf.cell(w=145, h=10, txt=f"The Total Amount to be paid is {sum}")

    if os.path.exists(f"Invoice-{comp_name}"):
        os.remove(f"Invoice-{comp_name}")

    pdf_op = pdf.output(f"Invoice-{comp_name}")

    st.info("Invoice generated successfully. To download please click on below button.")

    st.download_button(
        label="Download Generated PDF",
        data=pdf_op,
        file_name=f"Invoice-{comp_name}",
        mime='application/octet-stream',
    )
