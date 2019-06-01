from django.test import TestCase
from django.conf import settings
#from django.conf import settings
#settings.configure()
from applications.events.models import Event, Location
from applications.users.models import User
import datetime
from faker import Faker
import random
import string


#You must define the relevant variable to show where you settings.py file lives:

class EventPopulator():
    def __init__(self):
        self.faker = Faker()

    def create_events(self, num):
        counter = 0

        for i in range(100):
            username = self.faker.name()
            email = username.split(" ")[0] + "." + username.split(" ")[1] + "@gmail.com"
            user = User(email=email, is_staff=False, is_superuser=False, date_joined=datetime.datetime.now())
            user.save()

            language = "English"
            location_name = self.faker.text().split(" ")[0]
            location = Location.objects.get_or_create(location_name=location_name)
            tags = self.generate_tag_string()
            rand_day = self.generate_random_date()
            start_time, end_time = self.generate_random_time(rand_day)
            event_id = self.generate_event_id()
            event_name = self.generate_event_name() + "(" + event_id + ")"
            event = Event(event_id=event_id,
                          image_storage_url=settings.MEDIA_URL + "placeholders/placeholder_700x400.png/",
                          name= self.generate_event_name(), start_date=rand_day, end_date=rand_day, start_time=start_time, end_time=end_time,
                          language=language, tags=tags, location=location[0], description="Created by tests.py", host_name=username, host=user)
            event.save()
            counter +=1
        print(str(counter) + " events and users have been added.")

    def generate_random_date(self):
        year = random.choice(range(2019, 2021))
        month = random.choice(range(1, 13))
        day = random.choice(range(1, 29))
        date = datetime.datetime(year, month, day)
        return date

    def generate_random_time(self, date):
        time1 = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=random.choice(range(0, 24)), minute=random.choice([0, 30]))
        time2 = time1 + datetime.timedelta(hours=random.choice(range(1, 5)))
        return time1, time2

    def generate_event_name(self):
        name = self.faker.text()
        if len(name) > 30:
            temp = name
            name = ""
            for i in temp.split(" ")[0:3]:
                i += " "
                name += i
        return name

    def generate_event_id(self):
        event_id = ""
        for i in range(10):
            if random.randint(0, 1) == 0:
                event_id += str(random.randint(0, 9))
            else:
                event_id += random.choice(string.ascii_uppercase)
        return event_id

    def generate_tag_string(self):
        tag_seed = self.faker.text()
        tags = tag_seed.split(" ")
        tag_string = ""
        if len(tags) > 10:
            for i in tags[0:10]:
                tag_string = tag_string + "#" + i
                tag_string += ", "
        else:
            for i in tags:
                tag_string += i
                tag_string += ","
        return tag_string

def main():
    populator = EventPopulator()
    populator.create_events(100)

main()
