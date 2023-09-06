import os
import fitz  # PyMuPDF
import re
import requests
from pytube import YouTube
from tqdm import tqdm  # Import tqdm for progress bar


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


def download_video(link, output_folder):
    try:
        yt = YouTube(link)
        stream = yt.streams.get_highest_resolution()
        video_title = yt.title

        # Get the video stream URL
        video_url = stream.url

        # Determine the file size
        file_size = int(stream.filesize)

        # Create the output file path
        output_path = os.path.join(output_folder, f"{video_title}.mp4")

        # Download the video with requests while displaying a progress bar
        with open(output_path, "wb") as output_file, requests.get(
            video_url, stream=True
        ) as response:
            response.raise_for_status()
            with tqdm(
                total=file_size,
                unit="B",
                unit_scale=True,
                desc=f"Downloading: {video_title}",
            ) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        output_file.write(chunk)
                        pbar.update(len(chunk))

    except Exception as e:
        print(f"Error downloading {link}: {e}")


def download_videos(youtube_links, output_folder):
    for link in youtube_links:
        download_video(link, output_folder)


def process_pdfs_in_folder(pdf_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # List all PDF files in the folder
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_file)
        youtube_links = extract_youtube_links(pdf_path)
        download_videos(youtube_links, output_folder)


if __name__ == "__main__":
    # Get user input for the PDF folder location and output folder name
    pdf_folder = input("Enter the PDF folder location: ")
    output_folder = input("Enter the output folder name: ")

    process_pdfs_in_folder(pdf_folder, output_folder)
