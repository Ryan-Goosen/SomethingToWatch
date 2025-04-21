import requests
from datetime import datetime
from datetime import UTC

def get_api_link() -> str:
    '''
    DESCRIPTION:
    - Simply return the API link updated to the current year.
    
    RETURNS:
    - Return the new api link.
    '''
    current_year = datetime.today().year
    api_link = f"https://api.jolpi.ca/ergast/f1/{current_year}/races/"
    return api_link


def get_data(api_link:str) -> dict:
    '''
    DESCRIPTION:
    - Makes an API call using the link provided.
    RETURNS:
    - Racing dates
    '''
    data = requests.get(api_link)
    raw_data = data.json()
    race_data = raw_data.get('MRData', {}).get('RaceTable', {}).get('Races', [])
    return race_data

def is_this_week(race_date:str) -> list:
    '''
    DESCRIPTION:
    - Check if a given date string is in the current ISO calendar week.

    RETURNS:
    - True if the date is in this week, else False.
    '''
    event_date = datetime.strptime(race_date, r"%Y-%m-%d").date()
    today = datetime.today().date()
    return event_date.isocalendar()[1] == today.isocalendar()[1] and event_date.year == today.year

def races_this_week(data:list) -> dict | None:
    '''
    DESCRIPTION:
    -
    RETURNS:
    - 
    '''
    for race in data:
        if is_this_week(race.get("date", "")):
            return race
    return None

def cleaning_the_data(data:dict) -> str:
    '''
    DESCRIPTION:
    - Convert UTC date/time string to local datetime.

    RETURNS:
    - Tuple containing local date and local time (date, time).
    '''   
    utc_dt_str = f"{data.get('date')} {data.get('time')}"

    local_dt = datetime.fromisoformat(utc_dt_str).replace(tzinfo=UTC).astimezone()
    local_time = local_dt.time()
    local_date = local_dt.date()

    return local_date, local_time


def main():
    api_link = get_api_link()
    api_data = get_data(api_link)
    race_data = races_this_week(api_data)
    if race_data:
        date, time = cleaning_the_data(race_data)
        return date, time
    else:
        return None

if __name__ == "__main__":
    main()
