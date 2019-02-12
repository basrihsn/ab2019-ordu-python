from flask import Flask, request, render_template, redirect
import random
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)
client = MongoClient()
db = client.ab2019

def roll():
    return random.choice(["yek","du","se","car","penc","se"])

def get_messages():
    return db.messages.find()

@app.route('/', methods=["GET","POST"])
def main():
    if request.method == "POST":
        sender = request.form["sender"]
        body = request.form["body"]
        db.messages.insert({"sender":sender, "body":body})
    return render_template("main.html", messages = get_messages())

@app.route("/edit/<document_id>", methods = ["GET", "POST"])
def edit(document_id):
	if request.method == "POST":
		sender = request.form["sender"]
		body = request.form["body"]
		db.messages.update_one({"_id": ObjectId(document_id)},
							   {"$set": {
							   		"sender": sender,
							   		"body": body
							   }})
		return redirect("/")
	message = db.messages.find_one({"_id": ObjectId(document_id)})
	return render_template("edit.html", message = message)

@app.route("/remove/<document_id>")
def remove(document_id):
	db.messages.remove({"_id": ObjectId(document_id)})
	return redirect("/")

@app.route("/submit")
def submit():
	return render_template("submit.html")

if __name__ == '__main__':
    app.run()
