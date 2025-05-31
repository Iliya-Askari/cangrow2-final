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

def predict_job_and_missing_skills(resume_text):
    cleaned = resume_text.lower()
    cleaned = re.sub(r'[^a-zA-Z\s]', ' ', cleaned)
    tokens = tokenizer.tokenize(cleaned)
    tokens = [word for word in tokens if word not in stop_words]
    cleaned_text = ' '.join(tokens)

    vect = vectorizer.transform([cleaned_text])
    pred_label = model.predict(vect)[0]
    job_title = label_encoder.inverse_transform([pred_label])[0]

    job_descs = df_jobs[df_jobs['Job Title'].str.lower().str.contains(job_title.lower())]
    if job_descs.empty:
        return job_title, []

    top_keywords = get_top_keywords(job_descs['clean_description'], top_n=50)
    resume_words = set(tokens)
    missing_skills = [word for word in top_keywords if word not in resume_words]
    return job_title, missing_skills[:20]

def generate_roadmap_text(missing_skills):
    prompt = (
        "سلام من یکسری کلمات کلیدی هست و احتمال مدل من کلمات غیر ضروری هم اورده "
        "که از کسی هست رزومه‌اش این موارد رو کم داره\n\n" + str(missing_skills) + "'\n\n"
        "و من ازت می‌خوام یه نقشه راه به کاربر بدی که باید چی‌ها یاد بگیره و چه کارهایی باید انجام بده و اگر دیدی کلمه‌ای اضافه و بی‌مورد هست در نظر نگیر. "
        "و باید با دقت بالا نقشه راه بدی. اگر هر زبان یا کتابخونه‌ای از اون زبان رو باید یاد بگیره بگو. در ضمن باید طبق استاندارد نقشه راه بدی و حتما انگلیسی باشه. "
        " من بهت گقتم با دقت باشه این دقت حتما باید بر اساس اون کلمات مشخص باشه "
        "و چون این پرامپت من با API وصل می‌کنم توضیحات اول و آخر رو نیاز ندارم و بهم توضیح نده، فقط نقشه راه به زبان انگلیسی بفرست. "
        "منظورم اینه که توضیح ندی اینه که مثل این دستوراتی هستی که پاسخ به من می‌دی. من یک نرم‌افزار دارم و با API به تو وصل شدم و می‌خوام به محض اینکه پرامپت فرستادم "
        "نقشه راه باشه و در اول و آخر هیچی نباشه و باید بدون فرمت خاصی باشه. باید فرمت txt باشه."
        "در ضمن نمیخوام نقشه راه کوتتاه و مختصر باشه میخوام با بالاترین دقت و بهترین جزئیات نسب به اون کلمات باشه و هرچی بیشتر و کامل تر بهتر "
        "خب در خط اخر فقط این جمله رو بنویس  به صورت اگلیسی این مسیر مسیر کلی و استاندارد میباشد و طبق مهارت های که باید یاد بگیرید باشه "
    )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.choices[0].message.content
    for char in ['`', '*', '-']:
        text = text.replace(char, '')
    
    return text

def extract_text_from_pdf(file_path):
    import pdfplumber
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file_path):
    import docx
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

class MainPage(QWidget):
    def __init__(self, switch_to_analysis):
        super().__init__()
        self.switch_to_analysis = switch_to_analysis

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(60, 60, 60, 60)
        main_layout.setSpacing(40)

        self.label = QLabel("Choose Input Method")
        self.label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #333;")
        main_layout.addWidget(self.label)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(30)
        grid_layout.setContentsMargins(20, 20, 20, 20)

        button_style = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """

        buttons = [
            ("Load PDF", 'pdf'),
            ("Load DOCX", 'docx'),
            ("Load Text", 'txt'),
            ("Chat", 'chat')
        ]

        for idx, (label, btn_type) in enumerate(buttons):
            row = idx // 2
            col = idx % 2

            btn = QPushButton(label)
            btn.setFixedSize(QSize(150, 150))
            btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
            btn.setStyleSheet(button_style)
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

            if btn_type == 'chat':
                btn.clicked.connect(self.open_chat)
            else:
                btn.clicked.connect(lambda _, t=btn_type: self.open_file_dialog(t))

            grid_layout.addWidget(btn, row, col, alignment=Qt.AlignCenter)

        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

    def open_file_dialog(self, file_type):
        if file_type == 'pdf':
            filter_str = "PDF Files (*.pdf)"
        elif file_type == 'docx':
            filter_str = "Word Files (*.docx)"
        else:
            filter_str = "Text Files (*.txt)"

        file_path, _ = QFileDialog.getOpenFileName(self, f"Select {file_type.upper()} File", "", filter_str)
        if file_path:
            # استخراج متن بر اساس نوع فایل
            if file_type == 'pdf':
                text = extract_text_from_pdf(file_path)
            elif file_type == 'docx':
                text = extract_text_from_docx(file_path)
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            self.switch_to_analysis(text)

    def open_chat(self):
        self.switch_to_analysis("") 
        
class AnalysisPage(QWidget):
    def __init__(self, switch_to_main):
        super().__init__()
        self.switch_to_main = switch_to_main

        layout = QVBoxLayout()

        self.label = QLabel("Input Text / Chat:")
        layout.addWidget(self.label)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        btn_layout = QHBoxLayout()
        self.analyze_btn = QPushButton("Analyze Resume")
        self.analyze_btn.clicked.connect(self.analyze_text)
        btn_layout.addWidget(self.analyze_btn)

        self.clear_btn = QPushButton("Clear Text")
        self.clear_btn.clicked.connect(self.clear_text)
        btn_layout.addWidget(self.clear_btn)

        self.back_btn = QPushButton("Back to Main Menu")
        self.back_btn.clicked.connect(self.back_to_main)
        btn_layout.addWidget(self.back_btn)

        layout.addLayout(btn_layout)

        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

        self.roadmap_text_edit = QTextEdit()
        self.roadmap_text_edit.setReadOnly(True)
        layout.addWidget(self.roadmap_text_edit)

        self.setLayout(layout)

    def set_text(self, text):
        self.text_edit.setText(text)

    def clear_text(self):
        self.text_edit.clear()
        self.result_label.setText("")
        self.roadmap_text_edit.clear()

    def back_to_main(self):
        self.clear_text()
        self.switch_to_main()

    def analyze_text(self):
        resume = self.text_edit.toPlainText().strip()
        if not resume:
            QMessageBox.warning(self, "Warning", "Please enter or load some text first.")
            return
        if len(resume.split()) < 100:
            QMessageBox.warning(self, "Warning", "Resume text must be at least 100 words.")
            return

        predicted_job, suggested_skills = predict_job_and_missing_skills(resume)
        self.result_label.setText(f"Suggested job : <b>{predicted_job}</b>")

        roadmap = generate_roadmap_text(suggested_skills)
        self.roadmap_text_edit.setPlainText(roadmap)
        
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resume Analyzer & Chat")
        self.setGeometry(200, 200, 800, 700)

        self.stack = QStackedWidget()
        main_page = MainPage(self.show_analysis_page)
        self.analysis_page = AnalysisPage(self.show_main_page)

        self.stack.addWidget(main_page)
        self.stack.addWidget(self.analysis_page)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)

    def show_analysis_page(self, text):
        self.analysis_page.set_text(text)
        self.stack.setCurrentWidget(self.analysis_page)

    def show_main_page(self):
        self.stack.setCurrentIndex(0)