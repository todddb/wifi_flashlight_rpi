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