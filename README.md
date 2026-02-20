# 🩺 Diabetes Risk Analysis & Comorbidity Network Dashboard

A professional, academic-grade health analytics dashboard that explores diabetes risk factors, patient segmentation, and clinical association rules. Built with a **Flask** backend and a custom **Stitch-inspired** responsive UI.

## 🚀 Key Features

- **Risk Prediction Tool**: Real-time risk assessment using a Random Forest model with an interactive clinical input panel and animated risk gauge.
- **Cluster Analysis**: K-means segmentation of the BRFSS dataset to identify high-risk vs. low-risk patient profiles.
- **Association Rules**: Discovery of co-occurring health conditions using Jaccard similarity matrices and support/confidence/lift metrics.
- **Feature Importance**: In-depth analysis of the strongest biometric predictors (BMI, High BP, GenHlth) for diabetes.
- **Responsive Design**: Modern, mobile-first UI with a desktop sidebar and mobile bottom navigation bar.

## 📁 Project Structure

```text
├── flask_app.py          # Main Flask entry point & API endpoints
├── data/processed/       # Cleaned clinical datasets (CSVs)
├── models/               # Trained Random Forest model & Scaler
├── templates/            # Jinja2 HTML pages (Search/Predict/Analyze)
├── static/               # Custom CSS (Stitch UI) & AJAX JavaScript
├── notebooks/            # Jupyter notebooks for data science research
└── requirements.txt      # Project dependencies
```

## 🛠️ Installation & Setup

### 1. Clone & Setup Environment

```bash
git clone <repository-url>
cd comorbidity-network-analysis
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python flask_app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

## 🧪 Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: TailwindCSS, Jinja2, Plotly.js, Google Fonts (Inter)
- **Data Science**: Pandas, NumPy, Scikit-Learn
- **Research**: Jupyter Notebooks

## 📘 Academic Context

This project was developed for the **Data Science Course**. It utilizes the **Behavioral Risk Factor Surveillance System (BRFSS)** dataset to demonstrate the application of Predictive Modeling, Unsupervised Clustering, and Association Rule Mining in public health.
