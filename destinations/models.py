from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    division = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    best_time = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    main_image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    extra_image1 = models.ImageField(upload_to='destinations/', blank=True, null=True)
    extra_image2 = models.ImageField(upload_to='destinations/', blank=True, null=True)
    extra_image3 = models.ImageField(upload_to='destinations/', blank=True, null=True)
    extra_image4 = models.ImageField(upload_to='destinations/', blank=True, null=True)
    extra_image5 = models.ImageField(upload_to='destinations/', blank=True, null=True)
    extra_image6 = models.ImageField(upload_to='destinations/', blank=True, null=True)

    def __str__(self):
        return self.name

