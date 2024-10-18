"""
This script processes PDF files in a specified folder and its subfolders by adding a watermark with the filename to each page and combining them into a single PDF file. The watermark is added at the top and bottom of each page, and the pages are scaled and centered to A4 size.
Functions:
- get_all_pdf_pages(folder_path): Retrieves paths of all PDF files from a given folder and its subfolders.
- create_watermark_pdf(filename, page_size): Creates a PDF with the filename as a watermark overlay.
- scale_and_center_page_to_a4(page): Scales and centers a PDF page to A4 size using PyPDF2.
- annotate_and_combine_pdfs(folder_path): Processes PDF files in a folder, adding the filename as an overlay watermark and combining them into a single PDF file.
Usage:
1. Set the `folder_path` variable to the path containing your PDF files.
2. Run the script to generate a combined PDF with watermarked pages in the 'output' folder.
"""

import os
import numpy as np
from PyPDF2 import PdfReader, PdfWriter, PageObject
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from io import BytesIO

def get_all_pdf_pages(folder_path):
    """Get paths of all PDF files from a given folder and its subfolders."""
    pdf_paths = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_paths.append(os.path.join(root, file))
    return pdf_paths

def create_watermark_pdf(filename, page_size):
    """Create a PDF with the filename as a watermark overlay."""
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=page_size)
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor('red')
    text = f"Filename: {filename}"
    text_width = c.stringWidth(text, "Helvetica", 16)

    #add filenames to bottom and top (right aligned)
    c.drawString(page_size[0] - text_width - 25, 25, text)
    c.drawString(page_size[0] - text_width -25, page_size[1] - 25, text)

    c.save()
    packet.seek(0)  # Move to the beginning of the BytesIO buffer
    return packet

def scale_and_center_page_to_a4(page: PageObject):
    """Scale and center a PDF page to A4 size using PyPDF2."""
    original_width = float(page.mediabox.width)
    original_height = float(page.mediabox.height)
    scale_x = A4[0] / original_width
    scale_y = A4[1] / original_height
    
    scale = min(scale_x, scale_y)
    scale = scale * 0.9  # make a little smaller to fit better

    scaled_width = original_width * scale
    scaled_height = original_height * scale
    

    new_page = PageObject.create_blank_page(width=A4[0], height=A4[1])
    x_offset = (A4[0] - scaled_width) / 2
    y_offset = (A4[1] - scaled_height) / 2
    
    # Apply the transformation to the original page
    page.add_transformation([scale, 0, 0, scale, x_offset, y_offset])
    
    # Merge the transformed page onto the new A4 page
    new_page.merge_page(page)
    return new_page

def annotate_and_combine_pdfs(folder_path):
    """Print PDF files in a folder, adding the filename as an overlay watermark."""
    output_folder = 'output'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    pdf_paths = get_all_pdf_pages(folder_path)
    file_names = [os.path.basename(file_path) for file_path in pdf_paths]
    i_sorted = np.argsort(file_names)
    print(i_sorted)
    pdf_paths = [pdf_paths[i] for i in i_sorted]

    writer = PdfWriter()
    for i, file_path in enumerate(pdf_paths):
        
        file_name = os.path.basename(file_path)
        print(f"Processing: {file_name}")

        #create watermark page with filename as text
        watermark = create_watermark_pdf(file_name, A4)
        watermark_reader = PdfReader(watermark)
        watermark_page = watermark_reader.pages[0]

        # Overlay watermark on each page of the original PDF
        reader = PdfReader(file_path)
        for page in reader.pages:
            page = scale_and_center_page_to_a4(page)
            page.merge_page(watermark_page)
            writer.add_page(page)

    # Save the output PDF with watermark
    output_path = os.path.join(output_folder, f"Combined_pdf_with_watermark.pdf")
    with open(output_path, 'wb') as out:
        writer.write(out)
    
# Set the folder path containing your PDF files
folder_path = '/path/to/pdf/files/and/folders'
annotate_and_combine_pdfs(folder_path)