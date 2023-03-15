from flask import Flask, render_template, request, redirect, url_for
import pytesseract
import cv2
import os
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO)

if not os.path.exists("uploaded_images"):
    os.makedirs("uploaded_images")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        image = request.files.get("bookshelf_image")

        if image:
            image_path = os.path.join("uploaded_images", image.filename)
            image.save(image_path)

            logging.info("Processing the uploaded image...")
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)
            logging.info("Image processing complete.")

            titles = extract_book_titles(text)
            return render_template("index.html", titles=titles)

    return render_template("index.html")


def extract_book_titles(text):
    # This function should be improved to better extract titles from the OCR text
    lines = text.split("\n")
    titles = [line.strip() for line in lines if line.strip()]
    return titles

if __name__ == "__main__":
    app.run(debug=True)
