import tldextract
import subprocess
import ipaddress
import platform
import pwinput
import typing
import random
import socket
import ctypes
import httpx
import time
import sys
import os
import re

chars = r"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=:;'\}]{[/?.>,<"

# Useragent 
USER_AGENT = '5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5666.197 Safari/537.36'

# Title
def update_console_title():
    variations = ["|", "/", "-", "\\"]
    while True:
        for variation in variations:
            title = f"Versatile {variation} {os.getlogin()}"
            ctypes.windll.kernel32.SetConsoleTitleW(title)
            time.sleep(0.5)


# Auto pip install the package
for package in [['pwinput'], ['httpx'], ['pyperclip'], ['tldextract']]:
    try:
        __import__(package[-1])
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package[0]])

# clear
sys_os = platform.system()
def clear():
    os.system("cls") if sys_os == "Windows" else os.system('clear')


def get_self_ip() -> str | None:
	response = httpx.get('https://userapi.site/get_ip.php', headers={'User-Agent': USER_AGENT})

	if response.status_code != 200:
		return None

	return response.json()['message']

def get_private_ip():
	hostname = socket.gethostname()
	ip_address = socket.gethostbyname(hostname)
	if ip_address.startswith('::ffff:'):
		ip_address = ip_address[7:]
	return ip_address


def generate_password(length):
    return "".join(random.choice(chars) for _ in range(length))


def press_enter_to_continue():
    pwinput.pwinput(
        prompt=f"\n{TextColor.white}Press enter to continue...",
        mask=''
    )


def get_text_length(text: str):
	for i in TextColor.__dict__.items():
		if isinstance(i[1], str):
			text = text.replace(i[1], '')
	return len(text)


def better_print(*text, end='\n'):
	for line in text:
		for char in line:
			print(char, end='')
	print('', end=end)


def print_info(data):
    max_length = max([get_text_length(value) for value in data]) + 2
    better_print(f'{TextColor.light_black}┌{"─" * (max_length)}┐')
    for value in data:
        better_print(f'{TextColor.light_black}│{value}{" " * (max_length - get_text_length(value))}{TextColor.light_black}│')
    better_print(f'{TextColor.light_black}└{"─" * (max_length)}┘')


class Color:
    def __init__(self, r: typing.Union[int, str], g: typing.Optional[int] = None, b: typing.Optional[int] = None) -> None:
        if isinstance(r, str) and g is None and b is None:
            if not r.startswith('#'):
                r = '#' + r

            r += "0" * (6 - len(r))
            r, g, b = tuple(int(r[i:i + 2], 16) for i in (1, 3, 5))
        else:
            if g is None or not isinstance(g, int):
                g = 0

            if b is None or not isinstance(b, int):
                b = 0

        self.__r, self.__g, self.__b = r, g, b
        self.__fore: str = f"\x1b[38;2;{self.__r};{self.__g};{self.__b}m"
        self.__back: str = f"\x1b[48;2;{self.__r};{self.__g};{self.__b}m"
        self.__printable: str = f'{r}, {g}, {b}'
        self.__rgb: tuple = (self.__r, self.__g, self.__b)

    class InvalidType(Exception):
        pass

    @property
    def fore(self):
        return self.__fore

    @property
    def back(self):
        return self.__back

    @property
    def printable(self):
        return self.__printable

    @property
    def rgb(self):
        return self.__rgb

    @property
    def r(self):
        return self.__r

    @property
    def g(self):
        return self.__g

    @property
    def b(self):
        return self.__b


class TextColor:
    yellow = Color(255, 255, 0).fore
    red = Color(255, 0, 0).fore
    green = Color(0, 128, 0).fore
    lime = Color(0, 255, 0).fore
    blue = Color(0, 0, 255).fore
    royal_blue = Color(65, 105, 225).fore
    electric_purple = Color(184, 0, 255).fore
    cyan = Color(0, 246, 255).fore
    white = Color(255, 255, 255).fore
    grey = Color(128, 128, 128).fore
    black = Color(0, 0, 0).fore
    light_black = Color(90, 90, 90).fore
    light_blue = Color(173, 216, 230).fore
    reset = white


def create_gradient(start_rgb, end_rgb):
    # Extract the individual RGB components
    start_r, start_g, start_b = start_rgb
    end_r, end_g, end_b = end_rgb

    # Calculate the difference between the start and end RGB values
    diff_r = end_r - start_r
    diff_g = end_g - start_g
    diff_b = end_b - start_b

    # Calculate the number of steps needed for the gradient
    steps = max(abs(diff_r), abs(diff_g), abs(diff_b))

    # Calculate the increment for each RGB component
    increment_r = diff_r / steps
    increment_g = diff_g / steps
    increment_b = diff_b / steps

    # Generate the gradient by incrementing the RGB values
    gradient = []
    for i in range(steps + 1): # type: ignore
        r = int(start_r + i * increment_r)
        g = int(start_g + i * increment_g)
        b = int(start_b + i * increment_b)
        gradient.append((r, g, b))
    return gradient


def get_gradient(text, gradient):
    text_length = len(text)
    gradient_length = len(gradient)

    # Calculate the ratio between the text length and gradient length
    ratio = gradient_length / text_length

    # Initialize an empty string to store the formatted text
    formatted_text = ""

    # Iterate over each character in the text
    for i, char in enumerate(text):
        gradient_index = int(i * ratio)
        rgb = gradient[gradient_index]
        rgb_string = f"{rgb[0]};{rgb[1]};{rgb[2]}"
        formatted_char = f"\033[38;2;{rgb_string}m{char}\033[0m"
        formatted_text += formatted_char
    return formatted_text


def ip_lookup(ip: str) -> dict:
    try:
        response = httpx.get(f'https://freeipapi.com/api/json/{ip}', headers={'User-Agent': USER_AGENT})
        if response.status_code == 200:
            return {
                'status': True,
                'data': response.json()
            }
        else:
            return {
                'status': False,
                'message': f'Invalid response ({response.status_code})'
            }
    except Exception as e:
        return {
            'status': False,
            'message': f'Unexpected error: {e}'
        }


def get_weather_info(code: str) -> dict:
	try:
		response = httpx.get(
			f'http://api.weatherapi.com/v1/current.json?key=638e350524ab4650a4303224220807&q={code}&aqi=no', headers={'User-Agent': USER_AGENT})
		if response.status_code == 200:
			return {
				'status': True,
				'data': response.json()
			}
		else:
			return {
				'status': False,
				'message': f'Invalid response ({response.status_code})'
			}
	except Exception as e:
		return {
			'status': False,
			'message': f'Unexpected error: {e}'
		}


def is_valid_zip_code(zip_code):
	pattern = r'^\d{5}(-\d{4})?$'
	return bool(re.match(pattern, zip_code))


def is_valid_domain(domain):
	ext = tldextract.extract(domain)
	if ext.domain and ext.suffix:
		return True
	else:
		return False


def is_valid_ip(ip):
	try:
		ipaddress.ip_address(ip)
		return True
	except ValueError:
		return False


def get_color(value):
    if value < 61:
        return TextColor.lime
    elif 60 < value < 100:
        return TextColor.yellow
    else:
        return TextColor.red

gradient = create_gradient((0, 255, 255), (191, 0, 255))
Name = "Versatile-User0420"