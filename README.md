# 🛡️ ML-Based Web Application Firewall (WAF)

A learning project that demonstrates a Web Application Firewall (WAF) using Python, Flask, and Machine Learning to detect and block common web-based attacks.

## 📌 Project Overview

This project demonstrates how a basic Web Application Firewall can inspect incoming web requests and identify potentially malicious input.

The WAF combines **rule-based detection** with a **machine-learning-based classifier** to identify suspicious requests.

## 🚀 Features

* SQL Injection detection
* Cross-Site Scripting (XSS) detection
* Command Injection detection
* Machine-learning-based input classification
* Rate limiting
* Progressive IP blocking
* Logging of malicious requests

## 🧠 How It Works

The application processes user input through multiple security checks:

1. Incoming input is received by the Flask application.
2. Rule-based patterns are used to identify known malicious inputs.
3. Suspicious input is passed to a machine-learning classifier.
4. Malicious requests are blocked.
5. Blocked activity is recorded in the WAF logs.
6. Repeated suspicious requests can trigger temporary IP blocking or rate limiting.
7. Safe requests are allowed to continue.

## 🛠️ Technologies Used

* Python
* Flask
* Scikit-learn
* Joblib
* HTML/CSS
* Machine Learning

## 📂 Project Structure

```text
ML-based-Web-Application-Firewall/
│
├── app.py
├── train_model.py
├── waf_model.pkl
├── vectorizer.pkl
├── waf_logs.txt
├── screenshots/
│   ├── waf-home.png
│   ├── safe-input.png
│   ├── attack-blocked.png
│   └── rate-limiting.png
│
└── README.md
```

## ▶️ Setup and Usage

### 1. Clone the repository

```bash
git clone https://github.com/Cyber-rookie-007/ML-based-Web-Application-Firewall.git
cd ML-based-Web-Application-Firewall
```

### 2. Install the required dependencies

```bash
pip install flask scikit-learn joblib
```

### 3. Train the machine-learning model

```bash
python train_model.py
```

### 4. Start the Flask application

```bash
python app.py
```

### 5. Open the application

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

## 🧪 Security Testing

The project can be tested in a local environment using representative malicious and benign inputs.

Examples include:

* SQL Injection patterns
* XSS payloads
* Command Injection patterns
* Normal/safe input

The results of the tests will be documented with screenshots after the application is successfully configured and run.

## 📊 Logging

Malicious requests detected by the WAF are recorded in the application log.

```text
waf_logs.txt
```

The log can be used to review detected activity and understand how the WAF responds to suspicious requests.

## 🎯 Learning Objectives

This project is intended to provide practical exposure to:

* Web application security
* WAF concepts
* Rule-based attack detection
* Machine-learning-based classification
* Flask web applications
* Request filtering
* Rate limiting
* Security logging

## ⚠️ Disclaimer

This project is intended for educational and cybersecurity learning purposes. Security testing should be performed only against applications and systems that you own or are explicitly authorized to test.

## 🔮 Future Improvements

Possible improvements include:

* Real-time security monitoring dashboard
* SIEM integration
* Docker deployment
* Reverse-proxy integration
* Cloud deployment
* Improved machine-learning dataset
* Advanced anomaly detection

## 👤 Author

Cyber-rookie-007
