App Name - Prepstr

Prepstr – Mock Test Platform

Features

User Module

User Signup

Full Name

Username (unique)

Email

Password (hashed)


User Login

Forgot Password (optional)

Dashboard

Available Mock Tests

Start Test

Timer

One question per page

Previous/Next buttons

Flag Question

Submit Test

Result

Score

Accuracy

Rank (optional)

Detailed Explanation

Performance Analysis

Previous Attempts



---

Admin Module

Admin credentials (stored as hashed values, never plain text)

Username: PradipT0928
Password: PradipT@0928

Features

Admin Login

Create Mock Test

Edit Mock Test

Delete Mock Test

Upload Questions

Import Questions from Excel/CSV

Export Tests

View Users

View Results

Analytics Dashboard

Activate/Deactivate Tests



---

Mock Test Features

Single Correct MCQ

Negative Marking

Configurable Time

Random Questions

Random Options

Auto Submit on Timeout

Bookmark Questions

Question Palette

Review Before Submit

Instant Result

Explanation After Submission



---

Suggested Project Structure

Prepstr/

│
├── app.py
├── requirements.txt
├── database.py
├── auth.py
├── utils.py
│
├── pages/
│   ├── Login.py
│   ├── Signup.py
│   ├── Dashboard.py
│   ├── Mock_Test.py
│   ├── Result.py
│   └── Admin.py
│
├── data/
│   ├── users.db
│   ├── tests.db
│   └── results.db
│
├── assets/
│   ├── logo.png
│   └── css.css
│
└── questions/
    ├── test1.csv
    └── test2.csv


---

Database Tables

Users

id
name
username
email
password_hash
created_at

Tests

test_id
title
subject
time
negative_marking
total_questions

Questions

id
test_id
question
option1
option2
option3
option4
correct_option
explanation

Results

id
user
test
score
correct
wrong
accuracy
time_taken
date


---

Security

Passwords hashed using bcrypt

Secure admin authentication (store only hashed credentials)

Session management

SQL injection protection

Input validation



---

Streamlit Libraries

streamlit
streamlit-authenticator
sqlite3
bcrypt
pandas
plotly
openpyxl


---

Admin Dashboard

📊 Total Users

📝 Total Tests

❓ Total Questions

📈 Attempts

🏆 Top Performers

📋 Recent Results



---

User Dashboard

Welcome message

Available Tests

Completed Tests

Highest Score

Overall Accuracy

Progress Chart

Recent Attempts



---

Future Features

Dark Mode

Testbook-style UI

Leaderboard

Certificates

Mobile Responsive Design

AI Question Generator

PDF Question Import

Image-based Questions

Multi-language Support (English/Marathi)

Email Verification

OTP Login

Subscription Plans

Payment Gateway

Cloud Deployment


This architecture will produce a professional Prepstr mock test platform with secure user authentication, an encrypted admin login, a complete test management system, detailed analytics, and a Testbook-like testing experience.
