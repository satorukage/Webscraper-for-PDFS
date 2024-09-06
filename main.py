from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import os
import time
import shutil  # For zipping folders

# Dictionary of sectors with their corresponding URLs
sectors = {
    "Agriculture": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=agri",
    "Building and Construction": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=bouw",
    "Business Services": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=zakelijke-dienstverlening",
    "Energy": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=energie",
    "Financials": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=financials",
    "Food and Beverage": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=voeding-en-dranken",
    "ICT": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=ict",
    "Manufacturing": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=productiebedrijven",
    "Packaging": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=packaging",
    "Retail": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=retail",
    "Telecom": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=telecom",
    "Transport": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=telecom",
    "Waste (collection/treatment)": "https://www.sustainability-reports.com/bedrijf/?_sft_sector=afval-inzamelingverwerking",
}

# Create a main folder called "sustainability_pdfs"
main_folder = "sustainability_pdfs"
if not os.path.exists(main_folder):
    os.makedirs(main_folder)

# Function to initialize the web driver
def start_driver():
    return webdriver.Chrome()

# Loop through each sector and download PDFs
for sector, url in sectors.items():
    print(f"Processing sector: {sector}")

    # Restart Selenium for each sector to avoid disconnection
    driver = start_driver()

    try:
        # Open the URL for the sector
        driver.get(url)

        # Wait for the page to fully load (adjust the sleep time if necessary)
        time.sleep(5)

        # Fetch the page source after it has loaded
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Create a folder for the sector within "sustainability_pdfs"
        sector_folder = os.path.join(main_folder, sector.replace(" ", "_"))
        if not os.path.exists(sector_folder):
            os.makedirs(sector_folder)

        # Find all <a> tags with an href attribute (PDF links)
        pdf_links = soup.find_all('a', href=True)

        # Filter links that contain '.pdf' (even with query params)
        pdf_links = [link['href'] for link in pdf_links if '.pdf' in link['href']]

        # Loop through the filtered PDF links and download each one
        if pdf_links:
            for pdf_url in pdf_links:

                # Handle relative URLs if any (if URL doesn't start with http/https)
                if not pdf_url.startswith("http"):
                    pdf_url = url + pdf_url

                pdf_name = pdf_url.split("/")[-1].split("?")[0]  # Extract filename before query params

                # Debugging: Print each PDF URL to ensure correct links are being processed
                print(f"Downloading PDF from: {pdf_url}")

                try:
                    # Download the PDF with SSL verification disabled
                    pdf_response = requests.get(pdf_url, verify=False)

                    # Save the PDF to the sector folder
                    with open(os.path.join(sector_folder, pdf_name), 'wb') as pdf_file:
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_name}")
                except Exception as e:
                    print(f"Failed to download {pdf_url}: {e}")
        else:
            print(f"No PDFs found for sector: {sector}")

        # After downloading, zip the sector folder
        zip_filename = os.path.join(main_folder, sector.replace(" ", "_"))
        print(f"Zipping folder: {sector_folder} to {zip_filename}.zip")
        shutil.make_archive(zip_filename, 'zip', sector_folder)

    except Exception as e:
        print(f"Error processing sector {sector}: {e}")

    finally:
        # Close the driver after processing each sector
        driver.quit()

print("All sectors processed and zipped.")
