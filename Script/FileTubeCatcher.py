import os
import fitz
import re
import requests
from pytube import YouTube
from tqdm import tqdm
import pandas as pd
import logging

# Configure the logging
logging.basicConfig(
    filename="download.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Create a logger
logger = logging.getLogger()


def log_and_print(message):
    # Log the message
    logger.info(message)
    # Print the message to the console
    print(message)


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


def extract_youtube_links_from_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
        youtube_links = re.findall(
            r"(https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+)", content
        )
    return youtube_links


def extract_youtube_links_from_csv(file_path):
    df = pd.read_csv(file_path)
    youtube_links = []

    for column in df.columns:
        youtube_links.extend(
            df[column].apply(
                lambda x: re.findall(
                    r"(https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+)", str(x)
                )
            )
        )

    return [link for sublist in youtube_links for link in sublist]


def extract_youtube_links_from_xlsx(file_path):
    df = pd.read_excel(file_path)
    youtube_links = []

    for column in df.columns:
        youtube_links.extend(
            df[column].apply(
                lambda x: re.findall(
                    r"(https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+)", str(x)
                )
            )
        )

    return [link for sublist in youtube_links for link in sublist]


def download_video(link, output_folder, resolution):
    try:
        yt = YouTube(link)

        if resolution.lower() == "highest":
            stream = yt.streams.get_highest_resolution()
        else:
            stream = yt.streams.filter(res=resolution).first()

        if not stream:
            message = f"Video with resolution {resolution} not available for {link}"
            log_and_print(message)
            stream = yt.streams.get_highest_resolution()

        video_title = yt.title
        video_quality = stream.resolution
        file_size = stream.filesize
        output_path = os.path.join(output_folder, f"{video_title}.mp4")

        with open(output_path, "wb") as output_file, requests.get(
            stream.url, stream=True
        ) as response:
            response.raise_for_status()
            with tqdm(
                total=file_size,
                unit="B",
                unit_scale=True,
                desc=f"Downloading: Quality: {video_quality}, Total Size: {file_size/1000000:.2f} MB",
                bar_format="{desc}: {percentage:3.0f}% [{bar}] {n_fmt}/{total_fmt}",
            ) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        output_file.write(chunk)
                        pbar.update(len(chunk))

        message = f"Downloaded: {video_title}"
        log_and_print(message)

    except Exception as e:
        message = f"Error downloading {link}: {e}"
        log_and_print(message)


def download_videos(youtube_links, output_folder, resolution):
    for link in youtube_links:
        download_video(link, output_folder, resolution)


def process_files(file_or_folder, output_folder, resolution):
    os.makedirs(output_folder, exist_ok=True)

    if os.path.isdir(file_or_folder):
        files = os.listdir(file_or_folder)
        for file_name in files:
            file_path = os.path.join(file_or_folder, file_name)
            file_extension = os.path.splitext(file_path)[-1].lower()

            message = f"Processing file: {file_name}"
            log_and_print(message)

            if file_extension == ".pdf":
                youtube_links = extract_youtube_links(file_path)
                download_videos(youtube_links, output_folder, resolution)
            elif file_extension == ".txt":
                youtube_links = extract_youtube_links_from_file(file_path)
                download_videos(youtube_links, output_folder, resolution)
            elif file_extension == ".csv":
                youtube_links = extract_youtube_links_from_csv(file_path)
                download_videos(youtube_links, output_folder, resolution)
            elif file_extension == ".xlsx":
                youtube_links = extract_youtube_links_from_xlsx(file_path)
                download_videos(youtube_links, output_folder, resolution)
            else:
                message = f"Unsupported file format: {file_extension}"
                log_and_print(message)
    else:
        message = "Invalid input. Please provide a valid folder or file path."
        log_and_print(message)


if __name__ == "__main__":
    file_or_folder = input("Enter the folder or file location: ")
    output_folder = input("Enter the output folder name: ")
    resolution = input(
        "Enter the resolution ('highest' for highest available, e.g., '720p'): "
    )

    process_files(file_or_folder, output_folder, resolution)
