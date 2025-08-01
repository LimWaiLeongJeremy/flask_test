from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from extension import db
import model
import os

app = Flask(__name__)
CORS(app)

config_class = 'DevelopmentConfig'
config_class = os.getenv('FLASK_CONFIG', 'DevelopmentConfig')
app.config.from_object(f'config.{config_class}')

# db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html') 


if __name__ == "__main__":
    app.run(debug=True)
