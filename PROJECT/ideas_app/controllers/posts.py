from ideas_app import app
from ideas_app.models.user import *
from ideas_app.models.post import *
from ideas_app.models import *
from ideas_app.controllers import users
from flask import render_template, redirect, request, session,url_for

@app.route('/bright_ideas/delete/<int:id>')
def delete_post(id):
    data ={
        'id': id
    }
    Post.destroy(data)
    flash(f"Post #{id} has been deleted successfully!")
    return redirect('/bright_ideas')

@app.route('/bright_ideas/like/<int:id>')
def like_post(id):
    data ={
        'user_id': session.get("id"),
        'idea_id':id,
    }
    Post.like(data)
    return redirect('/bright_ideas')


@app.route('/bright_ideas/<int:id>')
def like_status(id):
    ideas = Post.get_posts_with_user()
    likes = Post.getLikes()
    alias = Post.get_alias_name(id)
    return render_template("like_status.html",ideas=ideas,likes=likes,id=id,alias=alias)

@app.route('/bright_ideas/likes/<int:id>')
def cant_likes(id):
    data ={
        'id': id
    }
    likes = Post.get_amount_of_likes_by_post(data['id'])
    print("LIKES cant_likes FUNCT ", likes)
    return render_template('/bright_ideas',likes=likes)

