# Sustainability Reports Scraper

This Python project scrapes PDF sustainability reports from various industry sectors and organizes them into categorized folders. The script downloads the PDF reports and then zips the files for each sector into separate compressed files for easy access.

## Features

- **Selenium-based web scraping**: The script uses Selenium to interact with a webpage, navigate through sectors, and scrape PDF reports.
- **Multi-sector support**: The script downloads PDFs for sectors like Agriculture, Energy, Financials, etc.
- **File organization**: After downloading, the PDFs are stored in separate folders for each sector.
- **Zipping functionality**: Each sector’s folder is compressed into a `.zip` file for easy sharing or storage.
- **SSL verification bypass**: The script can handle SSL errors by disabling certificate verification.

## Project Structure

- **`main.py`**: The primary Python script that handles scraping, downloading, and zipping of PDF reports.
- **`sustainability_pdfs/`**: This folder is created during runtime, and it contains all the downloaded PDFs and the corresponding zip files for each sector.

## Requirements

To run this project, you’ll need the following Python libraries:

- `selenium`
- `bs4` (BeautifulSoup)
- `requests`
- `shutil` (part of the Python standard library)

Install the required libraries using pip:

```bash
pip install selenium beautifulsoup4 requests
