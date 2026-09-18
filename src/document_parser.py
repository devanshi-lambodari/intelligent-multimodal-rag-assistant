# import os

# from docling.document_converter import DocumentConverter

# from ocr_utils import extract_text_from_image


# IMAGE_TYPES = {
#     ".png",
#     ".jpg",
#     ".jpeg",
# }

# DOCUMENT_TYPES = {
#     ".pdf",
#     ".docx",
#     ".pptx",
#     ".xlsx",
#     ".html",
#     ".md",
# }


# _converter = DocumentConverter()


# def parse_document(filepath: str) -> str:
#     """
#     Parse a supported file and return extracted text.
#     """

#     _, extension = os.path.splitext(filepath)
#     extension = extension.lower()

#     if extension in IMAGE_TYPES:
#         return extract_text_from_image(filepath)

#     if extension in DOCUMENT_TYPES:
#         try:
#             result = _converter.convert(filepath)
#             return result.document.export_to_markdown()

#         except Exception as e:
#             raise RuntimeError(
#                 f"Failed to parse '{filepath}'"
#             ) from e

#     raise ValueError(
#         f"Unsupported file type: {extension}"
#     )



# import os

# from docling.document_converter import DocumentConverter

# from ocr_utils import extract_text_from_image

# converter = DocumentConverter()


# def parse_document(filepath: str):

#     extension = os.path.splitext(filepath)[1].lower()

#     # -------------------------------
#     # Images
#     # -------------------------------

#     if extension in [".png", ".jpg", ".jpeg"]:

#         return extract_text_from_image(filepath)

#     # -------------------------------
#     # Documents
#     # -------------------------------

#     elif extension in [

#         ".pdf",
#         ".docx",
#         ".pptx",
#         ".xlsx",
#         ".html",
#         ".md",

#     ]:

#         result = converter.convert(filepath)

#         return result.document.export_to_markdown()

#     else:

#         raise ValueError(
#             f"Unsupported file {extension}"
#         )




import os
import fitz

from docling.document_converter import DocumentConverter

from ocr_utils import (
    extract_text_from_pdf,
    extract_text_from_image,
)

converter = DocumentConverter()


def is_searchable_pdf(filepath: str) -> bool:
    """
    Returns True if at least one page contains selectable text.
    """

    with fitz.open(filepath) as pdf:

        for page in pdf:

            if page.get_text().strip():
                return True

    return False


def parse_document(filepath: str):

    extension = os.path.splitext(filepath)[1].lower()

    # --------------------------------------------------
    # Images
    # --------------------------------------------------

    if extension in [".png", ".jpg", ".jpeg"]:

        return extract_text_from_image(filepath)

    # --------------------------------------------------
    # PDFs
    # --------------------------------------------------

    if extension == ".pdf":

        if is_searchable_pdf(filepath):

            print("Searchable PDF detected → Docling")

            result = converter.convert(filepath)

            return result.document.export_to_markdown()

        else:

            print("Scanned PDF detected → PaddleOCR")

            return extract_text_from_pdf(filepath)

    # --------------------------------------------------
    # Office documents
    # --------------------------------------------------

    if extension in [

        ".docx",
        ".pptx",
        ".xlsx",
        ".html",
        ".md",

    ]:

        result = converter.convert(filepath)

        return result.document.export_to_markdown()

    raise ValueError(f"Unsupported file: {extension}")