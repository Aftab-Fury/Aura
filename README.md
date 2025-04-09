# 🌟 Aura - A Q&A Platform

**Aura** is a Django-based Q&A platform. Users can post questions, answer others, like helpful answers, and admins have full control over the platform. It's built with simplicity and community interaction in mind.

---

## ✨ Features

### 👤 General Users
- Register and log in/log out securely
- Post questions and answer others’ questions
- Like others’ answers (cannot like own answers)
- Edit or delete their own questions and answers
- View question listings with like count summaries
- Sort questions by time or number of likes
- Only logged-in users can access questions

### 🛡️ Admin Users
- Access a dedicated admin panel (hidden from normal users)
- Delete any question or answer
- Promote or demote users to/from admin
- Change passwords of any user
- View and manage all users

## 🗂 Project Structure
```aiignore

Aura/
├── Aura/                    # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── core/                    # Main app
│   ├── models.py            # Models for Question, Answer, Like
│   ├── views.py             # Views and logic
│   ├── urls.py              # App URLs
│   ├── templates/           # HTML templates
│   │   ├── home.html
│   │   ├── question_detail.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── ...
├── db.sqlite3              # SQLite database
├── manage.py
├── requirements.txt
└── README.md

```

---

## 🚀 Getting Started

To run Aura locally on your machine, follow these steps.

### Clone the repository

```bash
git clone https://github.com/Aftab-Fury/Aura.git
cd aura
```
### Set up a virtual environment
```bash
python -m venv .venv
# Activate:
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```
### Install dependencies

```bash
pip install -r requirements.txt
```

### Run migrations
```bash
python manage.py migrate
```

### Create a superuser (admin)

```bash
python manage.py createsuperuser
```

### Run the server
```bash
python manage.py runserver
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
