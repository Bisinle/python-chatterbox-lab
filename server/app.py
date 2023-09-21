from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import desc


from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages',methods=['GET','POST'])
def messages():
    '''eturns an array of all messages as JSON, ordered by created_at 
        in ascending order.'''
    messages = Message.query.order_by(desc(Message.created_at))

    if request.method == 'GET':
        messages_list=[]
        for message in messages:
            message_dict={
                'id':message.id,
                'username':message.username,
                'body':message.body,
                'created_at':message.created_at,
                'updated_at':message.updated_at,
            }
            messages_list.append(message_dict)

        response = make_response(jsonify(messages_list),200)

        return response
    


    elif request.method == 'POST':

        data = request.get_json()
        message = Message(
            username = data.get('username'),
            body = data.get('body')
        )
        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()

        return make_response((message_dict),201)


@app.route('/messages/<int:id>',methods =['GET','PATCH','DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()

    print(message)

    if request.method == 'GET':
        message_dict = message.to_dict()
        return make_response(message_dict,200)
     



    if request.method == 'PATCH':
        for attr in request.form:
         setattr(message, attr, request.form.get(attr))
        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()

        return make_response(message_dict,200)

    if request.method =='DELETE':
        db.session.delete(message)
        db.session.commit()

        response = {
            'delete_successful':True,
            'message':'Message Deleted'
       }
        return make_response(response,200)
    
        


if __name__ == '__main__':
    app.run(port=5555, debug=True)
