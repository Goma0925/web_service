from django.test import TestCase
from django.conf import settings
#from django.conf import settings
#settings.configure()
from applications.events.models import Event, Location
from applications.users.models import User, UserProfile
import datetime
from faker import Faker
import random
import string


#You must define the relevant variable to show where you settings.py file lives:

def choose_sample_event_img():
    return "sample_event_img" + str(random.randint(1, 7)) + ".jpg"

def choose_sample_profile_img():
    return "sample_profile_img" + str(random.randint(1, 4)) + ".jpg"

class EventPopulator():
    def __init__(self):
        self.faker = Faker()

    def create_events(self, num):
        counter = 0

        for i in range(100):
            username = self.faker.name()
            email = username.split(" ")[0] + "." + username.split(" ")[1] + "@gmail.com"
            user = User(email=email, is_staff=False, is_superuser=False, date_joined=datetime.datetime.now())
            print("USERHERE:", user)
            profile = UserProfile()
            profile.profile_image_storage_url = settings.MEDIA_URL + "sample_profile_images/" + choose_sample_profile_img() + "/"
            profile.first_name = username.split(" ")[0]
            profile.last_name = username.split(" ")[0]
            user.save()
            profile.user = user
            profile.save()

            language = "English"
            location_name = "Example Location" + str(random.randint(1, 100))
            location = Location.objects.get_or_create(location_name=location_name)
            tags = self.generate_tag_string()
            rand_day = self.generate_random_date()
            start_time, end_time = self.generate_random_time(rand_day)
            event_id = self.generate_event_id()
            event_name = "Example hangout-" + str(i)
            event_description = '"Created by tests.py" Primus gradus est, in ipso constituere res planning tuis tractabilem et finis aliquip. Primum incipere petendo a te: Quare tu res quod organizing et spes ad consequi Quid ergo? Amet congue mauris ante organizationem si nosti, omnia potest ut pars eventus victoriae dolor. Tu es trying ad hominum conscientias movendas et causa, non potest fieri per colligunt tua donations moles deinde project? Tu sperans ad attrahunt convivae L vel D?Contra occidentem fine successu quantifiable metrica ponam te ut quadrigis facilius perveniant.'
            event = Event(event_id=event_id,
                          image_storage_url=settings.MEDIA_URL + "sample_event_images/" + choose_sample_event_img() + "/",
                          name=event_name, start_date=rand_day, end_date=rand_day, start_time=start_time, end_time=end_time,
                          language=language, tags=tags, location=location[0], description=event_description, host_name=username, host=user)
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
