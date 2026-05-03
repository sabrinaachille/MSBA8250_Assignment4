# 🍩 SVNG Bakery: Smart Value, No Waste Goods

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Shiny](https://img.shields.io/badge/Shiny-Python-orange)
![OR-Tools](https://img.shields.io/badge/OR--Tools-Optimization-green)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-yellow?logo=scikitlearn)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 🔗 Demo Link

[SVNG Application](https://sachil01.shinyapps.io/msba8250_assignment4/)

---

## ▶️ App Walkthrough

> 🔹 Shows: user input → demand prediction → optimization → results dashboard

---

## 🎯 Mission

**“Smart Value, No Waste Goods”**
Our mission is to save costs, reduce waste, and generate value through analytics-driven decision making.

---

## 📌 Summary

SVNG Bakery is a student-run bakery decision support tool that optimizes daily production under budget constraints. The application leverages **predictive analytics** to forecast product demand and **optimization techniques** to determine the most profitable production strategy while minimizing waste.

By allowing users to input budget limits, location, time of day, and promotion conditions, the app provides **data-driven insights and recommendations** that maximize revenue and operational efficiency.

---

## 🧠 Project Management

We used a **Kanban workflow** to organize and track development, assign ownership, and iterate efficiently throughout milestones.

* 📝 Backlog
* 🚧 In Progress
* ✅ Completed

---

## ⚙️ Development Approach

### 1️⃣ ✏️ Planning & Design

* Lo-fi mockups
* GitHub repo
* Shiny Python app framework

### 2️⃣ 📊 Dataset

* Existing dataset + custom features
* Ensured compatibility for both prediction and optimization

### 3️⃣ 📈 Predictive Model (`demand.py`)

* Supervised learning model

#### ✅ Validation

* Train-test split
* R² - explained variance
* MSE (Mean Squared Error) - error magnitude
* MAE (Mean Absolute Error) - average prediction error

Ensures predictions are **accurate, stable, and generalizable**

### 4️⃣ 📊 Optimization Model (`optimize.py`)

* Uses predicted demand as input
* Built with OR-Tools

**Objective:**

* 💰 Maximize profit
* ♻️ Minimize waste

**Constraints:**

* Cost ≤ budget
* Production ≤ demand

### 5️⃣ 📉 Visualization

* KPI cards
* Sales and products trend
* Real-time monitoring

Focus: **actionable insights**

---

## 🤖 AI-Assisted Development

Used AI to:

* Accelerate development
* Debug issues
* Structure models

---

## 🚀 Final Outcome

A full **decision support system** combining:

* Predictive analytics
* Optimization modeling
* Dashboard visualization

---

## 💡 Key Takeaway

> Data-driven decision making transforms everday operations into optimized, value-generating systems.
