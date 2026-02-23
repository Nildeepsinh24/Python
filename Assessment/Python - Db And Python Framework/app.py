from flask import Flask, render_template, request, redirect, session, flash
import os

app = Flask(__name__)
app.secret_key = "simple123"

# ------------------------------
# Helper functions
# ------------------------------
def load_users():
    if not os.path.exists("users.txt"):
        return {}
    users = {}
    with open("users.txt") as f:
        for line in f:
            name, pwd, role = line.strip().split(",")
            users[name] = {"password": pwd, "role": role}
    return users

def save_user(username, password, role="user"):
    with open("users.txt", "a") as f:
        f.write(f"{username},{password},{role}\n")

def load_tasks():
    if not os.path.exists("tasks.txt"):
        return []
    tasks = []
    with open("tasks.txt") as f:
        for line in f:
            user, title, status = line.strip().split(",")
            tasks.append({"user": user, "title": title, "status": status})
    return tasks

def save_tasks(tasks):
    with open("tasks.txt", "w") as f:
        for t in tasks:
            f.write(f"{t['user']},{t['title']},{t['status']}\n")

# ------------------------------
# Routes
# ------------------------------
@app.route('/')
def home():
    if 'user' in session:
        return redirect('/dashboard')
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash("User already exists!", "danger")
        else:
            save_user(username, password)
            flash("Registered successfully! Please login.", "success")
            return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]["password"] == password:
            session['user'] = username
            session['role'] = users[username]["role"]
            return redirect('/dashboard')
        else:
            flash("Invalid credentials!", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    
    tasks = load_tasks()
    user_tasks = [t for t in tasks if t['user'] == session['user'] or session['role'] == 'admin']

    if request.method == 'POST':
        title = request.form['title']
        tasks.append({"user": session['user'], "title": title, "status": "Pending"})
        save_tasks(tasks)
        flash("Task added successfully!", "success")
        return redirect('/dashboard')

    return render_template('dashboard.html', user=session['user'], role=session['role'], tasks=user_tasks)

@app.route('/complete/<int:index>')
def complete(index):
    tasks = load_tasks()
    if index < len(tasks):
        tasks[index]['status'] = "Completed"
        save_tasks(tasks)
    return redirect('/dashboard')

@app.route('/delete/<int:index>')
def delete(index):
    tasks = load_tasks()
    if index < len(tasks):
        if tasks[index]['user'] == session['user'] or session['role'] == 'admin':
            del tasks[index]
            save_tasks(tasks)
    return redirect('/dashboard')

@app.route('/admin')
def admin_panel():
    if 'role' not in session or session['role'] != 'admin':
        return redirect('/dashboard')

    users = load_users()
    tasks = load_tasks()
    return render_template('admin.html', users=users, tasks=tasks, admin=session['user'])

if __name__ == '__main__':
    app.run(debug=True)
