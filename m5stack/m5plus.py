from m5stack import *
from m5stack_ui import *  # type: ignore
from uiflow import *  # type: ignore
import ntptime  # type: ignore
import urequests  # type: ignore
import unit  # type: ignore
import utime  # type: ignore
import network  # type: ignore
import ure  # type: ignore
import urllib.parse

# WiFi configuration
WIFI_SSID = 'Yes'
WIFI_PASSWORD = '123456789'

running = True
backend_url = 'http://192.168.50.203:8080/'

# Initialize the PIR sensor
pir_sensor = unit.get(unit.PIR, (36, 39))

# Last motion detection time
last_motion_time = None

def connect_to_wifi():
    """
    Connect to the WiFi network using the specified SSID and password.
    Display a message on the LCD during the connection process.
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    lcd.print('Connecting to WiFi.', 0, 80, 0xff0000)  # Display connecting message
    while not wlan.isconnected():
        pass
    
    lcd.print('\b WiFi connected:', 0, 80, 0xff0000)  # Display connected message
    screen.clean_screen()
    screen.set_screen_bg_color(0xADD8E6)

def url_encode(value):
    """
    URL-encode a given value.
    """
    return ure.sub(r'[^A-Za-z0-9]', lambda x: '%%%02X' % ord(x.group(0)), str(value))

def post_data(date, time, indoor_temp, indoor_humidity, outdoor_temp, outdoor_humidity, outdoor_weather, outdoor_windspeed, detector_status, indoor_co2):
    """
    Post data to the backend server.
    """
    url = "{}post/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}".format(
        backend_url,
        url_encode(date),
        url_encode(time),
        url_encode(indoor_temp),
        url_encode(indoor_humidity),
        url_encode(outdoor_temp),
        url_encode(outdoor_humidity),
        url_encode(outdoor_weather),
        url_encode(outdoor_windspeed),
        url_encode(detector_status),
        url_encode(indoor_co2)
    )
    print(url)
    try:
        req = urequests.request(method='GET', url=url, headers={'Content-Type':'text/html'})
        response_status = req.status_code
        response_text = req.text
    except Exception as e:
        lcd.print('not ok', 0, 0, 0xffffff)  # type: ignore
        error_message = str(e)
        print("Error:", error_message)
        lcd.print(error_message, 0, 20, 0xffffff)  # type: ignore

def get_values(url):
    """
    Get values from the backend server.
    """
    url = '{}{}'.format(backend_url, url)
    try:
        response = urequests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        return None

def detect_motion():
    """
    Detect motion using the PIR sensor and display a pop-up if motion is detected.
    """
    global last_motion_time
    if pir_sensor.state:
        last_motion_time = utime.localtime()
        lcd.print("Motion Detected!", 20, 250, 0xff0000)
        utime.sleep(2)
        screen.clean_screen()
        screen.set_screen_bg_color(0xADD8E6)

def display_last_motion_time():
    """
    Display the last motion detection time on the screen.
    """
    if last_motion_time:
        time_str = "{:02}:{:02}:{:02}".format(last_motion_time[3], last_motion_time[4], last_motion_time[5])
        date_str = "{:02}/{:02}/{}".format(last_motion_time[2], last_motion_time[1], last_motion_time[0])
        label_last_motion.set_text(f"Last motion: {date_str} {time_str}")

def display_weather_icon():
    """
    Display the weather icon on the screen.
    """
    forecast = get_values('forecast')
    current_weather = forecast['list'][0]
    url = 'get_icon/{}'.format(current_weather["weather"][0]["icon"])
    icon_url = get_values(url)
    return icon_url

# Initialize the screen
screen = M5Screen()  # type: ignore
screen.clean_screen()
screen.set_screen_bg_color(0xADD8E6)
connect_to_wifi()
env3_0 = unit.get(unit.ENV3, (32, 33))
tvoc_0 = unit.get(unit.TVOC, (14, 13))

# Labels for displaying data
label_title_outdoor = M5Label('Outdoor:', x=20, y=20, color=0x000000, font=FONT_MONT_18, parent=None)  # type: ignore
label_outdoor_humidity = M5Label('Humidity: ', x=20, y=50, color=0x000000, font=FONT_MONT_14, parent=None)  # type: ignore
label_outdoor_temp = M5Label('Temp: ', x=20, y=70, color=0x000000, font=FONT_MONT_14, parent=None)  # type: ignore
label_outdoor_weather = M5Label('Weather: ', x=20, y=90, color=0x000000, font=FONT_MONT_14, parent=None)  # type: ignore
label_outdoor_windspeed = M5Label('Windspeed: ', x=20, y=110, color=0x000000, font=FONT_MONT_14, parent=None)  # type: ignore

label_title_indoor = M5Label('Indoor:', x=20, y=140, color=0x000000, font=FONT_MONT_18, parent=None)  # type: ignore
label_indoor_humidity = M5Label('Humidity: ', x=20, y=170, color=0x000000, font=FONT_MONT_14, parent=None)  # type: ignore
label_indoor_temp = M5Label('Temp: ', x=20, y=190, color=0x000000, font=FONT_MONT_14, parent=None)  # type: ignore
label_indoor_co2 = M5Label('CO2: ', x=20, y=210, color=0x000000, font=FONT_MONT_14, parent=None)  # type: ignore

label_date = M5Label('Date: ', x=200, y=20, color=0x000000, font=FONT_MONT_14, parent=None)  # type: ignore
label_time = M5Label('Time: ', x=200, y=50, color=0x000000, font=FONT_MONT_14, parent=None)  # type: ignore
label_last_motion = M5Label('Last motion:', x=20, y=230, color=0x000000, font=FONT_MONT_14, parent=None)

count = 0

while running:
    indoor_temp = env3_0.temperature
    indoor_humidity = env3_0.humidity
    indoor_co2 = tvoc_0.eCO2

    date = get_values('date')
    time = get_values('time')
    detector_status = pir_sensor.state
    outdoor_temp = get_values('outdoor_temp')
    outdoor_humidity = get_values('outdoor_humidity')
    outdoor_weather = str(get_values('outdoor_weather'))
    outdoor_windspeed = get_values('outdoor_windspeed')
    
    post_data(date, time, indoor_temp, indoor_humidity, outdoor_temp, outdoor_humidity, outdoor_weather, outdoor_windspeed, detector_status, indoor_co2)
    
    label_outdoor_humidity.set_text('Humidity: ' + str(outdoor_humidity) + ' %')
    label_outdoor_temp.set_text('Temp: ' + str(outdoor_temp) + ' °C')
    label_outdoor_weather.set_text('Weather: ' + outdoor_weather)
    label_outdoor_windspeed.set_text('Windspeed: ' + str(outdoor_windspeed) + ' km/h')

    label_indoor_humidity.set_text('Humidity: ' + str(indoor_humidity) + ' %')
    label_indoor_temp.set_text('Temp: ' + str(indoor_temp)+ ' °C')
    label_indoor_co2.set_text('CO2: ' + str(indoor_co2))

    label_date.set_text('Date: ' + date)
    label_time.set_text('Time: ' + time)
    
    display_last_motion_time()
    
    if count == 0:
        count = count + 1
        url = 'Good evening, it is {} and the weather is {}. The outside temperature is {}'.format(time, outdoor_weather, outdoor_temp)
        speaker.playCloudWAV('http://192.168.50.203:8080/text_to_speech/{}'.format(urllib.parse.quote(url)), volume=5)  # type: ignore
    
    if indoor_co2 > 1200:
        screen.clean_screen()
        screen.set_screen_bg_color(0xff0000)
        label_co2 = M5Label('CO2 ALERT !', x=100, y=100, color=0x000000, font=FONT_MONT_18, parent=None)  # type: ignore
        utime.sleep(60)
    else:
        utime.sleep(120)

    detect_motion()

lcd.print('Ended.', 0, 80, 0xff0000)  # type: ignore
