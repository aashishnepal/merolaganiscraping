# merolaganiscraping
Webscraping project using selenium to scrape data of Merolagani.

## Project Overview
This project involves data scraping from the MeroLagani website, a platform for NEPSE stocks information, IPO/FPO applications, profile viewing, and predictions.

## Tools and Technologies
- Python 3.11.8
- chromedriver-autoinstaller
- selenium
- beautifulsoup4

## Project Structure
- .github/workflows/seleniumcraping.yml
- main.py
- README.md

## `main.py` Description
The `main.py` file contains the main scraping operation code using selenium and beautifulsoup4 libraries to:
- Request the provided URL using chromedriver
- Search for the "hdl" stock through the search box
- Navigate to HDL's profile and access the floor sheet tab
- Extract categories from the floor sheet (S.N, Date, Transact. No., Buyer, Seller, Qty., etc.)
- Scroll through pagination to collect all transaction data
- Filter out redundant spaces and unwanted data
- Create and store data row-wise in "hdlscrapdata.csv"

## `seleniumcraping.yml` Description
This GitHub Actions YAML file sets up the environment, downloads dependencies, and specifies the schedule using cron syntax to run every Monday and Thursday at 12 am.

## Local Setup
1. Create and activate a virtual environment for Python.
2. Install dependencies: `pip install chromedriver-autoinstaller selenium beautifulsoup4`
3. Run `python main.py` to start scraping and data will be written to "hdlscrapdata.csv".

## Conclusion
The project, required for a Data Acquisition class, simplifies data scraping for beginners using selenium.

