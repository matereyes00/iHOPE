from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # You can pass any additional data your template needs here
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
