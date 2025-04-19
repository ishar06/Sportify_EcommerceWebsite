
# 🛍️ Sportify - E-commerce Website

Sportify is a full-featured, responsive e-commerce website built using **Flask** and **Django** frameworks. Designed as an Amazon clone, Sportify aims to provide a seamless online shopping experience with core functionalities like user authentication, product catalog, shopping cart, and checkout simulation. 

This repository contains two versions:
- [`Sportify_Flask`](./Sportify_Flask): Original version built using Flask
- [`Sportify_Django`](./Sportify_Django): Django-based version with modular app structure

---

## 👨‍💻 About the Team

We are a team of passionate developers from a tech background, striving to build scalable and user-friendly web applications. Sportify represents our collaborative journey from backend logic to frontend polish, implementing both RESTful practices and modern UI/UX standards.

### Team Members

| Name               | Role                                           | Email                          | LinkedIn |
|--------------------|------------------------------------------------|--------------------------------|----------|
| **Ishardeep Singh** | Team Leader, UI/UX Developer, Flask-Django Integrator | ishardeep3195.beai24@chitkara.edu.in        | [LinkedIn](https://www.linkedin.com/in/ishardeep-singh-743789311/) |
| **Aryan Verma**     | Shopping Cart & Payment Gateway, ChatBot (Flask-Django) | aryan3181.beai24@chitkara.edu.in      | [LinkedIn](https://www.linkedin.com/in/aryan-verma-638594320/) |
| **Damanjeet Singh** | User Authentication & Backend Logic (Flask-Django)    | damanjeet3183.beai24@chitkara.edu.in   | [LinkedIn](https://www.linkedin.com/in/damanjeet-singh-834596316/) |
| **Madhav Garg**     | App Routing & Debugging (Flask-Django)               | madhav3219.beai24@chitkara.edu.in      | [LinkedIn](https://www.linkedin.com/in/madhav-garg-059b4b339/) |



---

## 🚀 Features

✅ Responsive design using **Bootstrap 5**  
✅ Secure **Login/Signup** with form validation  
✅ **Admin and Customer roles**  
✅ **Product catalog** with search, sort, and filter  
✅ **Add to Cart**, **Update**, and **Remove** functionalities  
✅ Simulated **Checkout and Address Entry**  
✅ **Pagination & Infinite Scroll** (bonus)  
✅ Real-time **Flash messages** and **Modals**  
✅ Reusable **base.html** layout with Jinja templating  
✅ Django version has modular apps: `user_app`, `cart_app`

---

## 📂 Project Structure

```
Sportify_EcommerceWebsite/
│
├── Sportify_Flask/
│   ├── templates/
│   ├── static/
│   └── app.py
│   └── requirements.txt
│
├── Sportify_Django/
│   ├── Sportify1/
│   ├── user_app/
│   ├── cart_app/
│   ├── media/
│   ├── static/
│   ├── templates/
│   └── manage.py
│   └── requirements.txt
```

---

## 🔧 Tech Stack

- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Backend (Flask)**: Python, SQLite, Flask, Jinja2
- **Backend (Django)**: Python, Django, SQLite
- **Version Control**: Git & GitHub

---

## 📦 Setup Instructions

### For Flask Version

```bash
cd Sportify_Flask
python -m venv venv

# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
cd Sportify_Flask
python app.py
```
ADMIN LOGIN CREDENTIALS:

Go the url : http://127.0.0.1:5000/admin/login

Username ==> admin@sportify.com, 
Password ==> admin123

### For Django Version

```bash
cd Sportify_Django
python -m venv venv

# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
cd Sportify1/
python manage.py migrate
python manage.py runserver
```
ADMIN LOGIN CREDENTIALS:

Username ==> admin@sportify.com, 
Password ==> admin123

---

## 🙌 Acknowledgements

Thanks to our mentors, classmates, and the open-source community for guidance and tools that helped us build this project.

---

## 📫 Connect With Us

Feel free to reach out via LinkedIn or GitHub if you have feedback or want to collaborate!

---

> Made with 💖 by Team Sportify
