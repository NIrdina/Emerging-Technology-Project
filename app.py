from flask import Flask, render_template, redirect, url_for, session, request
from werkzeug.security import generate_password_hash, check_password_hash  # For password hashing

app = Flask(__name__)
app.secret_key = 'OGQ0ODc2ZjMtMTNhOS00Yzk4LTlhMmUtZTZhZWFlOGYyNjQyMDE0Nzk0YzAtYmMy_P0A1_955b0110-97b0-4717-a284-c57ffbc138a4'  # Replace with a real secret key


users = {
    "user@example.com": generate_password_hash("password123") 
}

@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html')  
    return redirect(url_for('login'))  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Validate the credentials using hashed password comparison
        if email in users and check_password_hash(users[email], password):
            session['user_id'] = email  
            return redirect(url_for('index'))  # Redirect to the main page after login
        else:
            return render_template('login.html', error="Invalid email or password")
    
    return render_template('login.html')  # Show the login form

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if the email already exists in the users dictionary 
        if email in users:
            return render_template('signup.html', error="Email already exists")
        
        # Hash the password before saving 
        hashed_password = generate_password_hash(password)
        
        # Save the new user 
        users[email] = hashed_password
        
        return redirect(url_for('login'))  # Redirect to login after successful signup
    
    return render_template('signup.html') 

@app.route('/logout')
def logout():
    session.pop('user_id', None)  
    return redirect(url_for('login'))  # Redirect to login page after logout

if __name__ == '__main__':
    app.run(debug=True)
