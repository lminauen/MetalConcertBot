from datetime import datetime

# log function
def write_log(content, log_type):
    # get time and date
    today = datetime.now().strftime("%Y%m%d")
    file = "logs/"+ today + "_log.txt"
    content = str(content)
    with open(file, "a", encoding="utf-8") as file:
        file.write(datetime.now().strftime("%A, %d %B %Y, %H:%M:%S") + "; " + log_type + "; " + content + "\n")
