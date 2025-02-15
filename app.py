from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from ai_quiz_app.app import quiz_app
from first.app import first_app
from resume_ats.app import resume_app

app = Flask(__name__)

# ✅ Secret Key for Sessions
app.secret_key = "f9a8b7c6d5e4f3a2b1c0d9e8f7g6h5i4"

# ✅ MongoDB setup
app.config["MONGO_URI"] = "mongodb://localhost:27017/authDB"
mongo = PyMongo(app)

# ✅ Make `mongo` available to Blueprints
app.mongo = mongo

# Register Blueprints
app.register_blueprint(quiz_app, url_prefix="/ai_quiz")
app.register_blueprint(first_app, url_prefix="/first")
app.register_blueprint(resume_app, url_prefix="/resume")
# Serve KeyQuest Static Files
@app.route("/keyquest/")
def keyquest():
    return send_from_directory(os.path.join(app.root_path, "keyquest"), "index.html")

# Serve CSS & JS for KeyQuest
@app.route("/keyquest/<path:filename>")
def keyquest_static(filename):
    return send_from_directory(os.path.join(app.root_path, "keyquest"), filename)

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
