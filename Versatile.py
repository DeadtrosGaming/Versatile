# Imports
from backend import *
import threading
import pyperclip
import ui_stuff
import random

title_thread = threading.Thread(target=update_console_title)
title_thread.daemon = True  # Allow the thread to exit when the main program exits
title_thread.start()

while True:
    clear()
    print(get_gradient(ui_stuff.Main, gradient))

    choice = input(f"{TextColor.light_black}\n┌─{TextColor.green}{get_gradient(Name, gradient)}{TextColor.light_black}\n└───▶{TextColor.reset} ").strip().split(" ")
    command = choice[0].lower()
    try:
        value = choice[1]
    except:
        value = None

    if command == "help":
        clear()
        print(get_gradient(ui_stuff.Help, gradient))
        press_enter_to_continue()

    elif command == "lookup":
        if (value):
            host = value
        else:
            host = input(f"{TextColor.royal_blue}IP{TextColor.light_black} ───▶{TextColor.reset} ").strip()

        if not is_valid_domain(host) and not is_valid_ip(host):
            print(f"\n{TextColor.red}Invalid host.{TextColor.reset}")

        print(f'{TextColor.electric_purple}Please wait...{TextColor.reset}', end='\r', flush=True)
        IP_Info = ip_lookup(host)
        if IP_Info['status']:
            data = IP_Info['data']
            lookup_data = [
                f' {TextColor.royal_blue}IP            {TextColor.reset}:   {data["ipAddress"]}',
                f' {TextColor.royal_blue}Latitude      {TextColor.reset}:   {data["latitude"]}',
                f' {TextColor.royal_blue}Longitude     {TextColor.reset}:   {data["longitude"]}',
                f' {TextColor.royal_blue}Country       {TextColor.reset}:   {data["countryName"]}',
                f' {TextColor.royal_blue}ZipCode       {TextColor.reset}:   {data["zipCode"]}',
                f' {TextColor.royal_blue}City          {TextColor.reset}:   {data["cityName"]}',
                f' {TextColor.royal_blue}Region        {TextColor.reset}:   {data["regionName"]}'
            ]
            print_info(lookup_data)
        press_enter_to_continue()

    elif command == "ping":
        if (value):
            ip = value
        else:
            ip = input(f"{TextColor.royal_blue}IP{TextColor.light_black} ───▶{TextColor.reset} ").strip()
        
        print(f'{TextColor.electric_purple}Please wait...{TextColor.reset}', end='\r', flush=True)
        output = subprocess.Popen(["ping", "-n", "4", ip], stdout=subprocess.PIPE).communicate()[0]
        output = output.decode("utf-8")
        if "Reply from " + ip in output:
            for line in output.split("\n"):
                if line.find("Minimum = ") != -1:
                    split = line.strip().split(',')
                    minimum = int(split[0].strip().replace('Minimum = ', '').replace('ms', ''))
                    maximum = int(split[1].strip().replace('Maximum = ', '').replace('ms', ''))
                    average = int(split[2].strip().replace('Average = ', '').replace('ms', ''))
                    values = [
                        f'  Minimum:{get_color(minimum)} {minimum}ms',
						f'  Maximum:{get_color(maximum)} {maximum}ms',
						f'  Average:{get_color(average)} {average}ms'
					]
                    print_info(values)
        press_enter_to_continue()

    elif command == "passgen":
        if (value):
            password_length = value
        else:
            password_length = input(f"{TextColor.royal_blue}Length{TextColor.light_black} ───▶{TextColor.reset} ").strip()

        print(f'{TextColor.electric_purple}Please wait...{TextColor.reset}', end='\r', flush=True)
        password_length = random.randint(30, 300) if password_length == "" else int(password_length)
        generated_password = generate_password(password_length)
        print(f"{TextColor.royal_blue}Password is: {TextColor.reset}{generated_password}")
        print("Password copied to clipboard.")
        pyperclip.copy(f"{generated_password}")
        press_enter_to_continue()

    elif command == "info":
        self_ip = get_self_ip() or 'Failed to Retrieve'
        private_ip = get_private_ip() or 'Failed to Retrieve'

        info = [
        f'{TextColor.white} This is developed by User0420',
        f'{TextColor.royal_blue} Your Public IP: {TextColor.lime if self_ip != "Failed to Retrieve" else TextColor.red}{self_ip}{TextColor.reset}',
        f'{TextColor.royal_blue} Your Private IP: {TextColor.lime if private_ip != "Failed to Retrieve" else TextColor.red}{private_ip}{TextColor.reset}'
        ]
        print_info(info)
        press_enter_to_continue()

    elif command == "weather":
        if (value):
            zip_code = value
        else:
            zip_code = input(f"{TextColor.royal_blue}ZIP code{TextColor.light_black} ───▶{TextColor.reset} ").strip()

        if not is_valid_zip_code(zip_code):
            print(f"{TextColor.red}Invalid Zip Code.")

        print(f'{TextColor.electric_purple}Please wait...{TextColor.reset}', end='\r', flush=True)
        weather_info = get_weather_info(zip_code)
        if weather_info['status']:
            data = weather_info['data']
            weather_data = [
            f'{TextColor.royal_blue}Time            {TextColor.reset}:   {data["location"]["localtime"]}',
            f'{TextColor.royal_blue}City            {TextColor.reset}:   {data["location"]["name"]}',
            f'{TextColor.royal_blue}State           {TextColor.reset}:   {data["location"]["region"]}',
            f'{TextColor.royal_blue}Country         {TextColor.reset}:   {data["location"]["country"]}',
            f'{TextColor.royal_blue}Timezon         {TextColor.reset}:   {data["location"]["tz_id"]}',
            f'{TextColor.royal_blue}Clouds          {TextColor.reset}:   {data["current"]["cloud"]}',
            f'{TextColor.royal_blue}Humidity        {TextColor.reset}:   {data["current"]["humidity"]}%',
            f'{TextColor.royal_blue}UV Index        {TextColor.reset}:   {data["current"]["uv"]}',
            f'{TextColor.royal_blue}Pressure        {TextColor.reset}:   {data["current"]["pressure_in"]} in, {data["current"]["pressure_mb"]} mb.',
            f'{TextColor.royal_blue}Condition       {TextColor.reset}:   {data["current"]["condition"]["text"]}',
            f'{TextColor.royal_blue}Day/Night       {TextColor.reset}:   {"Day" if data["current"]["is_day"] == 1 else "Night"}',
            f'{TextColor.royal_blue}Wind Speed      {TextColor.reset}:   {data["current"]["wind_mph"]} mph, {data["current"]["wind_kph"]} kph.',
            f'{TextColor.royal_blue}Visibility      {TextColor.reset}:   {data["current"]["vis_miles"]} miles, {data["current"]["vis_km"]} km.',
            f'{TextColor.royal_blue}Temperature     {TextColor.reset}:   {data["current"]["temp_f"]}°F, {data["current"]["temp_c"]}°C',
            f'{TextColor.royal_blue}Precipitation   {TextColor.reset}:   {data["current"]["precip_in"]} in, {data["current"]["precip_mm"]} mm.'
            ]
            print_info(weather_data)
        press_enter_to_continue()