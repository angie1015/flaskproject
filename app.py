from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)



class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    votes = db.Column(db.Integer, nullable=False, default=0)

@app.route('/', methods=['GET'])
def index():
    questions = Question.query.order_by(Question.votes).all()
    return jsonify(questions)

@app.route('/new', methods=['POST'])
def create():
    text = request.args.get('text')
    q = Question(text=text)
    db.session.add(q)
    db.session.commit()
    return 'created successfully'

@app.route('/<id>', methods=['PUT'])
def update(id):
    q = Question.query.filter_by(id = id).first()
    q.votes = q.votes +1
    db.session.commit()
    return 'updated successfully'

@app.before_first_request
def create_tables():
    db.create_all()

if __name__=="__main__":
    app.run(debug=True)