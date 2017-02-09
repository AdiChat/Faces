from flask import Flask
app = Flask(__name__)

@app.route('/')
def message():
   return 'Do you look like a Nobel Laureate, Physicist, Chemist, Mathematician, Actor or a Programmer? '

if __name__ == '__main__':
   app.run()