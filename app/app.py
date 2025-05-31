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