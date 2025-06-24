# from flask import Flask, render_template, send_from_directory
# import pandas as pd

# app = Flask(__name__)

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# @app.route("/")
# def home():
#   try:
#         # Load CSV file
#         file_path = "news.csv"  # Ensure this is the correct path
#         data = pd.read_csv(file_path)
        
#         # Debug: Print column names and data
#         print("Columns:", data.columns)
#         print(data.head())  # Verify data structure
        
#         # Extract relevant columns
#         records = data[["Headline", "Link", "Date"]].to_dict(orient="records")
#         print("Processed Records:", records)  # Verify processed data
        
#         return render_template("index.html", records=records)
#   except Exception as e:
#         print(f"Error: {e}")
#         return "Error loading data"
# if __name__ == "__main__":
#     app.run(debug=True)


import threading
import subprocess
import time
from flask import Flask, render_template, send_from_directory
import pandas as pd

# Flask App
app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def home():
    try:
        # Load CSV file
        file_path = "news.csv"  # Ensure this is the correct path
        data = pd.read_csv(file_path)

        # Debug: Print column names and data
        # print("Columns:", data.columns)
        # print(data.head())  # Verify data structure

        # Extract relevant columns
        records = data[["Headline", "Link", "Date"]].to_dict(orient="records")
        # print("Processed Records:", records)  # Verify processed data

        return render_template("index.html", records=records)
    except Exception as e:
        print(f"Error: {e}")
        return "Error loading data"

# Function to run `scraping.py`
def run_scraping_task():
    while True:
        print("Running scraping.py...")
        try:
            subprocess.run(["python", "scraping.py"], check=True)  # Run scraping.py
            print("scraping.py executed successfully.")
        except Exception as e:
            print(f"Error running scraping.py: {e}")
        time.sleep(300)  # Wait for 5 minutes (300 seconds) before running again

# Function to run Flask app
def run_flask_app():
    app.run(debug=True)

# Main Entry Point
if __name__ == "__main__":
    # Create and start a thread for scraping task
    scraping_thread = threading.Thread(target=run_scraping_task)
    scraping_thread.daemon = True  # Ensure it terminates when the main program exits
    scraping_thread.start()

    # Run the Flask app in the main thread
    print("Starting Flask app...")
    run_flask_app()

