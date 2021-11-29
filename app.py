from flask import Flask, render_template, request, redirect, url_for, Response
import sys
import os 
#from clean_tweets import find_tweetids  as ssearch
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
   if request.method == 'POST':
      linea = request.form['searchString']
      cantidad = request.form['cantidad']
      ans = ssearch(str(linea), int(cantidad))
      print(ans)
      
   
   return render_template('resultados.html', mensaje=ans)

if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))


    