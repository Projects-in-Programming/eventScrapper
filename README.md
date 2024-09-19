# eventScraper

This is a Python program that scrapes event data from the NYU Events website (www.events.nyu.edu) for the current week. It uses the Selenium WebDriver to navigate the website and BeautifulSoup to parse the HTML. The script extracts the event name, date, start time, end time, and link for each event and stores the data in a list of dictionaries. The list is then converted to a Pandas DataFrame and saved as a CSV file.

### Why events.nyu.edu ?

The events page of the website has listing of so many events and we wanted a way to have a quick way for someone to run an analysis on the event listing for a week and do something like  with it. This program aims to provide list of events for a whole week in a simple `.csv` file. 

### Design Choice

We decided to use selenium here because the website contains JS loader and using just Beautiful soup would not capture the loaded data. 

## Requirements

* Python 3.x
* Selenium
* BeautifulSoup
* Pandas
* Chrome WebDriver (or another WebDriver of your choice)

## Installation

1. Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

## Usage

1. Clone the repository to your local machine.
2. Open the script in a text editor and modify the `RATE_LIMIT` variable to set the desired rate limit for requests to the website (in seconds).
3. Run the script using Python:

```bash
python event_scraper.py
```

4. The script will create a CSV file called `file.csv` in the same directory containing the event data.

## Notes

* The script only scrapes events for the current week, starting from the current day and ending on Sunday.
* The script uses a rate limit to avoid overloading the website with requests. The default rate limit is 1 second, but you can modify this value as needed.
* The script uses error handling to catch `TimeoutException` errors that may occur when accessing the website. If a `TimeoutException` error occurs, the script will print an error message and continue to the next iteration of the loop.
* The script assumes that the HTML structure of the NYU Events website will not change. If the website's HTML structure changes, the script may need to be modified to continue working correctly.


## Future Work

* Allow user to select date range and get the events
* Add Search feature so that users can directly get  events based on filters. 
