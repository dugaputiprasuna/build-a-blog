from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogger:bloggerpwd@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(120))
    post = db.Column(db.String(250))

    def __init__(self,title,post):
        self.title = title
        self.post = post

    

@app.route('/', methods=['POST', 'GET'])
def index():
  
      return redirect('/blog')




@app.route("/blog", methods=['POST', 'GET'])
def blogInfo():
       bid=""  
       blogs=""
       
       if request.method == 'GET':
          id = request.args.get('id')
       
       if id :
           bid=id
           blogs = Blogs.query.filter_by(id=bid).all()
       else:
           blogs = Blogs.query.all()
         
       return render_template('blog.html',blogs=blogs,id=bid)



@app.route("/newpost", methods=['POST', 'GET'])
def newpostInfo():
    return render_template('newpost.html')

@app.route("/Saveblog", methods=['POST'])
def SavePostInfo():
      title = request.form['title']
      post = request.form['post']
      titlemsg=""
      postmsg=""

      if len(title) == 0:
          titlemsg = "please enter the blog title"
      if len(post) == 0:
          postmsg="please enter the blog post"
  
      if len(titlemsg) or len(postmsg):
          return render_template('newpost.html',title=title,post=post,titlemsg=titlemsg,postmsg=postmsg)
      else:
          new_blog = Blogs(title, post)
          db.session.add(new_blog)
          db.session.commit()

      
      return redirect('/blog?id='+str(new_blog.id))


app.run()  