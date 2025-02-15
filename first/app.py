from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer
import os

app = Flask(__name__)

# 🔑 Secret Key for Sessions (Use Environment Variable for Security)
app.secret_key = os.environ.get("SECRET_KEY", "f9a8b7c6d5e4f3a2b1c0d9e8f7g6h5i4")

# 🔹 MongoDB Connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/authDB"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

# Token Serializer for Secure Links
serializer = URLSafeTimedSerializer(app.secret_key)

# Reference to the users collection
users_collection = mongo.db.users

# 🏠 Home Route
@app.route("/")
def home():
    return render_template("signin.html")

# 🔹 SIGN-UP Route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("signup"))

        # Check if email already exists
        if users_collection.find_one({"email": email}):
            flash("Email already exists!", "danger")
            return redirect(url_for("signup"))

        # 🔐 Hash password before storing
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Store user in MongoDB
        users_collection.insert_one({
            "username": username,
            "email": email,
            "password": hashed_password
        })

        flash("User registered successfully!", "success")
        return redirect(url_for("signin"))

    return render_template("signup.html")

# 🔹 SIGN-IN Route
@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = users_collection.find_one({"email": email})

        if user and bcrypt.check_password_hash(user["password"], password):
            session["user"] = user["username"]
            flash("Login Successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials!", "danger")

    return render_template("signin.html")

# 🔹 Forgot Password Route
@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")

        user = users_collection.find_one({"email": email})
        if user:
            token = serializer.dumps(email, salt="password-reset")
            reset_url = url_for("reset_password", token=token, _external=True)

            # TODO: Send this reset_url via email (Mocked for now)
            flash(f"Password reset link: {reset_url}", "info")  # Mocked for testing

        else:
            flash("Email not found!", "danger")

    return render_template("forgot_password.html")

# 🔹 Reset Password Route
@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        email = serializer.loads(token, salt="password-reset", max_age=3600)  # Expires in 1 hour
    except:
        flash("Invalid or expired token!", "danger")
        return redirect(url_for("forgot_password"))

    if request.method == "POST":
        new_password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if new_password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("reset_password", token=token))

        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        users_collection.update_one({"email": email}, {"$set": {"password": hashed_password}})

        flash("Password reset successful! Please log in.", "success")
        return redirect(url_for("signin"))

    return render_template("reset_password.html", token=token)

# 🔹 Dashboard Route (After Login)
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return f"Welcome {session['user']}! You are logged in."
    else:
        flash("Please log in first!", "warning")
        return redirect(url_for("signin"))

# 🔹 Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully!", "info")
    return redirect(url_for("signin"))

if __name__ == "__main__":
    app.run(debug=True)
