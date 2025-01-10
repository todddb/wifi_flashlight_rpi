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
