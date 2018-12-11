from datetime import date, datetime
import random

date = date.today()
#time1 = datetime(year=date.year, month=date.month, day=date.day, hour=random.choice(range(0, 24)),
#                          minute=random.choice([0, 30]))
#time2 = time1 + datetime.timedelta(hours=random.choice(range(1, 5)))
print("Date:", date)
#print("Time zone:", datetime.timezone.tzname())