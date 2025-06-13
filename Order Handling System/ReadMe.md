Order Handling System using Flask on Google Colab
This project implements a Flask-based backend application for managing orders, including adding, editing, marking as delivered, deleting orders, and logging actions. The application is styled with Tailwind CSS for a clean and professional interface and is designed to run on Google Colab.
Prerequisites

Google Colab account
Internet connection
Basic familiarity with Python and Flask

Setup Instructions

Open Google Colab

Go to Google Colab and create a new notebook.


Install Required Packages

Run the following command in a Colab cell to install Flask and pyngrok:!pip install flask pyngrok




Set Up pyngrok for Public URL

Sign up for a free account at ngrok.com to obtain an authtoken.
In a Colab cell, set your ngrok authtoken:!ngrok authtoken YOUR_NGROK_AUTH_TOKEN

Replace YOUR_NGROK_AUTH_TOKEN with your actual ngrok authtoken.


Create the Application Files

Create a directory named templates in your Colab workspace and add the following files:
app.py: Main Flask application.
templates/index.html: HTML template for displaying orders and logs.
templates/add.html: HTML template for adding orders.
templates/edit.html: HTML template for editing orders.


Use the following commands in separate Colab cells to write each file:%%writefile app.py
# Paste the contents of app.py here

%%writefile templates/index.html
# Paste the contents of index.html here

%%writefile templates/add.html
# Paste the contents of add.html here

%%writefile templates/edit.html
# Paste the contents of edit.html here




Run the Flask Application

Use the following code in a Colab cell to start the Flask application and create a public URL with pyngrok:from pyngrok import ngrok
import os

# Create templates directory
os.makedirs('templates', exist_ok=True)

# Start ngrok tunnel on port 5000
public_url = ngrok.connect(5000)
print(f"Public URL: {public_url}")

# Run Flask app
!python app.py


After running, note the public URL provided by pyngrok (e.g., http://<random>.ngrok.io). This URL allows you to access the application in your browser.


Access the Application

Open the pyngrok public URL in your browser to interact with the order management system.
Use the web interface to add, edit, mark as delivered, or delete orders.
Action logs are displayed below the orders table in the main view.



Features

Add New Order: Create orders with unique IDs, number of items, delivery date, sender name, recipient name, recipient address, and default "Ongoing" status.
Edit Order: Modify details of existing orders.
Mark as Delivered: Change order status to "Delivered".
Delete Order: Remove orders from the system.
Action Logs: Log all actions (Created, Edited, Marked Delivered, Deleted) with action type, performed by, timestamp, and order ID.
Display Orders: View all orders and their statuses in a styled HTML table.

Styling

The interface uses Tailwind CSS for a clean and professional look:
Responsive tables with hover effects, alternating row colors, and scrollable overflow.
Centered forms with consistent padding, focus states, and modern input styles.
Color-coded status indicators (yellow for Ongoing, green for Delivered).
Buttons and links with smooth hover transitions for enhanced interactivity.


Tailwind CSS is included via CDN, requiring no additional setup.

Database

Uses SQLite (orders.db) to store orders and action logs.
Tables:
orders: Stores order details (order_id, num_items, delivery_date, sender_name, recipient_name, recipient_address, status).
action_logs: Stores action logs (id, action_type, performed_by, timestamp, order_id).



Notes

The application uses "Admin" as a placeholder for performed_by in action logs, as authentication is not required.
The pyngrok tunnel must remain active during testing; it may disconnect if the Colab session is idle for too long.
The SQLite database (orders.db) is stored in the Colab runtime and will be lost when the session ends. To persist data, download the orders.db file from Colab or use an external database.
Order IDs are truncated in the UI (first 8 characters) for readability but stored in full in the database.

Troubleshooting

Port Conflict: If Flask fails to bind to port 5000, restart the Colab runtime and rerun all cells.
pyngrok Errors: Ensure your pyngrok authtoken is valid. Free accounts may hit connection limits.
Template Not Found: Verify that the templates/ directory contains index.html, add.html, and edit.html.
Styling Issues: Ensure the Tailwind CSS CDN is accessible; an internet connection is required for the CDN to load.

