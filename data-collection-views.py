from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from screeninfo import get_monitors
from user_agents import parse
from ip2geotools.databases.noncommercial import DbIpCity
import socket
from .models import users


#THESE ARE GLOBAL VARIABLES TO KEEP TRACK OF DEVICE COUNT SO IT DOESN'T EARSE WHEN THE USER REFRESHES THE PAGE 
mobile = 0 
tablet = 0
monitor = 0


def index(request):
    if request.method == "GET":
        print("#######################################################################\n")
        print(f"\n##### USER AGENT INFORMATION #####\n")

    #THIS CALLS FOR THE NAME OF DEVICE MAKING THE REQUEST
        device=socket.gethostname()
        print(f"Device Name: {device}")

    #THIS IS DJANGO 2.2 INBUILT FUNCTION. THIS ALLOWS TO RETRIVE THE IP ADDRESS MAKING THE REQUEST
        address=request.META.get("REMOTE_ADDR")
        print(f"IP: {address}")

    #PASS THE {adress} VARIABLE UNTO THE GEO LOCATION, THE API_KEY IS ALWAYS 'free"
        response = DbIpCity.get(f"{address}", api_key='free')
        print(f"User Location: {response.city}, {response.region} {response.country}")
        print(f"User Exact Location: Lattitude {response.latitude} Longitude {response.longitude}")
        city_name = str(response.city)
        region_name = str(response.region)
        country_name = str(response.country)
        latitude_exact = response.latitude
        longitude_exact = response.longitude

    #THIS IS DJANGO 2.2 INBUILT FUNCTION. THIS ALLOWS TO RETRIVE THE INFORMATION ON THE DEVICE
        user_info = request.headers['User-Agent']

    #THIS IS HOW TO PARSE THE {user_info} STRING. THIS THE user_agent PACKAGE AT WORK
        ua_string = str(user_info)
        user_agent = parse(ua_string)
        print(f"OS: {user_agent.os.family}")
        print(f"Browser: {user_agent.browser.family} v{user_agent.browser.version_string}")
        print(f"Device: {user_agent.device.family}")
        device_type = None
        if user_agent.is_mobile == True:
            device_type = "Mobile"
            global mobile
            mobile+=1
        if user_agent.is_tablet == True:
            device_type = "Tablet"
            global tablet
            tablet+=1
        if user_agent.is_pc == True:
            device_type = "Desktop"
            global monitor
            monitor+=1
        print(f"Device Type: {device_type}")
        print(f"Touch Capabilities: {user_agent.is_touch_capable}")
        print(f"Bot Request: {user_agent.is_bot}")
        if user_agent.is_bot == True:
            print("THE MITCHELLS GOT ME")
            return HttpResponse("NO BOTS")
    #THIS SHOWS THE REQUEST NUMBER GIVING THEM ONE MORE UNIQUE ID 
        ticket=mobile+tablet+monitor
        print(f"Ticket #{ticket}")
        print("\n#### REQUEST COUNT and DEVICE COUNT #####\n")
        print(f"Total Request: Mobile - {mobile}, Tablet - {tablet}, Monitor - {monitor}\n")
        print("#######################################################################\n")
        users.objects.create(
            #about the user
            ip = address,
            ticket_id = ticket,
            is_bot = user_agent.is_bot,
            #user location
            country = country_name,
            city = city_name,
            region = region_name,
            latitude = latitude_exact,
            longitude = longitude_exact,
            # about the device 
            device_name = device,
            device_family = user_agent.device.family,
            device_type = device_type,
            device_os = user_agent.os.family,
        )

        return render(request, "index.html")
    else:
        if request.method == "POST":
            return HttpResponseRedirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")