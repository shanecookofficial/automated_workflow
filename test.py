from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import textwrap

message = """By signing this purchase invoice, you, Bob, authorize the sale of your items to 
Spellbound Books and Games LLC for the agreed upon amount of $100 in the form of cash.
This agreement confirms the completion of the sale under the terms stated herein and constitutes 
a binding commitment to proceed according to the specified terms and conditions.
"""

items = [
    ["Item 1", "$10", "2", "$20"],
    ["Item 2", "$30", "1", "$30"],
]

seller_info = ["Name", "Phone", "Email", "ID"]

def add_header(canv, width, height, page_number=1):
    header_text = ["PURCHASE INVOICE", f"INVOICE #", f"DATE:", f"PAGE: {page_number}"]
    x_position = width - 0.5 * inch
    y_position = height - 0.5 * inch
    for text in header_text:
        canv.drawRightString(x_position, y_position, text)
        y_position -= 12  # Move down for the next line

def add_buyer_seller_info(canv, width, height, seller_info):
    # Adjust starting position as needed from the top
    y_position = height - 2 * inch  # Start below the header

    # BUYER information on the left
    buyer_info = ["Spellbound Books and Games LLC", "PO Box 421", "Sugar City, Idaho", "83448", "spellboundcorporate@gmail.com"]
    x_position_left = 0.5 * inch  # Left margin
    canv.drawString(x_position_left, y_position, "BUYER")
    y_position -= 18  # Move down a bit more after the title

    for line in buyer_info:
        canv.drawString(x_position_left, y_position, line)
        y_position -= 12  # Move down for the next line

    # Placeholder SELLER information on the right
    # Use this section to add specific SELLER details
    x_position_right = width / 2  # Start at the middle of the page
    y_position = height - 2 * inch  # Reset Y position for the SELLER
    canv.drawString(x_position_right, y_position, "SELLER")
    y_position -= 18  # Move down a bit more after the title

    for line in seller_info:
        canv.drawString(x_position_right, y_position, line)
        y_position -= 12  # Move down for the next line


def add_items_table(canv, width, height, items, x_start, table_width, start_y_position, page_number):
    col_proportions = [0.5, 0.15, 0.15, 0.2]
    col_widths = [prop * table_width for prop in col_proportions]
    row_height = 18
    y_start = start_y_position

    headers = ["DESCRIPTION", "PRICE", "QUANTITY", "TOTAL"]
    y = y_start
    x = x_start

    # Function to draw table headers
    def draw_headers(y):
        x = x_start
        for header, col_width in zip(headers, col_widths):
            canv.drawString(x + 2, y - row_height + 5, header)
            canv.rect(x, y - row_height, col_width, row_height)
            x += col_width

    draw_headers(y)
    y -= row_height

    for item in items:
        if y < 0.5 * inch:  # Check if new page is needed
            canv.showPage()
            page_number += 1
            add_header(canv, width, height, page_number)
            y = height - 2 * inch  # Reset y to position after header for new page
            draw_headers(y)
            y -= row_height

        x = x_start
        for value, col_width in zip(item, col_widths):
            canv.drawString(x + 2, y - row_height + 5, str(value))
            canv.rect(x, y - row_height, col_width, row_height)
            x += col_width
        y -= row_height

    return y, page_number  # Return the last page number for further use

def add_signature_section(canv, width, height, message):
    # Initial setup for signature section
    section_height = 50  # Adjust as needed
    margin = 0.5 * inch  # Common margin for the sides

    # Calculate text area width
    text_width = width - 2 * margin

    # Wrap the provided message to fit within the text area width
    wrapped_text = textwrap.wrap(message, width=80)  # Adjust 'width' as needed for your font and size

    # Calculate the starting y position for the message
    # Assume each line needs about 12 points of height (this is an approximation)
    text_height = 12 * len(wrapped_text)  # Calculate total text height
    y_start_message = height - 2 * inch - text_height  # Adjust starting point as needed

    # Draw the wrapped message text
    for line in wrapped_text:
        canv.drawString(margin, y_start_message, line)
        y_start_message -= 12  # Move to the next line

    # Adjust y_start for the signature and date fields based on the message height
    y_start = y_start_message - 60  # Provide some space between the message and the signature section

    # Continue with the original signature section code...
    signature_width = (3/4) * (width - 2 * margin)
    date_width = (1/4) * (width - 2 * margin) - margin  # Adjust for spacing

    x_start_signature = margin
    x_start_date = x_start_signature + signature_width + margin

    signature_height = 40  # Adjust the height as needed

    # Signature label and box
    canv.drawString(x_start_signature, y_start + signature_height + 10, "Signature:")
    canv.rect(x_start_signature, y_start, signature_width, signature_height, stroke=1)

    # Date label and box
    canv.drawString(x_start_date, y_start + signature_height + 10, "Date:")
    canv.rect(x_start_date, y_start, date_width, signature_height, stroke=1)

    # Example message to add above the signature section


    
# Adjust your create_pdf function to include the add_signature_section call
def create_pdf(path, items, message, seller_info, seller_name, total_amount="$100"):
    width, height = letter
    pdf = canvas.Canvas(path, pagesize=letter)
    page_number = 1
    add_header(pdf, width, height, page_number)
    add_buyer_seller_info(pdf, width, height, seller_info)
    
    table_width = width - 1 * inch  # Desired table width, assuming a 0.5 inch margin on each side
    x_start = 0.5 * inch  # Starting X position
    start_y_position = height - 3.5 * inch  # Adjust based on content above
    
    # Add items table and get the final y position and page number
    final_y, page_number = add_items_table(pdf, width, height, items, x_start, table_width, start_y_position, page_number)
    
    # Check if there's enough space for the total amount and signature section; if not, add a new page
    if final_y - 100 < 0.5 * inch:  # Just a placeholder value for space calculation
        pdf.showPage()
        page_number += 1
        add_header(pdf, width, height, page_number)
        final_y = height - 1 * inch
    
    # Display total amount above signature section, aligned to the right
    right_margin = width - 0.5 * inch  # Assuming a 0.5 inch margin on the right
    total_amount_text = "Total Amount to be Paid: " + total_amount
    final_y -= 20  # Adjust for the total amount display
    pdf.drawRightString(right_margin, final_y, total_amount_text)
    
    final_y -= 30  # Adjust space for the legal notice

    # Check if there's enough space for the legal notice; if not, add a new page
    if final_y - 60 < 0.5 * inch:  # Estimate space needed for the legal notice
        pdf.showPage()
        page_number += 1
        add_header(pdf, width, height, page_number)
        final_y = height - 1 * inch

    # Add legal notice
    #add_legal_notice(pdf, width, final_y, seller_name, total_amount)
    final_y -= 100  # Adjust space after legal notice for any further content or end
    
    # Assuming the signature section is still needed, adjust its placement here
    # This is just a placeholder; you might need to adjust based on your actual layout needs
    if final_y < 100:  # Check space for signature section
        pdf.showPage()
        add_header(pdf, width, height, page_number + 1)
        final_y = height - 1 * inch

    add_signature_section(pdf, width, final_y, message)

    pdf.save()

create_pdf("purchase_invoice.pdf", items, message, seller_info)