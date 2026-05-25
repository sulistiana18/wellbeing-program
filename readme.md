# 💙 Employee Wellbeing Dashboard

An interactive dashboard to monitor employee activity, health metrics, and overall wellbeing using data analytics.

---

## 🚀 Overview

This project visualizes employee wellbeing data by combining:
- Activity tracking (distance, heart rate, time)
- Health records (BMI, medical check-up)
- User profile data

The dashboard provides insights into employee performance, activity patterns, and health indicators.

---

## 📊 Features

### 📈 Activity Monitoring
- Distance over time
- Activity type distribution
- Heart rate vs distance

### 🧠 Automated Insights
- Most active user
- Most common activity
- Average heart rate & BMI

### 🏆 Leaderboard
- Ranking users based on total activity time
- Top 3 highlighted with medals 🥇🥈🥉

### 📋 Data Exploration
- Interactive filters (User & Activity Type)
- Full dataset preview

---

## 🗂️ Dataset Structure

### 1. Users

| Column | Description |
|--------|------------|
| user_id | Unique user ID |
| fullname | Employee name |
| gender | Gender |
| age | Age |
| department | Department |

---

### 2. Activity Logs

| Column | Description |
|--------|------------|
| activity_id | Activity ID |
| user_id | User reference |
| distance | Distance (km) |
| average_heartrate | Avg heart rate |
| moving_time | Duration |
| type | Activity type |
| start_date_local | Activity date |

---

### 3. MCU Records

| Column | Description |
|--------|------------|
| mcu_id | Record ID |
| user_id | User reference |
| BMI | Body Mass Index |
| BMICat | BMI Category |

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas
- Plotly

---

## ⚙️ Installation (Local)

### 1. Clone this repository:


--

### 2. Run App

python -m streamlit run app.py