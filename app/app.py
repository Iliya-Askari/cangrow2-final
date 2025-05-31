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