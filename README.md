
# Resume Matcher Web App

This is the **final stage** of the project, where a trained machine learning model is deployed with a **user-friendly graphical interface and API**. This app allows users to upload resumes and receive job recommendations and personalized learning roadmaps.

---

## 🛠 Prerequisites

Make sure the following tools are installed on your system:

- **Python 3.8+** → [Python 3.8.12](https://www.python.org/downloads/release/python-3812/)
- **Git** → [Git](https://git-scm.com/downloads)

---

## 📥 Clone the Final Repository

```bash
gh repo clone Iliya-Askari/cangrow2-final
cd cangrow2-final
```

---

## 🧪 Create Virtual Environment (Recommended)

```bash
# Create a virtual environment
python -m venv venv

# Activate the environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
.
├── LICENSE
├── README.md
├── requirements.txt                 # Python dependencies
├── app/
│   ├── app.py                       # Main GUI and API logic
│   ├── Download_app_setup_exe.txt  # Instructions for packaging executable
│   ├── model_resume.pkl            # Trained ML model
│   └── README.md                   # App-specific documentation
├── DataSet/
│   ├── Job-Description-Dataset.csv
│   └── Role-Resume-Dataset.csv
├── Model/
│   └── model_resume.pkl
├── NoteBook/
│   ├── 01-Model.ipynb
│   └── Test/
│       └── test_out_put_model.py
```

---

## 🚀 Run the Application

```bash
cd app
python app.py
```

Once launched, the graphical interface will open.

---

## 🎬 Demo Video

Watch the demo video below to see how the app works:

[Watch the demo](./Preview/demo.mp4)

---

## 🖥 How to Use the Software

On the home screen, you will be asked to choose **one of four input formats**:

1. **Upload a Word document (.docx)**
2. **Upload a PDF file**
3. **Upload a plain text file (.txt)**
4. **Use the chat interface** to enter your resume manually

After providing your input, click on the **"Analyze Resume"** button. The system will process your resume and then display:

- The **predicted job title**
- A personalized **skill roadmap** to help you become job-ready

---

## ℹ️ App Documentation

For more information about how the app works, setup details, and customization, refer to:

```
app/README.md
```

This is the main reference for understanding the application's behavior and usage.

---

## 🧪 Try It Yourself with Sample Files

We’ve provided several sample resumes in different formats so you can quickly test how the application works.

📁 **Available Sample Files:**
- 📄 [sample_resume.pdf](./Samples/sample_resume.pdf)
- 📄 [sample_resume.docx](./Samples/sample_resume.docx)
- 📄 [sample_resume.txt](./Samples/sample_resume.txt)

👉 To try them out:
1. Clone the project and run the app.
2. On the homepage, choose your preferred input method (PDF, Word, Text, or Chat).
3. Upload one of the sample files above.
4. Click **"Analyze Resume"** and wait for the job suggestion and skill roadmap to appear.

> 📝 You can also try the **Chat Mode** by entering plain text instead of uploading a file.

---

## 📦 Build an Executable (Optional)

If you wish to build a standalone desktop executable for distribution, refer to the instructions in:

```
app/Download_app_setup_exe.txt
```

You can use tools like `pyinstaller` to convert the app into an `.exe` file.

---

## 📄 License

This project is released under the terms described in the `LICENSE` file.
