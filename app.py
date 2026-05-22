from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

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
    return f'<Agent {self.title}>'

with app.app_context():
    db.create_all()


# 📌 Главная страница: список агентов
@app.route('/')
@app.route('/agents')
def get_agents():
    agents = Agent.query.all()  # Получаем все задачи из базы
    return render_template('agents.html', agents=agents)


# 📌 Добавление новой задачи
@app.route('/add', methods=['GET', 'POST'])
def add_agent():
    if request.method == 'POST':
        codename = request.form['codename']
        phone = request.form['phone']
        email =request.form['email']
        access_level = request.form['access_level']

        if codename.strip():  # Проверяем, что строка не пустая
            new_agent = Agent(
                codename=codename,
                phone=phone,
                email=email,
                access_level=access_level
            )
            db.session.add(new_agent)
            db.session.commit()
        return redirect(url_for('get_agents'))
    return render_template('add.html')


# 📌 Просмотр данных
@app.route('/agent', methods=['GET', 'POST'])
def get_agent():
    if request.method == 'POST':
        codename = request.form['codename']
        if codename.strip():  # Проверяем, что строка не пустая
            new_agent = Agent(codename=codename)
            db.session.add(new_agent)
            db.session.commit()
        return redirect(url_for('get_agents'))
    return render_template('add.html')


# 📌 Редактирование задачи
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_agent(id):
    agent = Agent.query.get_or_404(id)  # Получаем задачу по ID
    if request.method == 'POST':
        new_agent = request.form['title']
        if new_agent.strip():
            agent.codename = new_agent
            db.session.commit()
        return redirect(url_for('get_agents'))
    return render_template('edit.html', agent=agent)

# 📌 Удаление задачи
@app.route('/delete/<int:id>')
def delete_agent(id):
    agent = Agent.query.get_or_404(id)  # Получаем задачу по ID
    db.session.delete(agent)  # Удаляем из базы
    db.session.commit()  # Подтверждаем изменения
    return redirect(url_for('get_agents'))

# Запуск сервера
if __name__ == "__main__":
    app.run(debug=True)
