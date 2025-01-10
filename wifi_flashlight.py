from flask import Flask, jsonify, render_template_string, request
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
    <title>Web-Controlled Flashlight</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f9f9f9;
        }
        #slider-container {
            border: 1px solid #ccc;
            padding: 20px;
            background: #fff;
            border-radius: 8px;
            display: inline-block;
        }
        #slider-description {
            font-size: 12px;
            color: #555;
            margin-top: 10px;
        }
    </style>
    <script>
        $(document).ready(function() {
            // Update slider and state dynamically
            function updateState() {
                $.getJSON("/state", function(data) {
                    $("#led-slider").val(data.state ? 1 : 0);
                    $("#led-status").text(data.state ? "ON" : "OFF");
                });
            }

            // Change LED state when slider moves
            $("#led-slider").on("input", function() {
                var state = $(this).val() == 1 ? "on" : "off";
                $.get("/led=" + state, function() {
                    updateState();
                });
            });

            // Periodically check state
            setInterval(updateState, 1000);
        });
    </script>
</head>
<body>
    <h1>Web-Controlled Flashlight</h1>
    <p>LEDs are currently: <strong id="led-status">{{ "ON" if led_state else "OFF" }}</strong></p>
    <div id="slider-container">
        <input type="range" id="led-slider" min="0" max="1" step="1" value="{{ 1 if led_state else 0 }}">
        <div id="slider-description">Click and drag the slider to turn the flashlight on or off.</div>
    </div>
</body>
</html>
"""

# Helper function for fading LEDs
def fade_leds(action):
    steps = 50
    delay = 0.01  # Total of 0.5 seconds for full fade

    for i in range(steps + 1):
        pwm_value = i / steps if action == "on" else (steps - i) / steps

        for pin in LED_PINS:
            GPIO.output(pin, GPIO.HIGH if pwm_value > 0 else GPIO.LOW)

        time.sleep(delay)

# Flask routes
@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, led_state=led_state)

@app.route("/led=<state>", methods=["GET"])
def control_led(state):
    global led_state
    if state == "on":
        fade_leds("on")
        led_state = True
    elif state == "off":
        fade_leds("off")
        led_state = False

    return "", 204

@app.route("/state", methods=["GET"])
def get_state():
    return jsonify(state=led_state)

# Initialize LED state
led_state = False

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000)
    finally:
        GPIO.cleanup()