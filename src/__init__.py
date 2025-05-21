from flask import render_template
from src.main import app

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/avaliar')
def avaliar():
    return render_template('avaliar.html')
