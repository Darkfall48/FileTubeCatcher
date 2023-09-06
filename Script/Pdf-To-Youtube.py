import os
import fitz  # PyMuPDF
import re
from pytube import YouTube


def extract_youtube_links(pdf_path):
    doc = fitz.open(pdf_path)
    youtube_links = []

    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text()

        # Use a regular expression to find YouTube links
        youtube_regex = r"(https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+)"
        youtube_links.extend(re.findall(youtube_regex, text))

    return youtube_links


def download_videos(youtube_links, output_folder):
    for link in youtube_links:
        try:
            yt = YouTube(link)
            stream = yt.streams.get_highest_resolution()
            stream.download(output_folder)
            print(f"Downloaded: {yt.title}")
        except Exception as e:
            print(f"Error downloading {link}: {e}")


def process_pdfs_in_folder(folder_path, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # List all PDF files in the folder
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        youtube_links = extract_youtube_links(pdf_path)
        download_videos(youtube_links, output_folder)


if __name__ == "__main__":
    # Get user input for the PDF folder location and output folder name
    pdf_folder = input("Enter the PDF folder location: ")
    output_folder = input("Enter the output folder name: ")

    process_pdfs_in_folder(pdf_folder, output_folder)
