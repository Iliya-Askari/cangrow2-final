# Resume Analyzer & Learning Roadmap Generator

## Overview

This project is a desktop application built with **PyQt5** that allows users to analyze resumes and generate detailed personalized learning roadmaps based on the missing skills inferred from the resume content. The application leverages a pre-trained machine learning model to predict the most suitable job title for the given resume text, extracts keywords to identify missing skills, and then connects to an OpenAI GPT API to create a comprehensive learning roadmap in English.

---

## Features

- Load resume text from multiple input formats: PDF, DOCX, and plain text files.
- Input resume text manually or via a chat interface.
- Predict the job title that fits the resume content using a machine learning model.
- Identify missing skills by comparing resume keywords to job descriptions.
- Generate a detailed, standards-compliant learning roadmap for missing skills via OpenAI GPT API.
- User-friendly GUI with separate pages for input selection and result analysis.
- Clear, reset, and navigation buttons for smooth user interaction.

---

## Project Structure & Main Components

### 1. `resource_path(relative_path)` function

- Handles file path resolution, especially when packaged into a standalone executable.
- Returns the absolute path to resources like the pre-trained model file.

### 2. Model loading

- Loads a serialized model bundle (`model_resume.pkl`) using `joblib`.
- The bundle contains:
  - `model`: The trained machine learning classification model.
  - `vectorizer`: TF-IDF vectorizer to convert text into features.
  - `label_encoder`: To convert numeric prediction back to job titles.
  - `stop_words`: List of stop words for text cleaning.
  - `tokenizer`: Tokenizer instance for splitting text.
  - `df_jobs`: DataFrame containing job descriptions for skill extraction.

### 3. OpenAI GPT Client Initialization

- Configured to connect to an API endpoint (`https://api.llm7.io/v1`) with a placeholder API key.
- Used for generating the learning roadmap text.

---

## Core Functions

### `get_top_keywords(texts, top_n=30)`

- Extracts top `n` keywords from a list of texts using TF-IDF.
- Useful for identifying important skills or concepts in job descriptions.

### `predict_job_and_missing_skills(resume_text)`

- Cleans and tokenizes the resume text.
- Converts it into TF-IDF features.
- Predicts the most suitable job title using the loaded model.
- Compares the resume tokens with top keywords from matching job descriptions.
- Returns predicted job title and a list of missing skills (top 20).

### `generate_roadmap_text(missing_skills)`

- Sends a detailed prompt with the missing skills list to OpenAI GPT API.
- Requests a thorough, detailed learning roadmap in English.
- Cleans the API response to remove formatting characters.
- Returns the roadmap text.

### `extract_text_from_pdf(file_path)`

- Uses `pdfplumber` to extract text from all pages of a PDF file.

### `extract_text_from_docx(file_path)`

- Uses `python-docx` to extract text from paragraphs in a DOCX file.

---

## PyQt5 GUI Classes

### `MainPage(QWidget)`

- The initial screen where the user chooses input method:
  - Load PDF, DOCX, Text file, or Chat input.
- Implements file dialog for loading files.
- Upon file selection or chat button press, switches to `AnalysisPage` with the loaded or empty text.

### `AnalysisPage(QWidget)`

- Shows a text area pre-filled with loaded resume text or empty for chat.
- Buttons:
  - **Analyze Resume**: Runs prediction and roadmap generation.
  - **Clear Text**: Clears input and output fields.
  - **Back to Main Menu**: Returns to `MainPage`.
- Displays predicted job title and detailed learning roadmap text.

### `MainWindow(QWidget)`

- Manages the main window and page navigation using `QStackedWidget`.
- Switches between `MainPage` and `AnalysisPage`.

---

## How It Works (Workflow)

1. **Start Application**  
   The user is presented with the main page to choose input method.

2. **Load Resume / Chat**  
   User loads a resume file or chooses to input text via chat.

3. **Analyze Resume**  
   The text is cleaned and vectorized, the model predicts the best matching job title.

4. **Missing Skills Extraction**  
   Compares resume keywords with job description keywords to find missing skills.

5. **Roadmap Generation**  
   Sends missing skills to GPT API with a prompt to generate a comprehensive learning roadmap.

6. **Display Results**  
   Shows the predicted job and the roadmap in the GUI.

7. **User Actions**  
   User can clear the text or go back to the main menu to start over.

8. **OutPut Exe**
   Command to get exe output for app.py (```  pyinstaller --onefile --add-data "model_resume.pkl;." --hidden-import nltk app.py ```)