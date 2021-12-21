from flask import Flask, render_template, request, redirect, url_for, Response
import sys
import os 
import face_recognition_project as fr
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('buscador.html')

@app.route('/resultados')
def result():
   return render_template('resultados.html')

    
@app.route('/', methods = ['GET', 'POST'])
def buscar():
   ans = []
   img = request.files['avatar']
   if request.method == 'POST':
      if request.form['colorRadio'] == 'knn':
         cantidad = request.form['cantidad']
         ans = fr.knn_search_rtree(int(cantidad), img)
      elif request.form['colorRadio'] == 'ratio':
         radio = request.form['radio_busqueda']
         ans = fr.range_search(float(radio), img)
                
   return render_template('resultados.html', mensaje=ans)

if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))


    