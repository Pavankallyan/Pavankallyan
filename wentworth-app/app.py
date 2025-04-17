from flask import Flask, render_template, request
import pymysql.cursors

app = Flask(__name__)

# Database Configuration - Update with your credentials
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Joe@011012',
    'database': 'UniversityDB',
    'cursorclass': pymysql.cursors.DictCursor
}

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    if request.method == 'POST':
        query = request.form['query']
        try:
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
        except Exception as e:
            results = [{'error': str(e)}]
        finally:
            connection.close()
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)