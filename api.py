from functools import wraps
import traceback
from flask import Blueprint, render_template, abort,request
import json
from firebase_admin import firestore, auth

db=firestore.client()
def checkToken(f):
    @wraps(f)
    def decorated_function(*args,**kws):
        if not 'Authorization' in request.headers:
            abort(401,{'message':'Unauthorized caller'})
        user=None
        try:
            data=request.headers['Authorization']
            header_token=str(data)
            token=header_token.split(" ")[-1]
            user=auth.verify_id_token(token)
            kws['uid']=user['uid']
            kws['email']=user['email']
            global emailadd
            emailadd=user['email']
        except Exception:
            traceback.print_exc()
            abort(401)

        return f(*args,**kws)
    return decorated_function
todo_info = Blueprint('todo_info', __name__)

@todo_info.route('/todo', methods=['POST'])
@checkToken
def create(*args,**kwargs):
    print(emailadd)
    todo_info=request.json
    todo_info["email"]=emailadd
    db.collection('todo_info').document().set(todo_info)
    print(request.json)
    return json.dumps(
        {
            'status':'ok',
            'entries':emailadd
        }
    )


@todo_info.route('/list-entries', methods=['POST'])
@checkToken
def list_entries(*args,**kwargs):
    docs = db.collection('todo_info').where('email', u'==', emailadd).stream()
    l=[]
    docid=[]
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')
        d=doc.to_dict()
        d['docid']=doc.id
        print(d)
        docid.append(doc.id)
        l.append(d)
    return json.dumps(
        {
            'status':'ok',
            'entries': l,
            'docid':docid

        }
    )

@todo_info.route('/delete', methods=['POST'])
@checkToken
def delete(*args,**kwargs):
    docid=request.json.get('docid')
    data=db.collection('todo_info').document(docid)
    data.delete()
    return json.dumps(
        {
            'status':'ok'
        }
    )
@todo_info.route('/update', methods=['POST'])
def update(*args,**kwargs):
    docid=request.json.get('docid')
    data=db.collection('todo_info').document(docid)
    data.update({'status':'true'})
    return json.dumps(
        {
            'status':'ok'
        }
    )



