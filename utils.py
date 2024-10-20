from datetime import datetime, date, timedelta

from config import LOGGING

# log function
def write_log(content, log_type):
    if not LOGGING:
        return

    # get time and date
    today = datetime.now().strftime("%Y%m%d")
    file = "logs/"+ today + "_log.txt"
    content = str(content)
    with open(file, "a", encoding="utf-8") as file:
        file.write(datetime.now().strftime("%A, %d %B %Y, %H:%M:%S") + "; " + log_type + "; " + content + "\n")

def get_past_dates(n_days):
    if not isinstance(n_days, int) or n_days < 1:
        raise ValueError("'n_days' must be an integer greater than zero.")
    end_date = date.today() - timedelta(days=1)
    start_date = date.today() - timedelta(days=n_days)
    return str(start_date) + " - " + str(end_date)