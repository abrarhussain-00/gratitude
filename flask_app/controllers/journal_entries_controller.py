from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.journal_entries_model import Entry
from flask_app.models.users_model import User
import requests
import calendar

import datetime
quote_of_day = requests.get('https://zenquotes.io/api/today')
quote_of_day = quote_of_day.json()
quote = {
    "quote_of_day" : quote_of_day[0]['q'],
    "author" : quote_of_day[0]['a']
}
print((quote_of_day[0]['q']))


print(quote_of_day[0])
# ---------- VIEW ENTRY ----------
@app.route("/entry/view/<int:date>")
def entry_view(date):
    if "user_id" not in session:
        return redirect("/")
    data = {
        'id': session['user_id'],
        'date': date
    }
    MMDDYYYY  = date
    YYYY      = MMDDYYYY %  10000       
    DD        = MMDDYYYY // 10000 % 100
    MM        = MMDDYYYY // 1000000
    current_day = DD
    current_month_name = calendar.month_name[MM]
    current_year = YYYY
    # quote = 'Comparison is the theif of joy. - Theodore Roosevelt'
    get_entry = Entry.get_one_by_date(data)
    global quote
    return render_template("entry_view.html", get_entry = get_entry, date = date, quote = quote, current_day = current_day, current_month_name = current_month_name, current_year = current_year)

# ---------- ADD ENTRY VIEW ----------
@app.route("/entry/new/<int:date>")
def add_view(date):
    if "user_id" not in session:
        return redirect("/")
    current_day = datetime.date.today().strftime("%d")
    current_month_name = datetime.date.today().strftime("%B")
    current_year = datetime.date.today().strftime("%Y")
    # quote = 'Comparison is the theif of joy. - Theodore Roosevelt'
    global quote
    return render_template("entry_create.html", date = date, quote = quote, current_day = current_day, current_month_name = current_month_name, current_year = current_year)

# ---------- ADD EDIT VIEW ----------
@app.route("/entry/edit/<int:date>")
def edit_view(date):
    print("------------------>", date)
    if "user_id" not in session:
        return redirect("/")
    current_day = datetime.date.today().strftime("%d")
    current_month_name = datetime.date.today().strftime("%B")
    current_year = datetime.date.today().strftime("%Y")
    # quote = 'Comparison is the theif of joy. - Theodore Roosevelt'
    global quote
    entry_data = {"date": date,
        "id": session['user_id']
    } 
    print(entry_data)
    entry = Entry.get_one_by_date(entry_data)
    if not entry:
        return redirect('/dashboard')
    return render_template("entry_edit.html", entry=entry, date = date, quote = quote, current_day = current_day, current_month_name = current_month_name, current_year = current_year)

# ---------- ADD ENTRY ACTION ----------
@app.route("/entry/create/<int:date>", methods=["post"])
def create_entry(date):
    if "user_id" not in session:
        return redirect("/")
    entry_add = {
        **request.form,
        "user_id": session["user_id"],
        "date": date
    }
    if not Entry.entry_validate(entry_add):
        return redirect(f"/entry/new/{date}")
    Entry.create_entry(entry_add)
    return redirect("/dashboard")

# ---------- EDIT ENTRY ACTION ----------
@app.route("/entry/edit_action", methods=["post"])
def edit_entry():
    if "user_id" not in session:
        return redirect("/")
    entry_edit = {
        **request.form,
        'user_id': session['user_id']
    }
    if not Entry.entry_validate(entry_edit):
        return redirect(f"/entry/edit/{request.form['id']}")
    Entry.edit_entry(entry_edit)
    return redirect("/dashboard")

# ---------- DELETE Sighting ----------
@app.route("/sightings/delete/<int:id>")
def delete(id):
    if "user_id" not in session:
        return redirect("/")
    entry_delete = {"id": id}
    Entry.delete(entry_delete)
    return redirect("/dashboard")

