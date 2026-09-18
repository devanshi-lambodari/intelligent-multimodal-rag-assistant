# # import fitz
# # import easyocr
# # import os

# # # Create OCR reader once
# # reader = easyocr.Reader(["en"])


# # def extract_text_from_pdf(pdf_path):
# #     """
# #     Extract text from both normal and scanned PDFs.
# #     """

# #     doc = fitz.open(pdf_path)
# #     full_text = ""

# #     for page in doc:

# #         # Try extracting selectable text first
# #         text = page.get_text()

# #         if text.strip():
# #             full_text += text + "\n"

# #         else:
# #             # Page is probably scanned
# #             print("⚡ OCR used on this page")

# #             pix = page.get_pixmap(dpi=300)

# #             image_path = "temp_page.png"

# #             pix.save(image_path)

# #             results = reader.readtext(image_path)

# #             page_text = "\n".join([r[1] for r in results])

# #             full_text += page_text + "\n"

# #             # Delete temporary image
# #             if os.path.exists(image_path):
# #                 os.remove(image_path)

# #     doc.close()

# #     return full_text


# # def extract_text_from_image(image_path):
# #     """
# #     Extract text from an image using EasyOCR.
# #     """

# #     results = reader.readtext(image_path)

# #     text = "\n".join([r[1] for r in results])

# #     return text



# # import fitz
# # import os

# # from paddleocr import PaddleOCR

# # # Initialize PaddleOCR once
# # ocr = PaddleOCR(
# #     use_doc_orientation_classify=False,
# #     use_doc_unwarping=False,
# #     use_textline_orientation=False,
# #     lang="en"
# # )


# # def paddle_extract(image_path):
# #     """
# #     Extract text from an image using PaddleOCR.
# #     Keeps text in reading order.
# #     """

# #     result = ocr.predict(image_path)

# #     lines = []

# #     for page in result:

# #         # page["rec_texts"] contains OCR text
# #         if "rec_texts" in page:

# #             lines.extend(page["rec_texts"])

# #     return "\n".join(lines)


# # def extract_text_from_image(image_path):
# #     return paddle_extract(image_path)


# # def extract_text_from_pdf(pdf_path):

# #     doc = fitz.open(pdf_path)

# #     full_text = ""

# #     for page in doc:

# #         text = page.get_text()

# #         # Normal searchable PDF
# #         if text.strip():

# #             full_text += text + "\n"

# #         # Scanned page
# #         else:

# #             print("⚡ PaddleOCR used")

# #             pix = page.get_pixmap(dpi=300)

# #             temp = "temp_page.png"

# #             pix.save(temp)

# #             full_text += paddle_extract(temp) + "\n"

# #             if os.path.exists(temp):
# #                 os.remove(temp)

# #     doc.close()

# #     return full_text



# import os
# import tempfile
# import fitz

# from paddleocr import PaddleOCR


# # ==========================================================
# # Initialize PaddleOCR only once
# # ==========================================================

# ocr = PaddleOCR(
#     use_doc_orientation_classify=False,
#     use_doc_unwarping=False,
#     use_textline_orientation=False,
#     lang="en",
# )


# # ==========================================================
# # OCR for Images
# # ==========================================================

# def paddle_extract(image_path: str) -> str:
#     """
#     Extract text from an image using PaddleOCR.
#     Returns text in reading order.
#     """

#     try:

#         result = ocr.predict(image_path)

#         lines = []

#         for page in result:
#             lines.extend(page.get("rec_texts", []))

#         return "\n".join(lines)

#     except Exception as e:

#         raise RuntimeError(
#             f"OCR failed for image: {image_path}"
#         ) from e


# # ==========================================================
# # Image OCR
# # ==========================================================

# def extract_text_from_image(image_path: str) -> str:
#     """
#     Extract text from an image.
#     """

#     return paddle_extract(image_path)


# # ==========================================================
# # PDF Text Extraction
# # ==========================================================

# def extract_text_from_pdf(pdf_path: str) -> str:
#     """
#     Extract text from a PDF.

#     Strategy:
#     1. If page has selectable text -> use PyMuPDF.
#     2. Otherwise use PaddleOCR.
#     """

#     pages = []

#     with fitz.open(pdf_path) as doc:

#         for page_number, page in enumerate(doc, start=1):

#             text = page.get_text().strip()

#             # --------------------------------------------------
#             # Searchable PDF
#             # --------------------------------------------------

#             if text:

#                 pages.append(text)

#             # --------------------------------------------------
#             # Scanned PDF
#             # --------------------------------------------------

#             else:

#                 print(f"⚡ OCR used on page {page_number}")

#                 pix = page.get_pixmap(dpi=300)

#                 with tempfile.NamedTemporaryFile(
#                     suffix=".png",
#                     delete=False
#                 ) as temp:

#                     temp_path = temp.name

#                 try:

#                     pix.save(temp_path)

#                     ocr_text = paddle_extract(temp_path)

#                     pages.append(ocr_text)

#                 finally:

#                     if os.path.exists(temp_path):
#                         os.remove(temp_path)

#     return "\n\n".join(pages)






