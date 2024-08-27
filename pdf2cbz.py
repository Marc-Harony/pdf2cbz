import os
import fitz  # PyMuPDF
import zipfile

# Source and destination directory paths
source_dir = "/where/pdf/are/stored"
destination_dir = "/path/to/dest"

# Function to convert a PDF file to CBZ
def convert_pdf_to_cbz(pdf_path, cbz_path):
    # Create a temporary directory to store the images
    temp_dir = os.path.join("/tmp", os.path.basename(pdf_path).replace(".pdf", ""))
    os.makedirs(temp_dir, exist_ok=True)
    
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    for page_num in range(pdf_document.page_count):
        # Render the page as an image
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        image_path = os.path.join(temp_dir, f"page_{page_num + 1}.png")
        pix.save(image_path)

    # Create a ZIP file (CBZ)
    with zipfile.ZipFile(cbz_path, 'w') as cbz_file:
        for image_file in os.listdir(temp_dir):
            cbz_file.write(os.path.join(temp_dir, image_file), image_file)
    
    # Delete the temporary directory
    for image_file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, image_file))
    os.rmdir(temp_dir)

# Traverse the source directory and its subdirectories
for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.endswith(".pdf"):
            pdf_path = os.path.join(root, file)
            relative_path = os.path.relpath(pdf_path, source_dir)
            cbz_path = os.path.join(destination_dir, relative_path.replace(".pdf", ".cbz"))
            
            # Create the target directory if necessary
            os.makedirs(os.path.dirname(cbz_path), exist_ok=True)
            
            # Convert the PDF file to CBZ
            convert_pdf_to_cbz(pdf_path, cbz_path)
            print(f"Converted: {pdf_path} -> {cbz_path}")

print("Conversion completed.")
