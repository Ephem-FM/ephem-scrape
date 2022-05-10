import kutx989
import koop917
import calendar
from datetime import date

def main():
    kutx989.main()
    today = calendar.day_name[date.today().weekday()]
    if today == "Wednesday":
        koop917.main()

if __name__=="__main__":
    main()