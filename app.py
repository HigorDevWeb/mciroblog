from flask import Flask, request, render_template,app
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os 
app = Flask(__name__)

load_dotenv()
# Database Connection
client = MongoClient(os.getenv('MONGODB_URI'))
app.db = client.microblog

def home():
    """
    Handles GET and POST requests to the homepage.

    On GET requests, retrieves and formats entries from the database for display.
    On POST requests, processes the form data and inserts a new entry into the database.

    Returns:
        A rendered template with the formatted entries.

    Example:
        >>> home()
        <html>...</html>  # rendered HTML template
    """
    if request.method == "POST":
        # Process POST request
        entry_content = request.form.get("content")
        formatted_date = datetime.today().strftime("%Y-%m-%d")
        app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

    # Retrieve and format entries for display
    entries_with_date = [
        (
            entry["content"],
            entry["date"],
            datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
        )
        for entry in app.db.entries.find()
    ]

    return render_template("home.html", entries=entries_with_date)

@app.route("/", methods=["GET", "POST"])
def home_route():
    """
    Route for the homepage.

    Calls the `home` function to handle the request.

    Returns:
        The result of the `home` function.
    """
    return home()

if __name__ == "__main__":
    app.run()