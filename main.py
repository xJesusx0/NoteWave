from models import *
from flask import *
from flask_session import *

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET","POST"])
def index():
    if not session.get("name"):
        return redirect("/login")
    
    UserId = session["id"]
    Notes = TableNotes.GetNotes(UserId)

    if request.method == "POST":     
        Title = request.form.get("Title")
        Content = request.form.get("Content")

        TableNotes.Add((UserId,Title,Content))

     
    return render_template("index.html",notes = Notes)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        Username = request.form.get("Name")
        Password = request.form.get("Password")

        if TableUsers.Validate(Username,Password):
            session["id"] = TableUsers.GetId(Username)
            session["name"] = Username
            return redirect("/")
        
    return render_template("login.html")

@app.route("/logout")
def logout():
    session["id"] = None
    session["name"] = None
    return redirect("/")

app.run(port=4000, debug=True)
