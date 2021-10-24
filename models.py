from django.db import models

#global variables
mobile = 0
tablet = 0
desktop = 0

class device_count(models.Model):
    mobile_count = mobile
    tablet_count = tablet
    desktop_count = desktop


class users(models.Model):

#about the user
    ip = models.CharField(max_length=255)
    ticket_id = models.CharField(max_length=255)
    is_bot = models.BooleanField(default=False)

#user location
    country = models.CharField(max_length=255)
    if country == None or country == "":
        country = "Unknown"
    city = models.CharField(max_length=255)
    if city == "" or city == None:
        city = "Unknown"
    region = models.CharField(max_length=255)
    if region == None or region == "":
        region = "Unknown"
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)

# about the device 
    device_name=models.CharField(max_length=255)
    device_family = models.CharField(max_length=255)
    device_type = models.CharField(max_length=255)
    device_os = models.CharField(max_length=255)
    touch_capability = models.BooleanField(default=False)
    device_count = models.CharField(max_length=255)
    if device_count == "Mobile":
        global mobile
        mobile += 1
    elif device_count == "Tablet":
        global tablet
        tablet += 1
    elif device_count == "Desktop":
        global desktop  
        desktop += 1

# dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
