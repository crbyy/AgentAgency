from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agents.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codename = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    access_level = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Agent {self.codename}>'

with app.app_context():
    db.create_all()


# 📌 Главная страница: список агентов
@app.route('/')
@app.route('/agents')
def get_agents():
    level = request.args.get('level', 'all')
    agents = Agent.query

    if level != 'all':
        agents = agents.filter(Agent.access_level == level)

    agents = agents.all()
    return render_template('agents.html', agents=agents, current_level=level)


# 📌 Добавление нового агента
@app.route('/add', methods=['GET', 'POST'])
def add_agent():
    error = None
    if request.method == 'POST':
        codename = request.form['codename']
        phone = request.form['phone']
        email =request.form['email']
        access_level = request.form['access_level']

        existing = Agent.query.filter_by(codename=codename).first()
        if existing:
            error = 'Агент с таким кодовым именем уже существует!'
        elif codename.strip():
            new_agent = Agent(
                codename=codename,
                phone=phone,
                email=email,
                access_level=access_level
            )
            db.session.add(new_agent)
            db.session.commit()
            return redirect(url_for('get_agents'))

    return render_template('add.html', error=error)


# 📌 Просмотр списка агентов
@app.route('/agent/<int:id>')
def get_agent(id):
    agent = Agent.query.get_or_404(id)
    return render_template('data.html', agent=agent)


# 📌 Редактирование агента
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_agent(id):
    agent = Agent.query.get_or_404(id)  # Получаем агента по ID
    if request.method == 'POST':
        new_codename = request.form['codename']
        new_phone = request.form['phone']
        new_email = request.form['email']
        new_access_level = request.form['access_level']

        if new_codename.strip():
            agent.codename = new_codename
            agent.phone = new_phone
            agent.email = new_email
            agent.access_level = new_access_level
            db.session.commit()
        return redirect(url_for('get_agents'))
    return render_template('edit.html', agent=agent)



# 📌 Поиск агента по кодовому имени
@app.route('/search', methods=['GET', 'POST'])
def search_agent():
    agents = []
    query = ''
    if request.method == 'POST':
        query = request.form.get('search')
        if query:
            agents = Agent.query.filter(Agent.codename.contains(query)).all()
    return render_template('search.html', agents=agents, query=query)





# 📌 Удаление агента
@app.route('/delete/<int:id>', methods=['POST'])
def delete_agent(id):
    agent = Agent.query.get_or_404(id)
    db.session.delete(agent)
    db.session.commit()
    return redirect(url_for('get_agents'))

# 📌 Удаление ВСЕХ
@app.route('/delete_all', methods=['POST'])
def delete_all():
    Agent.query.delete()
    db.session.commit()
    return redirect(url_for('get_agents'))

# Запуск сервера
if __name__ == "__main__":
    debug_mode = os.getenv('flask_debug') == 'True'
    app.run(debug=debug_mode)
