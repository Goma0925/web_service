from ..applications.events import models

class EventPopulator(BaseCommand):

    def create_events(self, num):
        counter = 0
        for i in range(num):
            username = #Faker
            user = Tag(name='Java')
            user.save()

            event = Event(name='')
            event.save()
            counter



        name = models.CharField(max_length=30, blank=False)
        date = models.DateField(default=datetime.date.today, blank=False)
        start_time = models.TimeField(default=None, blank=False)
        end_time = models.TimeField(default=None, blank=False)
        # picture = models.ImageField(upload_to=get_image_path, blank=True, null=True)

        location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=False)
        description = models.CharField(max_length=160, blank=False)
        host_name = models.CharField(default="", max_length=160, blank=False)
        """↑Update: Delete"""
        host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)

    def handle(self, *args, **options):
        self._create_tags()