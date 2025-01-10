#### You said: ####
Hi, I need to build a simple device to control an LED from a raspberry pi GPIO17 (pin 11). I need a python flask app that presents the user with a webpage and the webpage allows the user to turn the LED on or off.


#### ChatGPT said: ####

    from flask import Flask, render_template_string, request
    import RPi.GPIO as GPIO

    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.output(17, GPIO.LOW)

    # Create Flask app
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            action = request.form.get("action")
            if action == "on":
                GPIO.output(17, GPIO.HIGH)
            elif action == "off":
                GPIO.output(17, GPIO.LOW)

        # Read current LED state
        led_state = GPIO.input(17)
        return render_template_string(HTML_TEMPLATE, led_state=led_state)

    # Run the app
    if __name__ == "__main__":
        try:
            app.run(host="0.0.0.0", port=5000)
        except KeyboardInterrupt:
            GPIO.cleanup()
            print("\nGPIO cleanup and app stopped.")

**`Raspberry Pi Led Control`**

This Python Flask app includes the backend to control the LED connected to GPIO17. You'll also need a simple HTML file (index.html) to serve as the user interface. Would you like help creating the HTML file?

#### You said: ####
Yes! Could you integrate it into a single file?

#### ChatGPT said: ####

    from flask import Flask, render_template_string, request
    import RPi.GPIO as GPIO

    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.output(17, GPIO.LOW)

    # Create Flask app
    app = Flask(__name__)

    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>LED Control</title>
    </head>
    <body>
        <h1>Control the LED</h1>
        <p>LED is currently: <strong>{{ "ON" if led_state else "OFF" }}</strong></p>
        <form method="post">
            <button type="submit" name="action" value="on">Turn ON</button>
            <button type="submit" name="action" value="off">Turn OFF</button>
        </form>
    </body>
    </html>
    """

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            action = request.form.get("action")
            if action == "on":
                GPIO.output(17, GPIO.HIGH)
            elif action == "off":
                GPIO.output(17, GPIO.LOW)

        # Read current LED state
        led_state = GPIO.input(17)
        return render_template_string(HTML_TEMPLATE, led_state=led_state)

    # Run the app
    if __name__ == "__main__":
        try:
            app.run(host="0.0.0.0", port=5000)
        except KeyboardInterrupt:
            GPIO.cleanup()
            print("\nGPIO cleanup and app stopped.")

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

So, I went back to ChatGPT to add the other two LEDs.

#### You said: ####
That works great! Can you do me a favor? I'd like to have more than one LED. Can you add two more? One connected to GPIO27 and the other to GPIO22? They should all be controlled together with the same webpage.

#### ChatGPT said: ####
ChatGPT

    from flask import Flask, render_template_string, request
    import RPi.GPIO as GPIO

    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    GPIO.output(17, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)

    # Create Flask app
    app = Flask(__name__)

    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>LED Control</title>
    </head>
    <body>
        <h1>Control the LEDs</h1>
        <p>LED on GPIO17 is currently: <strong>{{ "ON" if led_states[17] else "OFF" }}</strong></p>
        <p>LED on GPIO27 is currently: <strong>{{ "ON" if led_states[27] else "OFF" }}</strong></p>
        <p>LED on GPIO22 is currently: <strong>{{ "ON" if led_states[22] else "OFF" }}</strong></p>
        <form method="post">
            <button type="submit" name="action" value="on">Turn ALL ON</button>
            <button type="submit" name="action" value="off">Turn ALL OFF</button>
        </form>
    </body>
    </html>
    """

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            action = request.form.get("action")
            if action == "on":
                GPIO.output(17, GPIO.HIGH)
                GPIO.output(27, GPIO.HIGH)
                GPIO.output(22, GPIO.HIGH)
            elif action == "off":
                GPIO.output(17, GPIO.LOW)
                GPIO.output(27, GPIO.LOW)
                GPIO.output(22, GPIO.LOW)

        # Read current LED states
        led_states = {
            17: GPIO.input(17),
            27: GPIO.input(27),
            22: GPIO.input(22)
        }
        return render_template_string(HTML_TEMPLATE, led_states=led_states)

    # Run the app
    if __name__ == "__main__":
        try:
            app.run(host="0.0.0.0", port=5000)
        except KeyboardInterrupt:
            GPIO.cleanup()
            print("\nGPIO cleanup and app stopped.")


I've added support for two additional LEDs connected to GPIO27 and GPIO22. The webpage now displays the states of all three LEDs and provides buttons to turn them all on or off simultaneously. Let me know if you need further modifications!

#### I saved the update on top of the original (`wifi_flashlight_rpi`) ####

When I ran it, the new interface looks like this:

![Screenshot](./doc/screenshots/v2_screenshot.png)

I don't like how it shows all 3 LEDs seperately, I would like them to funnction as a single light, even if I have them turn on and off a little staggered to provide a nice fade.

