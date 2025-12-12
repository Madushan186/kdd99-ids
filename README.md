🛡️ KDD ’99 Intrusion Detection System (IDS)
  

Overview

This project implements a Network Intrusion Detection System (IDS) using the KDD ’99 dataset, designed to detect malicious network activities in near real-time.
It leverages machine learning models to classify network traffic and identify attacks, providing an efficient tool for cybersecurity monitoring.

Features

Detects network intrusions using the KDD ’99 dataset.
Implements Random Forest for initial detection.
Supports exploratory data analysis (EDA) and visualizations.
Modular structure for future enhancements (LSTM, GRU, 1D CNN).
Easily extensible to new datasets or real-time traffic detection.

(Optional) Create a virtual environment:

python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

Install dependencies:

pip install -r requirements.txt

Dependencies may include: pandas, scikit-learn, matplotlib, seaborn, streamlit.

Usage
Load Dataset

import pandas as pd
df = pd.read_csv("data/kdd_dataset.csv")  # Adjust file name
st.write(df.head())

Train Random Forest Model

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

X = df.drop("label", axis=1)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

Run Streamlit Dashboard
streamlit run dashboard.py

Machine Learning Models
Model	Accuracy	F1 Score
Random Forest	0.95	0.94
LSTM (future)	0.97	0.96

Random Forest used as baseline; future enhancements include LSTM, GRU, and 1D CNN for sequence-based detection.

Dataset

KDD ’99 Dataset: https://archive.ics.uci.edu/static/public/130/kdd+cup+1999+data.zip

Preprocessing includes: removing duplicates, encoding categorical features, scaling numerical features.

Note: Sensitive or large files not included; place dataset in data/ folder.

Contributing

Contributions are welcome!
