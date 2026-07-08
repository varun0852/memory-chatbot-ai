"""
Document processing utilities.

This module is responsible for extracting text from uploaded
documents before they are passed to the chatbot.
"""

from io import BytesIO

from PyPDF2 import PdfReader


class DocumentProcessor:
    """
    Handles document parsing and text extraction.
    """

    def extract_text(self, pdf_file: BytesIO) -> str:
        """
        Extract text from a PDF file.

        Args:
            pdf_file: Uploaded PDF file.

        Returns:
            Extracted text as a single string.
        """

        reader = PdfReader(pdf_file)

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n\n".join(pages)
