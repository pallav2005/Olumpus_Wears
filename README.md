# 👕 Olympus Wears

Olympus Wears is a Django-based clothing web application that showcases a collection of stylish outfits through a structured and scalable backend. The project simulates a basic e-commerce platform with product display functionality using Django templates and static files.

---

## 🚀 Features

* 🛍️ Product listing using Django models
* 🖼️ Static image-based product catalog
* 🧩 Django app structure (`store`)
* 📄 Template rendering using Django
* ⚙️ Backend-powered website

---

## 🛠️ Tech Stack

* **Python** 🐍
* **Django** 🌐
* **HTML, CSS, JavaScript** 🎨
* **SQLite (default Django DB)**

---

## 📂 Project Structure

```bash
Olympus_Wears/
│── olympus/          # Main project settings
│── store/            # App handling products
│    ├── models.py
│    ├── views.py
│    ├── urls.py
│    ├── templates/store/
│    ├── static/store/
│
│── manage.py
│── requirements.txt
│── README.md
```

---

## ⚙️ How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Olympus_Wears.git
cd Olympus_Wears
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Start server

```bash
python manage.py runserver
```

👉 Open browser:
`http://127.0.0.1:8000/`

---

## 📸 Screenshots

*Add your website screenshots here*

---

## 🔐 Environment Variables

No sensitive environment variables are required for this project.

---

## 📌 Future Improvements

* 🛒 Add cart functionality
* 🔍 Product search & filtering
* 👤 User authentication system
* 💳 Payment gateway integration
* ☁️ Deployment (Render / Railway / AWS)
* 🗄️ Database upgrade (PostgreSQL / MongoDB)

---

## 🤝 Contributing

Feel free to fork this repository and contribute.

---

## 👤 Author

**Pallav Dahal**
Aspiring Data Engineer | Full Stack Developer

---

⭐ If you like this project, give it a star on GitHub!
