# Import necessary libraries/modules
import os
import fitz
import re
import requests
import logging
from pytube import YouTube
from tqdm import tqdm
import pandas as pd

# Configure logging settings to write logs to a file
logging.basicConfig(
    filename="download.log",  # Log file name
    level=logging.INFO,  # Log level (INFO: Informational messages)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
    datefmt="%Y-%m-%d %H:%M:%S",  # Date and time format
)

# Create a logger instance
logger = logging.getLogger()


def log_and_print(message):
    # Log the provided message
    logger.info(message)
    # Print the message to the console
    print(message)


# Function to extract YouTube video links from a PDF file
def extract_youtube_links(pdf_path):
    doc = fitz.open(pdf_path)  # Open the PDF file
    youtube_links = []  # List to store YouTube video links

    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text()

        # Use a regular expression to find YouTube links in the text
        youtube_regex = r"(https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+)"
        youtube_links.extend(re.findall(youtube_regex, text))

    return youtube_links


# Function to extract YouTube video links from a text file
def extract_youtube_links_from_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
        # Use regular expression to find YouTube links in the file's content
        youtube_links = re.findall(
            r"(https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+)", content
        )
    return youtube_links


# Function to extract YouTube video links from a CSV file
def extract_youtube_links_from_csv(file_path):
    df = pd.read_csv(file_path)  # Read the CSV file into a DataFrame
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


# Function to extract YouTube video links from an Excel file (XLSX)
def extract_youtube_links_from_xlsx(file_path):
    df = pd.read_excel(file_path)  # Read the Excel file into a DataFrame
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


# Function to download a YouTube video given its link, output folder, and resolution
def download_video(link, output_folder, resolution):
    try:
        yt = YouTube(link)  # Create a YouTube object for the video

        if resolution.lower() == "highest":
            stream = (
                yt.streams.get_highest_resolution()
            )  # Get the highest resolution stream
        else:
            stream = yt.streams.filter(res=resolution).first()  # Filter by resolution

        if not stream:
            # Handle the case when the requested resolution is not available
            message = f"Video with resolution {resolution} not available for {link}"
            log_and_print(message)
            stream = yt.streams.get_highest_resolution()

        video_title = yt.title  # Get the video title
        video_quality = stream.resolution  # Get the video resolution
        file_size = stream.filesize  # Get the video file size
        output_path = os.path.join(
            output_folder, f"{video_title}.mp4"
        )  # Output file path

        with open(output_path, "wb") as output_file, requests.get(
            stream.url, stream=True
        ) as response:
            response.raise_for_status()
            # Create a progress bar for downloading
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
        # Handle errors that may occur during the download process
        message = f"Error downloading {link}: {e}"
        log_and_print(message)


# Function to download multiple YouTube videos given a list of links, output folder, and resolution
def download_videos(youtube_links, output_folder, resolution):
    for link in youtube_links:
        download_video(link, output_folder, resolution)


# Function to process files in a specified folder or file path
def process_files(file_or_folder, output_folder, resolution):
    os.makedirs(
        output_folder, exist_ok=True
    )  # Create the output folder if it doesn't exist

    if os.path.isdir(file_or_folder):
        # If the input is a folder, process all files in the folder
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
    # Input from the user for folder/file location, output folder, and resolution
    file_or_folder = input("Enter the folder or file location: ")
    output_folder = input("Enter the output folder name: ")
    resolution = input(
        "Enter the resolution ('highest' for highest available, e.g., '720p'): "
    )

    # Process the files in the specified folder or file path
    process_files(file_or_folder, output_folder, resolution)
