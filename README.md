# Combine PDFs with filename added to top and bottom.

After searching for ways to print pdfs with filename, i didn't find an easy solution. Therefore, i built this python script that might be helpful to others.

The script processes all PDF files in a specified folder and its **subfolders** by adding a watermark with the filename to each page and combining them into a single PDF file. The watermark is added at the top and bottom of each page, and the pages are scaled and centered to A4 size. All pdfs are then merged into a single pdf called `Combined_pdf_with_watermark.pdf` which is saved to the `output` folder.

## Functions

- `get_all_pdf_pages(folder_path)`: Retrieves paths of all PDF files from a given folder and its subfolders.
- `create_watermark_pdf(filename, page_size)`: Creates a PDF with the filename as a watermark overlay.
- `scale_and_center_page_to_a4(page)`: Scales and centers a PDF page to A4 size using PyPDF2.
- `annotate_and_combine_pdfs(folder_path)`: Processes PDF files in a folder, adding the filename as an overlay watermark and combining them into a single PDF file.

## Usage

1. Set the `folder_path` variable to the path containing your PDF files.
2. Run the script to generate a combined PDF with watermarked pages in the 'output' folder.

## Requirements

Make sure to install the required Python packages listed in `requirements.txt`:

```sh
pip install -r requirements.txt
```