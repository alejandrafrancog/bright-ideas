from ideas_app import app
from ideas_app.models.user import *
from ideas_app.models.post import *
from flask import render_template, redirect, request, session,url_for
from flask_bcrypt import Bcrypt
from collections import Counter

from flask import flash

bcrypt = Bcrypt(app)

@app.route('/')
@app.route('/main')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        usuario = Usuario.getEmail(email)

        if usuario is None or not bcrypt.check_password_hash(usuario.password, password):
            flash("Contraseña o correo inválidos")
            return redirect('/')
        session["id"] = usuario.id
        return redirect('/bright_ideas')
    else:
        return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if request.form['password'] == request.form['confirm_password']:
            data = dict(request.form)
            print(f"\n\n\n{request.form}\n\n\n")
            data['password'] = bcrypt.generate_password_hash(
                request.form['password'])
            if Usuario.validate_user(request.form):
                usuario = Usuario.save(data)
                print(f"\n\n{usuario}\n\n")
                session["id"] = usuario.id
                return redirect("/bright_ideas")
        else:
            flash("La contraseña debe ser la misma")
            return render_template('index.html')
        return render_template('index.html')


@app.route('/bright_ideas')

def bright_ideas():
    if session.get('id') is None:
        return redirect('/')
    else:
        usuario = Usuario.getId(session)
        ideas = Post.get_posts_with_user()
        likes = Post.getLikes()
        like_counts = Counter(like['idea_id'] for like in likes if like.get('idea_id'))

        like_data = [[idea_id, count] for idea_id, count in like_counts.items()]
        like_data.sort()
        return render_template("user_page.html", user=usuario, ideas=ideas, likes=like_data)

    
@app.route('/add-idea', methods=['GET','POST'])
def postear():
    user = Usuario.get_all()
    posts = Post.save(request.form)
    return redirect(url_for('bright_ideas',ideas=posts,user = user))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')

@app.route('/users/<int:id>')
def user_page(id):
    usuario = Usuario.getId(session)
    user = Usuario.get_all()
    ideas = Post.get_posts_with_user()
    likes = Post.get_amount_of_likes(id)
    total = Usuario.total_posts(id)

    likes = likes[0]['count(user_id)']
  
    return render_template("user_summary.html",users=usuario,ideas=ideas,id=id,usu=user,total=total,cantLikes = likes)