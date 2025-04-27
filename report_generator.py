from fpdf import FPDF

def generate_pdf_report(claim, verdict, score, urls):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Set font for the title (bold)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="AI Fact Checker Report", ln=True, align="C")
    
    # Add some space
    pdf.ln(10)
    
    # Set font for the body text
    pdf.set_font("Arial", size=12)
    
    # Adding Claim, Verdict, and Confidence
    pdf.cell(200, 10, txt=f"Claim: {claim}", ln=True)
    pdf.cell(200, 10, txt=f"Verdict: {verdict}", ln=True)
    pdf.cell(200, 10, txt=f"Confidence: {score:.2f}", ln=True)
    
    # Add some space
    pdf.ln(10)
    
    # Adding Sources Section
    pdf.cell(200, 10, txt="Sources:", ln=True)
    
    # Add URLs as hyperlinks
    pdf.set_text_color(0, 0, 255)  # Set text color to blue for links
    for url in urls:
        pdf.cell(200, 10, txt=url, ln=True, link=url)
    
    # Save the PDF to a file
    file_path = "fact_check_report.pdf"
    pdf.output(file_path)
    
    return file_path
