from flask import Flask, render_template_string, request
import RPi.GPIO as GPIO
import time

# Setup GPIO
GPIO.setmode(GPIO.BCM)
LED_PINS = [17, 27, 22]
for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

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
    <p>LEDs are currently: <strong>{{ "ON" if led_state else "OFF" }}</strong></p>
    <form method="post">
        <button type="submit" name="action" value="on">Turn ALL ON</button>
        <button type="submit" name="action" value="off">Turn ALL OFF</button>
    </form>
</body>
</html>
"""

# Helper function for fading LEDs
def fade_leds(action):
    steps = 50
    delay = 0.005  # Total of 0.25 seconds for full fade

    for i in range(steps + 1):
        pwm_value = i / steps if action == "on" else (steps - i) / steps

        # Center LED starts earlier/later
        if pwm_value >= 0.2:
            GPIO.output(27, GPIO.HIGH if action == "on" else GPIO.LOW)
        else:
            GPIO.output(27, GPIO.LOW)

        # Outer LEDs
        GPIO.output(17, GPIO.HIGH if pwm_value > 0.1 else GPIO.LOW)
        GPIO.output(22, GPIO.HIGH if pwm_value > 0.1 else GPIO.LOW)

        time.sleep(delay)

# Flask routes
@app.route("/", methods=["GET", "POST"])
def index():
    global led_state
    if request.method == "POST":
        action = request.form["action"]
        if action == "on":
            fade_leds("on")
            led_state = True
        elif action == "off":
            fade_leds("off")
            led_state = False

    return render_template_string(HTML_TEMPLATE, led_state=led_state)

# Initialize LED state
led_state = False

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000)
    finally:
        GPIO.cleanup()
