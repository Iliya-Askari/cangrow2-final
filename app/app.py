import sys
import os
import re
import joblib
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QLabel, QMessageBox, QStackedWidget, QLineEdit,
    QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout, QSizePolicy
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
import openai

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

model_path = resource_path("model_resume.pkl")

model_bundle = joblib.load(model_path)
model = model_bundle['model']
vectorizer = model_bundle['vectorizer']
label_encoder = model_bundle['label_encoder']
stop_words = model_bundle['stop_words']
tokenizer = model_bundle['tokenizer']
df_jobs = model_bundle['df_jobs']

client = openai.OpenAI(
    base_url="https://api.llm7.io/v1",
    api_key="unused"
)

def get_top_keywords(texts, top_n=30):
    from sklearn.feature_extraction.text import TfidfVectorizer
    import numpy as np
    tfidf = TfidfVectorizer(max_features=5000)
    tfidf_matrix = tfidf.fit_transform(texts)
    scores = np.asarray(tfidf_matrix.sum(axis=0)).ravel()
    words = tfidf.get_feature_names_out()
    top_idx = scores.argsort()[::-1][:top_n]
    return [words[i] for i in top_idx]