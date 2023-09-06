# FileTubeCatcher - YouTube Video Downloader

## Introduction

FileTubeCatcher is a versatile YouTube video downloader that allows you to effortlessly extract and download YouTube video links from various sources, including PDF files, text documents, CSV files, and Excel spreadsheets. With FileTubeCatcher, you can quickly capture YouTube links from your files and save your favorite videos for offline viewing. This tool is designed to make the process of downloading YouTube videos as easy as possible.

## Features

- Extract YouTube video links from PDF files.
- Retrieve YouTube links from plain text documents.
- Collect YouTube video URLs from CSV files and Excel spreadsheets.
- Download videos in your desired resolution (e.g., 720p, highest available).
- Display a progress bar during downloads for easy tracking.
- Choose your own custom output folder to save downloaded videos.
- Automatic logging of download activities for easy tracking.
- Support for processing multiple files with different extensions in a folder.

## Prerequisites

Before using FileTubeCatcher, ensure that you have the following requirements met:

- Python 3.x installed on your system.
- Required Python libraries: `os`, `fitz`, `re`, `requests`, `pytube`, `tqdm`, `pandas`, `logging`.
- Access to the internet to download videos.
- PDF, text, CSV, or Excel files containing YouTube video links.

## Usage

1. Clone this repository to your local machine or download the source code.

2. Install the necessary Python libraries if you haven't already. You can use `pip` to install missing libraries:

```
pip install pytube tqdm pandas
```

3. Run the `FileTubeCatcher.py` script:

```
python FileTubeCatcher.py
```

4. Follow the on-screen prompts to specify the folder or file location containing YouTube links, your desired output folder for downloaded videos, and the desired resolution for video downloads (e.g., 'highest' or '720p').

5. FileTubeCatcher will start processing your files, extracting YouTube links, and downloading videos to the specified output folder.

6. You can monitor the progress, download speed, and a convenient progress bar in the command-line interface. Additionally, a log file named `download.log` will be created, providing detailed information about the download process.

7. Once the process is complete, you will find the downloaded YouTube videos in the custom output folder you specified.

## Contributing

Contributions to FileTubeCatcher are welcome! If you have any ideas for improvements or new features, please feel free to submit pull requests or open issues in the GitHub repository.
