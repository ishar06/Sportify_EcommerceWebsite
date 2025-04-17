
# 🛍️ Sportify - E-commerce Website

Sportify is a full-featured, responsive e-commerce website built using **Flask** and **Django** frameworks. Designed as an Amazon clone, Sportify aims to provide a seamless online shopping experience with core functionalities like user authentication, product catalog, shopping cart, and checkout simulation. 

This repository contains two versions:
- [`Sportify_Flask`](./Sportify_Flask): Original version built using Flask
- [`Sportify_Django`](./Sportify_Django): Django-based version with modular app structure

---

## 👨‍💻 About the Team

We are a team of passionate developers from a tech background, striving to build scalable and user-friendly web applications. Sportify represents our collaborative journey from backend logic to frontend polish, implementing both RESTful practices and modern UI/UX standards.

### Team Members

| Name            | Role                                  | LinkedIn                                  |
|-----------------|---------------------------------------|--------------------------------------------|
| **Ishar Singh** | Team Leader, UI Developer, Flask-Django Integrator | [LinkedIn](https://www.linkedin.com/in/ishardeep-singh-743789311/) |
| **Aryan**       | Shopping Cart & Payment Gateway, ChatBot (Flask-Django) | [LinkedIn](https://www.linkedin.com/in/aryan-verma-638594320/) |
| **Damanjeet**   | User Authentication & Backend Logic (Flask-Django)    | [LinkedIn](https://www.linkedin.com/in/damanjeet-singh-834596316/) |
| **Madhav**      | App Routing & Debugging (Flask-Django)               | [LinkedIn](https://www.linkedin.com/in/madhav-garg-059b4b339/) |


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
✅ Django version has modular apps: `UserApp`, `CartApp`

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
pip install -r requirements.txt
python app.py
```

### For Django Version

```bash
cd Sportify_Django
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 🙌 Acknowledgements

Thanks to our mentors, classmates, and the open-source community for guidance and tools that helped us build this project.

---

## 📫 Connect With Us

Feel free to reach out via LinkedIn or GitHub if you have feedback or want to collaborate!

---

> Made with 💖 by Team Sportify
