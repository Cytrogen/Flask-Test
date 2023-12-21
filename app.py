import sqlite3

from flask import Flask, render_template, request, redirect

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True


def get_db():
    """
    Get database connection.
    :return:
    """

    db = sqlite3.connect('test.db')

    # Uncomment this block to create a new table and insert a demo record
    # with db:
    #     db.execute('''CREATE TABLE IF NOT EXISTS chat(
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     is_user INTEGER NOT NULL,
    #     message TEXT NOT NULL);''')
    #     db.execute('INSERT INTO chat(is_user, message) VALUES (0, ?)', ('Hello, this is a demo page.',))
    #     db.commit()
    return db


# This route is for demo purpose only
# GET -> normally used to get data from server
# POST -> normally used to send data to server
@app.route('/', methods=['GET', 'POST'])
def test():
    db = get_db()
    cur = db.cursor()

    # Handle POST request
    if request.method == 'POST':
        # Check if user input is empty. If so, redirect to the same page -> do nothing
        if not request.form.get('text-area'):
            return redirect('/')

        # Get user input
        user_message = request.form.get('text-area')

        # Insert user input into database
        cur.execute(f'INSERT INTO chat (is_user, message) VALUES (?, ?)', (1, user_message))
        # Repeat. Insert bot response into database
        # This part can be changed to connect to the model
        cur.execute(f'INSERT INTO chat (is_user, message) VALUES (?, ?)', (0, user_message))
        db.commit()

        return redirect('/')

    # Handle GET request
    # Get all records from database
    records = cur.execute('SELECT * FROM chat ORDER BY id').fetchall()
    print(records)
    return render_template('layout.html', records=records)


if __name__ == '__main__':
    app.run(debug=True)
