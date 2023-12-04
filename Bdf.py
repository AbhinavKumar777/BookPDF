import PyPDF4

def reorder_pages(pdf_writer, total_pages, pdf_writer_edo):
    for i in range(1, (total_pages // 2) + 1):
        pdf_writer_edo.addPage(pdf_writer.getPage(total_pages - i))
        pdf_writer_edo.addPage(pdf_writer.getPage(i - 1))

def main(input_pdf_path, output_pdf_path):
    with open(input_pdf_path, 'rb') as input_file:
        pdf_reader = PyPDF4.PdfFileReader(input_file)
        total_pages = pdf_reader.getNumPages()

        pdf_writer = PyPDF4.PdfFileWriter()

        for page_num in range(total_pages):
            pdf_writer.addPage(pdf_reader.getPage(page_num))

        if total_pages % 2 != 0:
            blank_page = PyPDF4.pdf.PageObject.createBlankPage(width=612, height=792)
            pdf_writer.addPage(blank_page)
        
        pdf_writer_edo = PyPDF4.PdfFileWriter()
        total_pages_edo = pdf_writer.getNumPages()

        reorder_pages(pdf_writer, total_pages_edo, pdf_writer_edo)

        with open(output_pdf_path, 'wb') as output_file:
            pdf_writer_edo.write(output_file)

if __name__ == "__main__":
    input_pdf_path = r"C:\Users\91971\Desktop\BDF\CS229_notes.pdf" 
    output_pdf_path = r"output.pdf"
    main(input_pdf_path, output_pdf_path)
