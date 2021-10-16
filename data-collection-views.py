from django.http.response import HttpResponse
from django.shortcuts import render, HttpResponse, redirect

'''THIS PACKAGE GETS THE SCREEN DIMENSIONS
    >> pip install screeninfo
'''
from screeninfo import get_monitors

''' THIS PACAKGE ALLOWS TO PARSE THE request.headear['User_agent'](see:https://docs.djangoproject.com/en/2.2/ref/request-response/#django.http.HttpRequest.META),
    
        MEANING IT WILL GIVE KEYS TO THE VALUES https://pypi.org/project/user-agents/ 
        >> pip install pyyaml ua-parser user-agents
'''
from user_agents import parse

'''THIS PACKAGE ALLOWS TO GEO LOCATE AN IP ADDRESS
        TO PASS A ACTIVE IP PASS THE 
        "IP=request.META.get("REMOTE_ADDR")" as an arguement in 
        response = DbIpCity.get(f"{IP}", api_key='free')
        response.key
        https://pypi.org/project/ip2geotools/
'''
from ip2geotools.databases.noncommercial import DbIpCity

'''THIS IS A MODULE IN PYTHON3.X TO GET INFORMATION ON THE REQUEST

'''
import socket



#THESE ARE GLOBAL VARIABLES TO KEEP TRACK OF DEVICE COUNT SO IT DOESN'T EARSE WHEN THE USER REFRESHES THE PAGE 
mobile = 0 
tablet = 0
monitor = 0

def index(request):
    print("#######################################################################\n")
    print(f"\n##### USER AGENT INFORMATION #####\n")

#THIS CALLS FOR THE NAME OF DEVICE MAKING THE REQUEST
    device=socket.gethostname()
    print(f"Device Name: {device}")

#THIS LOOPS THROUGH ALL POTENTIAL SCREEN TYPE BY RETURNING DIMENSIONS OF A SCREEN USING THE screeninfo PACKAGE
    for m in get_monitors():
        if m.width < 768:
            global mobile
            mobile+=1
            print(f"Screen Type - Mobile: {m.width} X {m.height}")
        elif 768 < m.width < 1024:
            global tablet
            tablet+=1
            print(f"Screen Type - Tablet: {m.width} X {m.height}")
        elif m.width>1024:
            global monitor
            monitor+=1
            print(f"Screen Type - Monitor: {m.width} X {m.height}")

#THIS IS DJANGO 2.2 INBUILT FUNCTION. THIS ALLOWS TO RETRIVE THE IP ADDRESS MAKING THE REQUEST
    address=request.META.get("REMOTE_ADDR")
    print(f"IP: {address}")

#PASS THE {adress} VARIABLE UNTO THE GEO LOCATION, THE API_KEY IS ALWAYS 'free"
    response = DbIpCity.get(f"{address}", api_key='free')
    print(f"User Location: {response.city}, {response.region} {response.country}")
    print(f"User Exact Location: Lattitude {response.latitude} Longitude {response.longitude}")

#THIS IS DJANGO 2.2 INBUILT FUNCTION. THIS ALLOWS TO RETRIVE THE INFORMATION ON THE DEVICE
    user_info = request.headers['User-Agent']

#THIS IS HOW TO PARSE THE {user_info} STRING. THIS THE user_agent PACKAGE AT WORK
    ua_string = str(user_info)
    user_agent = parse(ua_string)
    print(f"OS: {user_agent.os.family}")
    print(f"Browser: {user_agent.browser.family} v{user_agent.browser.version_string}")
    print(f"Device Type: {user_agent.device.family}")
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
    return render(request, "index.html")