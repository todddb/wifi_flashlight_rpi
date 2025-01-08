#### You said: ####
Hi, I need to build a simple device to control an LED from a raspberry pi GPIO17 (pin 11). I need a python flask app that presents the user with a webpage and the webpage allows the user to turn the LED on or off.


#### ChatGPT said: ####
*(generated code)*
Raspberry Pi Led Control

This Python Flask app includes the backend to control the LED connected to GPIO17. You'll also need a simple HTML file (index.html) to serve as the user interface. Would you like help creating the HTML file?

#### You said: ####
Yes! Could you integrate it into a single file?

#### ChatGPT said: ####
ChatGPT
*Edited Code*
The HTML template is now integrated into the Python script using render_template_string. You can run this single file, and it will provide the webpage to control the LED. Let me know if you need further assistance!

#### I saved the file as the original `wifi_flashlight_rpi` and ran it using `python3 wifi_flashlight_rpi` ####
Here is the commandline output:

    python3 wifi_flashlight.py 
    /home/todddb/wifi_flashlight_rpi/wifi_flashlight.py:6: RuntimeWarning: This channel is already in use, continuing anyway.  Use GPIO.setwarnings(False) to disable warnings.
     GPIO.setup(17, GPIO.OUT)
     * Serving Flask app 'wifi_flashlight'
     * Debug mode: off
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     * Running on all addresses (0.0.0.0)
     * Running on http://127.0.0.1:5000
     * Running on http://192.168.11.193:5000
    Press CTRL+C to quit
    192.168.11.3 - - [08/Jan/2025 16:39:40] "GET / HTTP/1.1" 200 -
    192.168.11.3 - - [08/Jan/2025 16:39:40] "GET /favicon.ico HTTP/1.1" 404 -
    192.168.11.3 - - [08/Jan/2025 16:39:44] "POST / HTTP/1.1" 200 -
    192.168.11.3 - - [08/Jan/2025 16:39:46] "POST / HTTP/1.1" 200 -
    192.168.11.3 - - [08/Jan/2025 16:39:47] "POST / HTTP/1.1" 200 -
    192.168.11.3 - - [08/Jan/2025 16:39:48] "POST / HTTP/1.1" 200 -

and here is what the webpage looks like:

![Screenshot](./doc/screenshots/v1_screenshot.png)






