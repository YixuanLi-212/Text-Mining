## Get the currency rate from the website
import requests
from bs4 import BeautifulSoup

## URL of the Google Finance Page
url = "https://www.google.com/finance/quote/USD-CNY?sa=X&ved=2ahUKEwizo4qn7_iAAxWJmmoFHdXpDtIQmY0JegQIARAn"

## Send an HTTP GET request to the URL
response = requests.get(url)

## Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find the element containing the exchange rate
    exchange_rate_element = soup.find("div", {"class": "YMlKec fxKbKc"})
    # Extract the exchange rate (number)
    today_exchange_rate = round(float(exchange_rate_element.text.strip()),2)

## Update google sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Initialize the Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/yixuanli/Desktop/price-tracking-397023-d06b5fe9029a.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheets document by its sheet id
sheet_id = '1hD-jCYuQqxLP0RbL_PlQmsHiS6ipAAnH_aaNZbNCW_Y'

# Access the worksheet I want to work on
try:
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.get_worksheet(0)
    cell = worksheet.acell('H2')

except gspread.exceptions.SpreadsheetNotFound:
    print(f"Google Sheets document with ID {sheet_id} not found.")

# Update the cell with the current date
cell.value = today_exchange_rate

