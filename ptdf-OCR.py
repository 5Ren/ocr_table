import PyPDF2
from PIL import Image
import pytesseract
import io
import os
from pdf2image import convert_from_path


def pdf_to_img(pdf_file):
    return convert_from_path(pdf_file)


def ocr_core(file):
    text = pytesseract.image_to_string(file)
    return text


def print_pages(pdf_file):
    images = pdf_to_img(pdf_file)

    for i in range(len(images)):
        print("Page " + str(i) + ":")
        print(ocr_core(images[i]))
        print("\n-----------------\n")


pdf_file = "2009_Kumar_ナノ構造.pdf"
print_pages(pdf_file)