import os
import tempfile
import fitz

from PIL import Image
from paddleocr import PaddleOCR


# ==========================================================
# Initialize PaddleOCR only once
# ==========================================================

print("Initializing PaddleOCR...")

ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    lang="en",
    enable_mkldnn=False,
)

print("PaddleOCR initialized successfully.")


# ==========================================================
# PaddleOCR extraction
# ==========================================================

def paddle_extract(image_path: str) -> str:
    """
    Extract text from an image using PaddleOCR.

    The image is first converted to a clean RGB PNG.
    This avoids problems with JPG modes, transparency,
    CMYK images, or unusual image formats.
    """

    if not os.path.exists(image_path):
        raise FileNotFoundError(
            f"Image does not exist: {image_path}"
        )

    temp_path = None

    try:

        # --------------------------------------------------
        # Open image
        # --------------------------------------------------

        print(f"OCR input: {image_path}")

        image = Image.open(image_path)

        print(
            f"Image loaded: "
            f"{image.size[0]}x{image.size[1]}, "
            f"mode={image.mode}"
        )

        # --------------------------------------------------
        # Convert to RGB
        # --------------------------------------------------

        if image.mode != "RGB":
            image = image.convert("RGB")

        # --------------------------------------------------
        # Save as temporary PNG
        # --------------------------------------------------

        with tempfile.NamedTemporaryFile(
            suffix=".png",
            delete=False
        ) as temp:

            temp_path = temp.name

        image.save(temp_path, format="PNG")

        print(f"Temporary OCR image: {temp_path}")

        # --------------------------------------------------
        # Run PaddleOCR
        # --------------------------------------------------

        result = ocr.predict(temp_path)

        # --------------------------------------------------
        # Extract OCR text
        # --------------------------------------------------

        lines = []

        for page in result:

            # PaddleOCR 3.x may return a result object
            # instead of a normal dictionary.
            #
            # Try dictionary-style access first.

            if isinstance(page, dict):

                rec_texts = page.get("rec_texts", [])

                if rec_texts:
                    lines.extend(
                        str(text)
                        for text in rec_texts
                        if str(text).strip()
                    )

            else:

                # Some PaddleOCR versions return objects
                # containing the OCR data.

                if hasattr(page, "json"):

                    try:

                        data = page.json

                        if callable(data):
                            data = data()

                        if isinstance(data, str):
                            import json
                            data = json.loads(data)

                        if isinstance(data, dict):

                            rec_texts = data.get(
                                "rec_texts",
                                []
                            )

                            if rec_texts:
                                lines.extend(
                                    str(text)
                                    for text in rec_texts
                                    if str(text).strip()
                                )

                    except Exception:
                        pass

                # Another possible representation
                elif hasattr(page, "rec_texts"):

                    rec_texts = page.rec_texts

                    if rec_texts:
                        lines.extend(
                            str(text)
                            for text in rec_texts
                            if str(text).strip()
                        )

        text = "\n".join(lines).strip()

        print(
            f"OCR extracted {len(text)} characters"
        )

        return text

    except Exception as e:

        print(
            f"\n❌ PaddleOCR error for: {image_path}"
        )

        print(
            f"Error type: {type(e).__name__}"
        )

        print(
            f"Error details: {e}"
        )

        raise RuntimeError(
            f"OCR failed for image: {image_path}"
        ) from e

    finally:

        # --------------------------------------------------
        # Delete temporary file
        # --------------------------------------------------

        if temp_path and os.path.exists(temp_path):

            try:
                os.remove(temp_path)

            except Exception:
                pass


# ==========================================================
# Image OCR
# ==========================================================

def extract_text_from_image(image_path: str) -> str:
    """
    Extract text from an image file.
    """

    return paddle_extract(image_path)


# ==========================================================
# PDF Text Extraction
# ==========================================================

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF.

    Strategy:

    1. Try extracting selectable text using PyMuPDF.
    2. If the page contains no text, render it as an image.
    3. Run PaddleOCR on that image.
    """

    pages = []

    with fitz.open(pdf_path) as doc:

        for page_number, page in enumerate(
            doc,
            start=1
        ):

            text = page.get_text().strip()

            # --------------------------------------------------
            # Searchable PDF
            # --------------------------------------------------

            if text:

                print(
                    f"Page {page_number}: "
                    f"searchable text detected"
                )

                pages.append(text)

            # --------------------------------------------------
            # Scanned PDF
            # --------------------------------------------------

            else:

                print(
                    f"⚡ OCR used on page {page_number}"
                )

                pix = page.get_pixmap(
                    dpi=300,
                    alpha=False
                )

                temp_path = None

                try:

                    with tempfile.NamedTemporaryFile(
                        suffix=".png",
                        delete=False
                    ) as temp:

                        temp_path = temp.name

                    pix.save(temp_path)

                    ocr_text = paddle_extract(
                        temp_path
                    )

                    pages.append(ocr_text)

                finally:

                    if (
                        temp_path
                        and os.path.exists(temp_path)
                    ):

                        try:
                            os.remove(temp_path)

                        except Exception:
                            pass

    return "\n\n".join(pages).strip()

