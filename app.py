from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# MongoDB Atlas Connection String

MONGO_URI = "mongodb+srv://ermanoj250:ermanoj250@parul.xpxgml1.mongodb.net/?appName=parul"

# Create a new client and connect to the server
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = Flask(__name__)


client = MongoClient(MONGO_URI)

# Database and Collection
db = client["flaskdb"]
collection = db["users"]

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():

    try:
        name = request.form['name']
        email = request.form['email']

        data = {
            "name": name,
            "email": email
        }

        # Insert data into MongoDB
        collection.insert_one(data)

        # Redirect only on success
        return redirect(url_for('success'))

    except Exception as e:

        # Stay on same page and show error
        return render_template(
            'form.html',
            error=str(e)
        )

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)