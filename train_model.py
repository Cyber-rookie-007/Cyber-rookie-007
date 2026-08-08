from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

# Training data
texts = [
    "hello world",
    "welcome to my website",
    "how are you",
    "this is a normal message",
    "please submit the form",
    "good morning",
    "thank you for visiting",
    
    "' OR '1'='1",
    "' OR 1=1 --",
    "UNION SELECT username,password FROM users",
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert(1)>",
    "; cat /etc/passwd",
    "| whoami",
    "&& ls -la"
]

# Labels: 0 = safe, 1 = malicious
labels = [
    0, 0, 0, 0, 0, 0, 0,
    1, 1, 1, 1, 1, 1, 1, 1
]

# Convert text into numerical features
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

# Train the classifier
model = MultinomialNB()
model.fit(X, labels)

# Save the trained model and vectorizer
joblib.dump(model, "waf_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model training completed successfully.")
print("Saved: waf_model.pkl")
print("Saved: vectorizer.pkl")
