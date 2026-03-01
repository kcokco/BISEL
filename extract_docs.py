import sys
import docx
from pypdf import PdfReader

def extract_docx(path):
    print("--- DOCX ---")
    print(f"File: {path}")
    doc = docx.Document(path)
    for para in doc.paragraphs:
        if para.text.strip():
            print(para.text)
    print("------------")

def extract_pdf(path):
    print("--- PDF ---")
    print(f"File: {path}")
    reader = PdfReader(path)
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            print(f"-- Page {i+1} --")
            print(text.strip())
    print("-----------")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: extract_docs.py <path>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    if filepath.endswith('.docx'):
        extract_docx(filepath)
    elif filepath.endswith('.pdf'):
        extract_pdf(filepath)
    else:
        print("Unsupported file format.")
