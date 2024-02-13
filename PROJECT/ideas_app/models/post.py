from flask import flash,request,session,url_for,redirect
from ideas_app.config.mysqlconnection import connectToMySQL
from ideas_app.controllers import users

db_name ="users"
class Post:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def getId(cls, data):
        query = f"select * from ideas where id = %(id)s;"
        mysql = connectToMySQL(db_name)
        result = mysql.query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None
    @classmethod
    def save(cls, data):
       
        user_id = session.get("id")
        query = "insert into ideas (content,user_id) values "\
                f"(%(content)s,{user_id});"
        mysql = connectToMySQL(db_name)
        result = mysql.query_db(query, data)
        data_usuario = {'id': result}
        return cls.getId(data_usuario)
    @classmethod
    def getPosts(cls):
        query = "select * from ideas;"
        results = connectToMySQL(db_name).query_db(query)
        print(results)
        ideas = []
        for i  in results:
            ideas.append( cls(i) )
        return ideas
    @classmethod
    def get_posts_with_user(cls):
        query = "select users.name,users.alias,users.id,users.email,ideas.user_id, ideas.id, ideas.content from users left join ideas on users.id = ideas.user_id;"

        results = connectToMySQL(db_name).query_db(query)
        
        posts = []
        for result  in results:
            posts.append(result)
        return posts
    @classmethod
    def get_posts_by_users(cls,data):
        query = "select users.name, users.alias ideas.content from users left join ideas on users.id = ideas.user_id;"
        results = connectToMySQL(db_name).query_db(query)
        print(results)
        posts = cls(results[0])
        for row in results:
            p = {
                'id': row['id'],
                'users.name': row['users.name'],
                'users.alias': row['users.alias'],
                'ideas.content': row['content']
                
            }
            posts.append( Post(p) )
          
        return posts
    
    @classmethod
    def destroy(cls,data):
        query  = f"DELETE FROM ideas WHERE id = {data['id']};"
        return connectToMySQL(db_name).query_db(query,data)
    
    @classmethod
    def getLikes(cls):
        query = "select * from likes"
        results = connectToMySQL(db_name).query_db(query)
        print("\n\nLikes",results)
        print("\Likes type",type(results))
        likes = []
        for result  in results:
            likes.append(result)
        return likes
    
    @classmethod
    def like(cls,data):
        query = f"insert into likes (user_id,idea_id,amount) values ({session.get('id')},{data['idea_id']},1);"
        result = connectToMySQL(db_name).query_db(query,data)
        return result
    @classmethod
    def get_likes_by_id(cls,data):
        query = f"select * from likes where user_id={data}"
        results = connectToMySQL(db_name).query_db(query)
        likes = []
        for result  in results:
            likes.append(result)
        return likes
    @classmethod
    def get_amount_of_likes(cls,data):
        query = f"select count(user_id) from likes where user_id={data};"
        results = connectToMySQL(db_name).query_db(query)
      
        return results
    @classmethod
    def update_like(cls,idea_id):
        query = f"update likes set amount = amount + 1 where (user_id = {session.get('id')} AND idea_id = {idea_id})"
        results = connectToMySQL(db_name).query_db(query)
        return results


    @classmethod
    def get_amount_of_likes_by_post(cls,id):
        query = f"select amount from likes where idea_id = {id};"
        results = connectToMySQL(db_name).query_db(query)
        return results[0]['amount']
    @classmethod
    def get_alias_name(cls,id):
        query=f"select users.alias,users.name,users.id from users left join likes on users.id = likes.user_id where likes.idea_id={id};"
        results = connectToMySQL(db_name).query_db(query)
        return results