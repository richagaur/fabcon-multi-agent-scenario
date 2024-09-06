import fitz  # PyMuPDF

def extract_toc(pdf_document):
    doc = fitz.open(pdf_document)
    # Extract text from the PDF
    toc = fitz.utils.get_toc(doc)  # Extract TOC from PDF outline
    sections = []
    for section in toc:
        print(section)
        level, title, page_start = section
        page_end = toc[toc.index(section) + 1][2] - 1 if toc.index(section) + 1 < len(toc) else doc.page_count
        
        # Extract the entire page content in binary format (raw PDF for now)
        section_pages = b""
        text_content = ""
        for page_num in range(page_start - 1, page_end):
            page = doc.load_page(page_num)
            pdf_bytes = page.read_contents()  # Get binary content of the page
            section_pages += pdf_bytes  # Append the binary content
            # Prepare the page for text extraction
            text_content += page.get_textpage().extractText()  # Extract text content from the page
            print(f"Extracted content from page {page_num + 1}")

        sections.append({
            "title": title,
            "content": section_pages,
            "text_content": text_content,
            "page_start": page_start,
            "page_end": page_end
        })
        # if len(sections) == 5:
        #     break
    
    return sections
# if __name__ == "__main__":
#     pdf_path = "C:\\Users\\richagaur\\Desktop\\azure-cosmos-db.pdf"
#     sections = extract_toc(pdf_path)
#     for section in sections:
#         print(f"Title: {section['title']}, Pages: {section['page_start']} - {section['page_end']}")
