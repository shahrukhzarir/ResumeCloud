from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku

#create flask application
app = Flask(__name__)

#create database and heroku connection
heroku = Heroku(app)
db = SQLAlchemy(app)

# Create our database model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<E-mail %r>' % self.email

class FileContents(db.Model):
    __tablename__="files"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)


# new homepage
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/prereg', methods=['POST'])
def prereg():
    email = ""
    if request.method == 'POST':
        email = request.form['email']

        #if email doesnt exist add it or if it does just ignore
        if not db.session.query(User).filter(User.email == email).count():
            reg = User(email)
            db.session.add(reg)
            db.session.commit()
            return render_template('success.html')
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']
    newFile = FileContents(name=file.filename, data=file.read())
    db.session.add(newFile)
    db.session.commit()
    return render_template('success.html')


if __name__ == '__main__':
    app.run()
