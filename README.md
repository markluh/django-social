# Django Social

Django Social is a social networking platform built with **Django** where users can:

- Create an account (authentication & registration)
- Update their profile picture and status
- Create and join communities
- Follow other users
- Create posts, like posts, and comment on posts
- Reply to comments
- Chat with other users
- Go live (real-time streaming support planned)

This project is a foundation for a modern social media app.

---

## 🚀 Getting Started

Follow these steps to run the project locally.

### 1. Clone the Repository
```bash
git clone https://github.com/markluh/django-social.git
cd django-social/backend
2. Create & Activate Virtual Environment
python -m venv .venv
source .venv/bin/activate   # On Linux/Mac
.venv\Scripts\activate  #on windows
3. Install Dependencies
pip install -r requirements.txt

4. Set Up Database

Apply migrations to create the required database schema:

python manage.py migrate

5. Create a Superuser (Admin)
python manage.py createsuperuser


Follow the prompts to set up your admin account.

6. Run the Development Server
python manage.py runserver


Now open the app in your browser:
👉 http://127.0.0.1:8000

📦 Project Structure
django-social/
│
├── backend/              # Django project folder
│   ├── manage.py
│   ├── backend/          # Project settings
│   ├── accounts/         # Authentication & user profiles
│   ├── posts/            # Posts, likes, comments
│   ├── chat/             # Chat & messaging
│   ├── live/             # Live streaming features
│   └── ...
│
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation

⚙️ Tech Stack

Backend: Django, Django REST Framework

Database: SQLite (default) / MySQL / PostgreSQL

Realtime: Django Channels (for chat & live)
