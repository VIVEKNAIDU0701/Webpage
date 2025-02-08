from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="chatbot_db"
)

@app.route('/')  # This serves the chatbot webpage
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])  # This handles chat messages
def chat():
    data = request.json
    user_query = data.get('query', '').lower()

    cursor = db.cursor(dictionary=True)
    
    # Use LIKE for flexible matching
    cursor.execute("SELECT answer FROM responses WHERE question LIKE %s", ('%' + user_query + '%',))
    result = cursor.fetchone()
    
    if result:
        return jsonify({"response": result['answer']})
    else:
        return jsonify({"response": "Sorry, I don't understand. Can you ask differently?"})

if __name__ == '__main__':
    app.run(debug=True)
