import click
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time

@click.command()
@click.option('--website', prompt = 'Enter the website URL:', help = 'Flight booking website URL')
@click.option('--origin', prompt = 'Enter the origin city:', help = 'Origin city')
@click.option('--destination', prompt = 'Enter the destination city:', help = 'Destination city')
@click.option('--departure-date', prompt='Enter departure date (YYYY-MM-DD):', help='Start date for tracking')
@click.option('--passengers', type=int, prompt='Enter the number of passengers:', help='Number of passengers')
@click.option('--backfill-days', type=int, prompt='Enter the number of past days to track:', help='Number of past days to track')
@click.option('--show-airlines', is_flag=True, help='Show airline information')

def flight_tracker(website, origin, destination, departure_date, backfill_days, passengers, show_airlines):
    '''
    Track flight ticket prices using web scraping for a specific range of dates.
    '''
    try:
        start_date = datetime.strptime(departure_date, '%Y-%m-%d')
        date_range = [start_date - timedelta(days=i) for i in range(backfill_days)]
        
       
        for date in date_range:
            formatted_date = date.strftime('%Y-%m-%d')
            url = f"{website}?origin={origin}&destination={destination}&departure={formatted_date}&passengers=adults:{passengers},children:0,seniors:0,infantinlap:Y"
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                prices = soup.find_all('span',class_='flight_price')
                airlines = soup.find_all('div', class_='airline_name') if show_airlines else []
                for i,price in enumerate(prices):
                    airline = airlines[i].text.strip() if show_airlines and i<len(airlines) else 'N/A'
                    result = f'Date: {formatted_date}, Airline: {airline}, Price: {price.text}'
                    click.echo(result)
                time.sleep(2)
            else:
                click.echo(f"Failed to retrieve data for {formatted_date}. Status code: {response.status_code}")

    except Exception as e:
        click.echo(f'An error occurred: {str(e)}')

if __name__ == '__main__':
    flight_tracker()
