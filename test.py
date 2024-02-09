from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Optional: add header methods
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Header Title', 0, 1, 'C')

    def footer(self):
        # Optional: add footer methods
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# Create instance of FPDF class
pdf = PDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(0, 10, "Hello, World!", 0, 1)

# Save the PDF to a file
pdf.output("hello_pyfpdf.pdf")
