# FollowUp Buddy

**FollowUp Buddy** is a Django-based web app designed to help users (especially Christians) track their evangelism efforts and schedule meaningful follow-ups. It uses Django’s template engine and works with the default SQLite database. No REST framework or API is used—just simple, clean web forms and views.

---

## ✨ Features

- Log evangelism encounters and faith levels
- Add and manage follow-ups per person
- Automatically prioritizes follow-ups by faith status
- Admin dashboard with a modern UI using Jazzmin
- Uses SQLite by default (no extra setup needed)
- Built-in superuser seeding for quick setup
- Debug toolbar for development diagnostics

---

## 🛠 Requirements

- Python 3.10+
- Internet connection (required for full UI functionality)
- All Python dependencies listed in `requirements.txt`

---

## 📦 Tech Stack

- **Backend:** Django 5.2.1 (with Templates)
- **Database:** SQLite (default)
- **UI:** HTML, CSS, Bootstrap, Jazzmin Admin
- **Extra:** `django-debug-toolbar`, `django-widget-tweaks`, `faker` for seeding

---

## 🚀 Getting Started

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/followup-buddy.git
cd followup-buddy
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. (Optional) Create a Superuser

```bash
python manage.py createsuperuser
```

Alternatively, skip this step and run the next command to seed a default superuser automatically.

### 6. Seed the Database

To populate the database with demo evangelism data and a default superuser (`evangelist / password123`):

```bash
python seed.py
```

> ⚠️ This step is important if you want to explore the app quickly without manually entering records.

### 7. Run the Development Server

```bash
python manage.py runserver
```

Open your browser and visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 💡 Important Notes

- ✅ **Internet connection required**: Some UI assets (like from Jazzmin) require internet access to render properly.
- ✅ **Seed your database** using `python seed.py` for default data and easier exploration.
- ✅ **Create or log in as admin** to access the dashboard and test core features.
- ❌ No external DB setup is needed (uses `db.sqlite3` by default).

---

## 🧪 Development Tools

- [django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar)
- [django-widget-tweaks](https://github.com/jazzband/django-widget-tweaks)
- [Jazzmin Admin Theme](https://github.com/farridav/django-jazzmin)
- [Faker](https://faker.readthedocs.io/) – for generating sample data

---

## 🙌 Contribution

Pull requests are welcome. Please open an issue to discuss major changes before submitting.

---

## 📄 License

MIT License

---

## ✝️ Inspiration

> “Go therefore and make disciples of all nations…”  
> — Matthew 28:19

FollowUp Buddy is built to help you not only obey the Great Commission, but steward every soul with love, intention, and diligence.

