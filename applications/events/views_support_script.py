import random
import string

def generate_event_id():
    event_id = ""
    for i in range(10):
        if random.randint(0, 1) == 0:
            event_id += str(random.randint(0, 9))
        else:
            event_id += random.choice(string.ascii_uppercase)
    return event_id