from flask import Flask, request, render_template_string
import joblib
import re
import time
from collections import defaultdict

app = Flask(__name__)

# Load the trained ML model and vectorizer
model = joblib.load("waf_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Track suspicious requests
request_history = defaultdict(list)
blocked_ips = {}

# Basic rule-based patterns
SQL_PATTERNS = [
    r"(\bor\b|\band\b)\s+[\w'\"=]+",
    r"union\s+select",
    r"select\s+.*\s+from",
    r"drop\s+table",
    r"insert\s+into",
    r"delete\s+from",
]

XSS_PATTERNS = [
    r"<script.*?>",
    r"javascript:",
    r"onerror\s*=",
    r"onload\s*=",
    r"<iframe",
]

COMMAND_PATTERNS = [
    r";\s*(cat|ls|whoami|pwd)",
    r"\|\s*(cat|ls|whoami|pwd)",
    r"&&\s*(cat|ls|whoami|pwd)",
]

RATE_LIMIT = 5
TIME_WINDOW = 10
BLOCK_TIME = 30


def detect_rule_based_attack(text):
    """Check input against basic attack signatures."""

    for pattern in SQL_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return "SQL Injection"

    for pattern in XSS_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return "Cross-Site Scripting (XSS)"

    for pattern in COMMAND_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return "Command Injection"

    return None


def detect_ml_attack(text):
    """Classify input using the trained ML model."""

    transformed_text = vectorizer.transform([text])
    prediction = model.predict(transformed_text)[0]

    return prediction == 1


def log_event(ip, text, reason):
    """Record blocked requests."""

    with open("waf_logs.txt", "a") as log:
        log.write(
            f"IP={ip} | Reason={reason} | Input={text} | Time={time.ctime()}\n"
        )


def check_rate_limit(ip):
    """Apply a simple rate limit."""

    current_time = time.time()

    request_history[ip] = [
        timestamp
        for timestamp in request_history[ip]
        if current_time - timestamp < TIME_WINDOW
    ]

    request_history[ip].append(current_time)

    return len(request_history[ip]) > RATE_LIMIT


@app.route("/", methods=["GET", "POST"])
def home():

    message = ""
    status = ""

    ip = request.remote_addr

    # Check whether the IP is temporarily blocked
    if ip in blocked_ips:

        if time.time() < blocked_ips[ip]:
            return render_template_string(
                PAGE,
                message="Request blocked: IP temporarily blocked.",
                status="blocked"
            )

        del blocked_ips[ip]

    if request.method == "POST":

        user_input = request.form.get("input", "")

        # Rate limiting
        if check_rate_limit(ip):

            blocked_ips[ip] = time.time() + BLOCK_TIME

            log_event(
                ip,
                user_input,
                "Rate limit exceeded"
            )

            message = "Request blocked because of excessive requests."
            status = "blocked"

            return render_template_string(
                PAGE,
                message=message,
                status=status
            )

        # Rule-based detection
        attack_type = detect_rule_based_attack(user_input)

        if attack_type:

            log_event(
                ip,
                user_input,
                attack_type
            )

            message = f"Malicious request blocked: {attack_type}"
            status = "blocked"

        # ML detection
        elif detect_ml_attack(user_input):

            log_event(
                ip,
                user_input,
                "Machine Learning Detection"
            )

            message = "Malicious request blocked by ML classifier."
            status = "blocked"

        else:

            message = "Request allowed. Input appears safe."
            status = "safe"

    return render_template_string(
        PAGE,
        message=message,
        status=status
    )


PAGE = """
<!DOCTYPE html>

<html>

<head>

<title>ML Web Application Firewall</title>

<style>

body {
    font-family: Arial;
    background: #f4f4f4;
    text-align: center;
    padding: 60px;
}

.container {
    background: white;
    padding: 30px;
    max-width: 700px;
    margin: auto;
    border-radius: 10px;
}

input {
    width: 80%;
    padding: 12px;
    margin: 15px;
}

button {
    padding: 12px 25px;
    cursor: pointer;
}

.safe {
    color: green;
}

.blocked {
    color: red;
}

</style>

</head>

<body>

<div class="container">

<h1>🛡️ ML-Based Web Application Firewall</h1>

<p>Enter text to test the WAF.</p>

<form method="POST">

<input
    type="text"
    name="input"
    placeholder="Enter text..."
    required
>

<br>

<button type="submit">
    Check Request
</button>

</form>

{% if message %}

<h3 class="{{ status }}">
    {{ message }}
</h3>

{% endif %}

</div>

</body>

</html>
"""


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
