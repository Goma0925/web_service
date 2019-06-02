from PIL import Image, ImageOps, ImageDraw
from applications.events.models import Event

def put_circle_layer_on(image):
    #print("Putting a layer on image:", str(image))
    size = (128, 128)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    output = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    return output

def retrieve_event_objs(id_list):
    events = list()
    for event_id in id_list:
        event = Event.objects.filter(event_id=event_id)
        event[0].start_date = str(event[0].start_date.month) + "/" + str(event[0].start_date.day) + "/" + str(event[0].start_date.year)
        event[0].end_date = str(event[0].end_date.month) + "/" + str(event[0].end_date.day) + "/" + str(event[0].end_date.year)
        events += event
    return events
