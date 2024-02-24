import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QFileDialog
from PyQt5.QtGui import QColor, QPalette, QIcon
import PyPDF4

class BDFApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BookPDF")
        self.setWindowIcon(QIcon("pdf_icon.png"))  # Replace "pdf_icon.png" with the path to your icon file
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)

        # Instructions label
        instructions_label = QLabel("Select PDF file to reorder its pages:")
        layout.addWidget(instructions_label)

        # File selection section
        file_layout = QHBoxLayout()
        self.entry_path = QLineEdit()
        self.entry_path.setPlaceholderText("Select PDF file...")
        self.entry_path.setStyleSheet("border: 1px solid #aaa; padding: 8px; border-radius: 5px;")
        file_layout.addWidget(self.entry_path)

        self.button_browse = QPushButton("Browse")
        self.button_browse.setStyleSheet("padding: 8px 16px; border: none; background-color: #007bff; color: white; border-radius: 5px;")
        self.button_browse.clicked.connect(self.browse_pdf)
        file_layout.addWidget(self.button_browse)

        layout.addLayout(file_layout)

        # Process button
        self.button_process = QPushButton("Process PDF")
        self.button_process.setStyleSheet("padding: 12px 24px; border: none; background-color: #007bff; color: white; border-radius: 5px; font-weight: bold;")
        self.button_process.clicked.connect(self.start_processing)
        layout.addWidget(self.button_process)

        self.setLayout(layout)
        self.resize(600, 300)  # Set larger window size

    def reorder_pages(self, pdf_writer, total_pages, pdf_writer_edo):
        for i in range(1, (total_pages // 2) + 1):
            pdf_writer_edo.addPage(pdf_writer.getPage(total_pages - i))
            pdf_writer_edo.addPage(pdf_writer.getPage(i - 1))

    def process_pdf(self):
        input_pdf_path = self.entry_path.text()
        if not input_pdf_path:
            QMessageBox.critical(self, "Error", "Please select a PDF file.")
            return

        try:
            input_dir, input_filename = os.path.split(input_pdf_path)
            output_filename = input_filename.split('.')[0] + "-reordered.pdf"
            output_pdf_path = os.path.join(input_dir, output_filename)

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

                self.reorder_pages(pdf_writer, total_pages_edo, pdf_writer_edo)

                with open(output_pdf_path, 'wb') as output_file:
                    pdf_writer_edo.write(output_file)
            
            QMessageBox.information(self, "Success", f"PDF Processed. Output file: \"{output_filename}\"")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def browse_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF files (*.pdf)")
        if file_path:
            self.entry_path.setText(file_path)

    def start_processing(self):
        self.process_pdf()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(45, 45, 45))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(30, 30, 30))
    palette.setColor(QPalette.AlternateBase, QColor(45, 45, 45))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    app.setPalette(palette)
    
    window = BDFApp()
    window.show()
    sys.exit(app.exec_())



    