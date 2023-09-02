from flask import Flask, jsonify, request, json
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
# import os

app = Flask(__name__)
CORS(app)
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://vrbgfzfgoxllgb:d420f4a0559ca4cf90146e367a828543aaf87939865876975fe087fb0dc6584b@ec2-107-21-67-46.compute-1.amazonaws.com:5432/d5h7evj9lgj92k'
db = SQLAlchemy(app)

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.Text, nullable=False)

  def __str__(self):
    return f'{self.id} {self.content}'

def todo_serializer(todo):
   return {
      'id': todo.id,
      'content': todo.content
   }

@app.route('/', methods=['GET'])
@cross_origin()
def serve_frontend():
    return app.send_static_file('index.html')

@app.route('/static/<path:path>')
@cross_origin()
def serve_static(path):
   return app.send_static_file(os.path.join('YouDoTodo-App', 'public', path))

@app.route('/api', methods=['GET'])
@cross_origin()
def index():
    return jsonify([*map(todo_serializer, Todo.query.all())])

@app.route('/api/create', methods=['POST'])
def create():
  request_data = json.loads(request.data)
  todo = Todo(content=request_data['content'])

  db.session.add(todo)
  db.session.commit()

  return {'201': 'todo created successfully'}

@app.route('/api/<int:id>', methods=['DELETE'])
def delete(id):
   Todo.query.filter_by(id=id).delete()
   db.session.commit()

   return jsonify({'message': 'Deleted successfully'}), 200

@app.route('/api/<int:id>', methods=['PUT'])
def update(id):
    request_data = json.loads(request.data)
    todo = Todo.query.get(id)
    todo.content = request_data['content']
    db.session.commit()

    return jsonify({'message': 'Updated successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
