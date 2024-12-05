# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from db import db
from models import Task, User
from forms import LoginForm, RegistrationForm

app = Flask(__name__)
app.secret_key = "8cd5a4b11e9bd5bd5c5402109a52ca3cb1e48167cc13c314f9f8d0e057d206d9"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo_list.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_SECRET_KEY'] = 'random key for CSRF protection'
db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()


# Reste de votre code...
@app.before_request
def create_tables():
    db.create_all()

def format_datetime(value, format='%Y-%m-%d %H:%M:%S'):
    if value is None: return ""
    return value.strftime(format)

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', username=username)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect', 'danger')
            return redirect(request.url)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Vous avez été déconnecté', 'success')
    return redirect(url_for('login'))


@app.route('/compteur')
def compteur():
    if "compteur" not in session:
        session['compteur'] = 1
    else:
        session['compteur'] = session['compteur'] + 1
    print(session)
    nombre_visites = session['compteur']
    return f"Vous avez visité la page {nombre_visites} fois"

# Route pour ajouter une tâche
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')
        date = request.form['date']
        time = request.form['time']

        # Insertion dans la base de données
        new_task = Task(title=title, description=description, date=date, time=time)
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('list_tasks'))

    return render_template('add.html')

# Route pour afficher toutes les tâches
@app.route('/list')
def list_tasks():
    tasks = Task.query.all()
    return render_template('list.html', tasks=tasks)

# Route pour consulter une tâche spécifique (par ID)
@app.route('/view/<int:task_id>')
def view_task(task_id):
    task = Task.query.get(task_id)
    return render_template('view.html', task=task)

# Route pour modifier une tâche
@app.route('/tasks/edit/<int:task_id>/', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get(task_id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.date = request.form['date']
        task.time = request.form['time']
        db.session.commit()
        return redirect(url_for('view_task', task_id=task_id))
    return render_template('edit.html', task=task)

# Route pour supprimer une tâche
@app.route('/tasks/delete/<int:task_id>/', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('list_tasks'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User(username=username)
        new_user.set_password(password)  # Assurez-vous que la méthode set_password est définie dans votre modèle User
        db.session.add(new_user)
        db.session.commit()
        flash('Votre compte a été créé avec succès!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)