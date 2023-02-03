from flask import render_template, redirect, request, session, flash
from flask_app import app, bcrypt
from flask_bcrypt import Bcrypt
from flask_app.models.users_model import User
from flask_app.models.journal_entries_model import Entry
import datetime 

from calendar import monthrange
import calendar

bcrypt = Bcrypt(app)

# ----------LOGIN/REGISTER VIEW ----------
@app.route("/")
def index():
    if "user_id" in session:
        return redirect('/dashboard')
    return render_template("index.html")

# ---------- REGISTER ----------
@app.route("/user/register", methods=["post"])
def create():
    print(request.form)
    if not User.register_validate(request.form):
        return redirect("/")
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': hashed_pw
    }
    user_id = User.register(data)
    session['user_id'] = user_id
    return redirect("/dashboard")

# ---------- LOGIN ----------
@app.route("/user/login", methods=["post"])
def login():
    data = {
        "email": request.form["email"]
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid credentials", "log")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid credentials", "log")
        return redirect("/")
    session["user_id"] = user_in_db.id
    return redirect("/")

# ---------- DASHBOARD VIEW ----------
@app.route("/dashboard")
def dash():
    if 'user_id' not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    logged_user = User.get_by_id(data)
    entries = Entry.get_all_by_user_id(data)
    current_month_number = int(datetime.date.today().strftime("%m"))
    current_month_name = datetime.date.today().strftime("%B")
    current_year = datetime.date.today().strftime("%Y")
    current_day = datetime.date.today().strftime("%d")
    number_of_days_in_month = monthrange(int(current_year), current_month_number)
    all_days = [datetime.date(int(current_year), int(current_month_number), day)for day in range(1, number_of_days_in_month[1] + 1)]
    number_of_days_in_month = int(number_of_days_in_month[1])
    entry_for_day = False
    for entry in entries:
        if entry.date == f"{current_month_number}{current_day}{current_year}":
            entry_for_day = True
    session['month_now'] = current_month_number
    print('-------------------------->', current_month_number)
    print('-------------------------->', current_day)
    print('-------------------------->', current_year)
    print('-------------------------->', all_days)

    month = []
    week = []
    print(all_days[0].weekday())
    for day in range(all_days[0].weekday()+1):
        week.append(None)
    for day in all_days:
        if(day.weekday()== 6):
            month.append(week)
            week = []
        week.append(day)
    month.append(week)
    print(month)

    # print("THIS IS THE DATE: ", number_of_days_in_month) # RETURNS WHEN THE FIRST DAY IS AND THE NUMBER OF DAYS IN THAT MONTH
    return render_template("dashboard.html", logged_user=logged_user, entries=entries, current_year = current_year, current_day = current_day, current_month_name = current_month_name, number_of_days_in_month = number_of_days_in_month, current_month_number = current_month_number, month = month, entry_for_day = entry_for_day)

# ----------PAST MONTH ----------
# @app.route("/dashboard/back")
# def dashback():
#     if 'user_id' not in session:
#         return redirect("/")
#     data = {"id": session["user_id"]}
#     logged_user = User.get_by_id(data)
#     entries = Entry.get_all_by_user_id(data)
#     current_month_number = int(datetime.date.today().strftime("%m"))-1
#     current_month_name = datetime.date.today().strftime("%B")
#     current_year = datetime.date.today().strftime("%Y")
#     current_day = datetime.date.today().strftime("%d")
#     number_of_days_in_month = monthrange(int(current_year), current_month_number)
#     all_days = [datetime.date(int(current_year), int(current_month_number), day)for day in range(1, number_of_days_in_month[1] + 1)]
#     number_of_days_in_month = int(number_of_days_in_month[1])
#     entry_for_day = False
#     past_month = calendar.month_name[current_month_number]
#     for entry in entries:
#         if entry.date == f"{current_month_number}{current_day}{current_year}":
#             entry_for_day = True

#     print('-------------------------->', current_month_number)
#     print('-------------------------->', current_day)
#     print('-------------------------->', current_year)
#     print('-------------------------->', all_days)
#     print('--------------------------->', calendar.month_name[current_month_number])

#     month = []
#     week = []
#     print(all_days[0].weekday())
#     for day in range(all_days[0].weekday()+1):
#         week.append(None)
#     for day in all_days:
#         if(day.weekday()== 6):
#             month.append(week)
#             week = []
#         week.append(day)
#     month.append(week)
#     print(month)

#     # print("THIS IS THE DATE: ", number_of_days_in_month) # RETURNS WHEN THE FIRST DAY IS AND THE NUMBER OF DAYS IN THAT MONTH
#     return render_template("dashboard.html", logged_user=logged_user, entries=entries, current_year = current_year, current_day = current_day, current_month_name = current_month_name, number_of_days_in_month = number_of_days_in_month, current_month_number = current_month_number, month = month, entry_for_day = entry_for_day, past_month = past_month)

# ----------FORWARD MONTH ----------



# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------- SETTINGS ----------
@app.route('/settings')
def settings():
    return render_template('settings.html')

