import fitz
import os

from google import genai
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

def describe_image_with_gemini(image_path):

    image = Image.open(image_path)

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[
            """
            Describe this image in detail.

            If it contains:
            - diagrams
            - charts
            - screenshots
            - tables
            - figures

            explain them clearly.

            The output should be useful for Retrieval-Augmented Generation.
            """,
            image,
        ],
    )

    return response.text

def extract_images_from_pdf(pdf_path, output_folder="temp_images"):
    """
    Extract all images from a PDF and save them temporarily.
    Returns a list of image file paths.
    """

    os.makedirs(output_folder, exist_ok=True)

    doc = fitz.open(pdf_path)

    image_paths = []

    image_count = 0

    for page_num in range(len(doc)):

        page = doc[page_num]

        images = page.get_images(full=True)

        for img in images:

            xref = img[0]

            base_image = doc.extract_image(xref)

            image_bytes = base_image["image"]

            ext = base_image["ext"]

            image_path = os.path.join(
                output_folder,
                f"page_{page_num+1}_{image_count}.{ext}"
            )

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            image_paths.append(image_path)

            image_count += 1

    doc.close()

    return image_paths


if __name__ == "__main__":

    images = extract_images_from_pdf("data/NIRMA ELECTRICAL.pdf")

    print(f"Found {len(images)} images\n")

    for img in images:

        print("=" * 60)
        print(f"Image: {img}")
        print("=" * 60)

        description = describe_image_with_gemini(img)

        print(description)
        print()