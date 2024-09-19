import time
import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd

# Set up the WebDriver
driver = webdriver.Chrome()
Events = []

# Set a rate limit (in seconds)
RATE_LIMIT = 1

# converting date to string to put in the website
def conv_date_to_string(today_date):
  today_date = str(today_date)
  today_date = today_date.replace('-','')
  return today_date

# function to correct the url if it is not complete
def correct_url(url):
    if url[0] == 'h':
        return url
    else:
        return 'https://www.events.nyu.edu' + url

# function to get the event pages for the week
def get_event_pages_for_week():
    today = datetime.date.today()
    day_of_the_week = today.weekday()
    today_str = conv_date_to_string(today)
    print(day_of_the_week)

    # running the loop until Sunday
    while day_of_the_week <= 6:
        webpage = "https://events.nyu.edu/day/date/" + today_str
        print(webpage)

        # error handling for TimeoutException
        try:
            driver.get(webpage)
            time.sleep(RATE_LIMIT)
        except TimeoutException:
            print(f"Timeout error occurred while accessing {webpage}")
            continue

        # Parse the page source with Beautiful Soup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # For the top highlighted Event
        feature_top = soup.find_all('div', class_ = 'feature-top')
        for feature in feature_top:

            # get url to the event
            link = feature.find('a', href = True)['href']
            link = correct_url(link)
            
            # getting the event detail container and accessing all the details
            feature = feature.find('div', {'class': 'feature-top-info' })
            event_name = feature.h4.text

            # start time, first check if its there
            if feature.find('div', {'class': 'nyu-date-time'}).find('span', {'class': 'lw_start_time'}):
                start = feature.find('div', {'class': 'nyu-date-time'}).find('span', {'class': 'lw_start_time'}).text
            else:
                start = None

            # end time, first check if its there
            if feature.find('div', {'class': 'nyu-date-time'}).find('span', {'class': 'lw_end_time'}):
                end = feature.find('div', {'class': 'nyu-date-time'}).find('span', {'class': 'lw_end_time'}).text
            else:
                end = None

            # add event to the list
            Events.append({'Event Name': event_name,'Date': today, 'Start':start , 'End': end, 'Link': link})

        # For other events
        
        # lw_cal_event is  hte container that contains details for each event
        all_events = soup.find_all('div', class_='lw_cal_event')
        n = 1
        for target in all_events:
            # get the event name and link
            title = target.find('div', {'class':'lw_events_title'})
            text = title.a.text
            link = title.a['href']
            link = correct_url(link)

            # get the start and end time
            time_ = target.find('div', {'class':'nyu-date-time'})
            if time_.find('span', {'class': 'lw_start_time'}):
                start = time_.find('span', {'class': 'lw_start_time'}).text
            else:
                start = None
            if time_.find('span', {'class': 'lw_end_time'}):
                end = time_.find('span', {'class': 'lw_end_time'}).text
            else:
                end = None

            # add event to the list
            Events.append({'Event Name': text,'Date': today, 'Start':start , 'End': end, 'Link': link})
            n += 1
        print(f'{n} events for {today}')

        # Increment the date
        today = today + datetime.timedelta(days=1)
        today_str = conv_date_to_string(today)
        day_of_the_week = day_of_the_week + 1

get_event_pages_for_week()

# Create a DataFrame from the list of events
df = pd.DataFrame(Events)
df.to_csv('file.csv', index=False)
# print(df)
