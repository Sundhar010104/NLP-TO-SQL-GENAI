# 🤖 NLP to SQL Chatbot using Gemini AI

An AI-powered web application that converts **Natural Language into SQL queries** using **Google Gemini AI**, executes the generated SQL on uploaded datasets, and displays the results instantly through an interactive Streamlit interface.

## 🌐 Live Demo

🔗 **https://nlp-to-sql-genai-rphnhgbb5qx6dja76lkftl.streamlit.app/**

---

# 📌 Project Overview

Writing SQL queries can be difficult for users who are not familiar with SQL syntax. This project solves that problem by allowing users to ask database questions in plain English.

Users simply:

- Upload a CSV or Excel dataset
- Ask questions in natural language
- Let Gemini AI generate SQL
- Execute the SQL automatically
- View results instantly

The application also includes user authentication and chat history so each user's conversations remain private.

---

# 🚀 Features

## 🔐 Authentication

- Firebase Email & Password Authentication
- Secure Session Management
- User-specific Chat History
- Logout Support

---

## 📂 Dataset Upload

Supports:

- CSV (.csv)
- Excel (.xlsx)

Uploaded datasets are automatically converted into SQLite tables.

---

## 🤖 AI-Powered SQL Generation

Powered by **Google Gemini AI**

Example Questions:

```
Show all employees from Chennai

Find employees earning more than 60000

Average salary by department

Top 5 highest paid employees

Employees with more than 5 years experience
```

---

## ✅ SQL Validation

Before execution, every SQL query is validated to block unsafe operations.

### Allowed

- SELECT
- WITH

### Blocked

- DROP
- DELETE
- UPDATE
- INSERT
- ALTER
- TRUNCATE
- CREATE
- ATTACH
- DETACH

---

## 💻 SQL Execution

Uses:

- SQLite
- SQLAlchemy
- Pandas

Query results are displayed as interactive tables.

---

## 💬 Chat History

Every successful query is stored in Firebase Firestore.

Each chat stores:

- Question
- Generated SQL
- Query Result
- Timestamp

Users can reopen previous conversations at any time.

---

# 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| Streamlit | Web Application |
| Google Gemini API | SQL Generation |
| Firebase Authentication | User Login |
| Firebase Firestore | Chat History |
| SQLite | Local Database |
| SQLAlchemy | Database Engine |
| Pandas | Data Processing |
| OpenPyXL | Excel Support |

---

# 📂 Project Structure

```text
nlp-to-sql-genai/

│
├── app.py
│
├── auth/
│   ├── firebase.py
│   ├── login.py
│   ├── signup.py
│   └── session.py
│
├── database/
│   ├── db.py
│   ├── history.py
│   └── schema.py
│
├── llm/
│   ├── gemini.py
│   └── prompts.py
│
├── sql/
│   ├── executor.py
│   └── validator.py
│
├── utils/
│   └── uploader.py
│
├── requirements.txt
│
└── README.md
```

---

# 🔄 Application Workflow

```text
                User Login
                     │
                     ▼
           Upload CSV / Excel File
                     │
                     ▼
          Store Dataset in SQLite
                     │
                     ▼
      Ask Question in Natural Language
                     │
                     ▼
          Google Gemini AI Generates SQL
                     │
                     ▼
             SQL Validation Layer
                     │
                     ▼
             Execute SQL Query
                     │
                     ▼
             Display Query Results
                     │
                     ▼
        Save Chat History to Firestore
```

---

# 📸 Screens

✔ Login

✔ Signup

✔ Dataset Upload

✔ Dataset Preview

✔ SQL Generation

✔ Query Results

✔ Chat History

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/nlp-to-sql-genai.git
```

Move into the project directory

```bash
cd nlp-to-sql-genai
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

# 🔑 Environment Variables

Create a `.env` file (or use Streamlit Secrets for deployment) and configure:

```env
GOOGLE_API_KEY=

FIREBASE_API_KEY=

FIREBASE_AUTH_DOMAIN=

FIREBASE_PROJECT_ID=

FIREBASE_STORAGE_BUCKET=

FIREBASE_MESSAGING_SENDER_ID=

FIREBASE_APP_ID=

FIREBASE_SERVICE_ACCOUNT=
```

---

# 📝 Example Usage

### Upload Dataset

Upload an Employee dataset.

### Ask

```
Show all employees from Chennai
```

### Gemini Generates

```sql
SELECT *
FROM employees
WHERE City = 'Chennai';
```

### Output

| EmployeeID | Name | Department | City |
|------------|------|------------|------|
| 101 | Rahul | IT | Chennai |
| 115 | Priya | HR | Chennai |

---

# 🔒 Security

- Firebase Authentication
- Firestore User Isolation
- SQL Validation
- Session Management
- Unsafe SQL Blocking

---

# 📈 Future Enhancements

- Google Sign-In
- Query Visualization (Charts)
- CSV & Excel Download
- SQL Explanation
- Multi-table Queries
- MySQL Support
- PostgreSQL Support
- SQL Server Support
- Dark / Light Theme
- AI Chat Memory
- Admin Dashboard

---

# 🌍 Live Application

### Streamlit Community Cloud

https://nlp-to-sql-genai-rphnhgbb5qx6dja76lkftl.streamlit.app/

---

# 👨‍💻 Author

**Sundharesan KP**

B.Tech Computer Science and Engineering

SRM Institute of Science and Technology

GitHub: https://github.com/Sundhar010104

LinkedIn: https://linkedin.com/in/sundhar010104

---

# ⭐ Support

If you found this project helpful, please consider giving it a **⭐ Star** on GitHub.

It helps others discover the project and motivates future improvements.

---

# 📄 License

This project is developed for educational and research purposes.

Feel free to use and modify it for learning.
