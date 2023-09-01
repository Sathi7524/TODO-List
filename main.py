from flask import Blueprint, Flask, render_template, send_from_directory

from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials

app = Flask(__name__)
CORS(app)
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)
from api import todo_info


todolist=Blueprint('to-do-list',__name__,template_folder='to-do-list/dist/to-do-list')
app.register_blueprint(todolist)

app.register_blueprint(todo_info,url_prefix='/api')

@app.route('/assets/<path:filename>')
def custom_static_for_assets(filename):
    return send_from_directory('to-do-list/dist/to-do-list/assets',filename)

@app.route('/<path:filename>')
def custom_static(filename):
    return send_from_directory('to-do-list/dist/to-do-list/',filename)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)