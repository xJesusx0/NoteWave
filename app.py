from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from Models.notes import Note

app = Flask(__name__)

@app.route("/")
def index():
    notes = Note.get_notes()
    return render_template("index.html",notes = notes)

@app.route("/add", methods = ["POST"])
def add():
    title = request.form.get("title")
    content = request.form.get("content")

    note = Note(title,content)
    note.add_note()
    return redirect("/")

@app.route("/delete/<int:id>", methods=["GET"])
def delete(id):
    Note.delete(id)
    return redirect("/")

@app.route("/done/<int:id>")
def done(id):
    print(id)
    Note.set_done(id)
    return redirect("/")

if (__name__ == '__main__'):
    app.run( debug = True )