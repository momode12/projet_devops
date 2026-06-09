from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User
from config import Config, DockerConfig
import os

app = Flask(__name__)

# Configuration selon l'environnement
if os.environ.get('DOCKER_ENV') == 'true':
    app.config.from_object(DockerConfig)
else:
    app.config.from_object(Config)

# Initialiser la base de données
db.init_app(app)

# Créer les tables
with app.app_context():
    db.create_all()

# ============ ROUTES CRUD ============

@app.route('/')
def index():
    users = User.query.order_by(User.date_creation.desc()).all()
    return render_template('index.html', users=users)

@app.route('/view/<int:id>')
def view(id):
    user = User.query.get_or_404(id)
    return render_template('view.html', user=user)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        telephone = request.form.get('telephone', '')
        
        if User.query.filter_by(email=email).first():
            flash('Cet email existe déjà !', 'error')
            return redirect(url_for('create'))
        
        new_user = User(nom=nom, prenom=prenom, email=email, telephone=telephone)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Utilisateur créé avec succès !', 'success')
        return redirect(url_for('index'))
    
    return render_template('create.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        user.nom = request.form['nom']
        user.prenom = request.form['prenom']
        user.email = request.form['email']
        user.telephone = request.form.get('telephone', '')
        
        db.session.commit()
        flash('Utilisateur modifié avec succès !', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit.html', user=user)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    
    flash('Utilisateur supprimé avec succès !', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)