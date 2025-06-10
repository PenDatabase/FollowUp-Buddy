Sure! Below is a complete `README.md` file for your **FollowUp Buddy** Django app, which uses Django templates (not DRF) and runs on the default `db.sqlite3` database:

---

````markdown
# FollowUp Buddy

**FollowUp Buddy** is a Django-based web application designed to help users (especially Christians) track their evangelism efforts and follow-ups. It uses Django’s built-in templating system (not DRF) to provide a simple, intuitive interface for managing evangelism records and scheduling follow-ups.

## ✨ Features

- Track evangelism sessions and follow-up status
- Template-based views (not API-based)
- Simple SQLite database setup (default)
- Admin dashboard using [Jazzmin](https://github.com/farridav/django-jazzmin)
- Debugging via Django Debug Toolbar
- Enhanced form customization with `django-widget-tweaks`

## 🛠 Requirements

- Python 3.10+
- Django 5.2.1
- All dependencies listed in `requirements.txt`

## 📦 Tech Stack

- **Backend:** Django (Class-based Views or Function-based Views)
- **Frontend:** Django Templates + HTML/CSS
- **Database:** SQLite (default)
- **UI/UX:** Jazzmin Admin Theme

## 📁 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/followup-buddy.git
cd followup-buddy
````

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser to use the application.

## 🧪 Development Tools

* `django-debug-toolbar` – for inspecting queries, templates, and more.
* `django-widget-tweaks` – for customizing form widgets in templates.
* `django-jazzmin` – replaces the default Django admin UI with a modern, responsive theme.


## 💡 Notes

* The project uses the built-in Django SQLite database; no extra setup is required.
* Designed for small teams or individual users keeping track of personal evangelism efforts.

## 🙌 Contribution

Feel free to open an issue or submit a pull request with improvements or bug fixes.

## 📄 License

This project is licensed under the MIT License.

## ✝️ Why FollowUp Buddy?

Inspired by Matthew 28:19 — "Go therefore and make disciples of all nations..." — this app helps believers not just evangelize, but stay accountable by following up with the souls God entrusts to them.

```

---

Let me know if you want this README to include screenshots, sample user flows, or a breakdown of follow-up logic.
```
