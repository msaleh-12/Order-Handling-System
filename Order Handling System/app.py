from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime
import sqlite3
import uuid

app = Flask(__name__)

# Initialize database
def init_db():
    with sqlite3.connect('orders.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            num_items INTEGER,
            delivery_date TEXT,
            sender_name TEXT,
            recipient_name TEXT,
            recipient_address TEXT,
            status TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS action_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_type TEXT,
            performed_by TEXT,
            timestamp TEXT,
            order_id TEXT,
            FOREIGN KEY(order_id) REFERENCES orders(order_id)
        )''')
        conn.commit()

# Helper function to log actions
def log_action(action_type, performed_by, order_id):
    with sqlite3.connect('orders.db') as conn:
        c = conn.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute('INSERT INTO action_logs (action_type, performed_by, timestamp, order_id) VALUES (?, ?, ?, ?)',
                  (action_type, performed_by, timestamp, order_id))
        conn.commit()

# Home route to display orders
@app.route('/')
def index():
    with sqlite3.connect('orders.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM orders')
        orders = c.fetchall()
        c.execute('SELECT * FROM action_logs ORDER BY timestamp DESC')
        logs = c.fetchall()
    return render_template('index.html', orders=orders, logs=logs)

# Add new order
@app.route('/add', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        order_id = str(uuid.uuid4())
        num_items = request.form['num_items']
        delivery_date = request.form['delivery_date']
        sender_name = request.form['sender_name']
        recipient_name = request.form['recipient_name']
        recipient_address = request.form['recipient_address']
        status = 'Ongoing'
        performed_by = 'Admin'  # Placeholder for user authentication

        with sqlite3.connect('orders.db') as conn:
            c = conn.cursor()
            c.execute('INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?)',
                      (order_id, num_items, delivery_date, sender_name, recipient_name, recipient_address, status))
            conn.commit()
        
        log_action('Created', performed_by, order_id)
        return redirect(url_for('index'))
    return render_template('add.html')

# Edit order
@app.route('/edit/<order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    if request.method == 'POST':
        num_items = request.form['num_items']
        delivery_date = request.form['delivery_date']
        sender_name = request.form['sender_name']
        recipient_name = request.form['recipient_name']
        recipient_address = request.form['recipient_address']
        performed_by = 'Admin'

        with sqlite3.connect('orders.db') as conn:
            c = conn.cursor()
            c.execute('UPDATE orders SET num_items=?, delivery_date=?, sender_name=?, recipient_name=?, recipient_address=? WHERE order_id=?',
                      (num_items, delivery_date, sender_name, recipient_name, recipient_address, order_id))
            conn.commit()
        
        log_action('Marked Delivered', performed_by, order_id)
        return redirect(url_for('index'))
    
    with sqlite3.connect('orders.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM orders WHERE order_id=?', (order_id,))
        order = c.fetchone()
    return render_template('edit.html', order=order)

# Mark order as delivered
@app.route('/deliver/<order_id>')
def mark_delivered(order_id):
    performed_by = 'Admin'
    with sqlite3.connect('orders.db') as conn:
        c = conn.cursor()
        c.execute('UPDATE orders SET status="Delivered" WHERE order_id=?', (order_id,))
        conn.commit()
    
    log_action('Marked Delivered', performed_by, order_id)
    return redirect(url_for('index'))

# Delete order
@app.route('/delete/<order_id>')
def delete_order(order_id):
    performed_by = 'Admin'
    with sqlite3.connect('orders.db') as conn:
        c = conn.cursor()
        c.execute('DELETE FROM orders WHERE order_id=?', (order_id,))
        conn.commit()
    
    log_action('Deleted', performed_by, order_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)