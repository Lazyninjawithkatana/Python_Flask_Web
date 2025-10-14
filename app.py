from flask import Flask, render_template, session, url_for, redirect, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import psycopg2.errors
import database_const
import re

app = Flask(__name__)
# ეს უნდა იყოს ძლიერი, უნიკალური გასაღები
app.secret_key = 'jkhaksjhdkajshdkjsah13123kjahsd'

#Db connection
def db_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            host=database_const.HOST,
            user=database_const.USER,
            password=database_const.PASSWORD,
            database=database_const.NEW_DB_NAME
        )
        return conn
    except psycopg2.Error as e:
        print(f'[!] Error with {e}')
        return None

#Main page / Sign In
# დავამატე '/' როგორც მთავარი როუტი
@app.route('/', methods=['GET','POST'])
@app.route('/sign_in', methods=['GET','POST'])
def sign_in():
    conn = None
    cur = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Username and password are required.', 'error')
            return redirect(url_for('sign_in'))
        
        conn = db_connection()
        if not conn:
            flash('Database connection error', 'error')
            # შესწორებულია
            return redirect(url_for('sign_in'))
    
        sql = 'SELECT id, username, email, password FROM users WHERE username = %s'
        try:
            cur = conn.cursor()
            cur.execute(sql, (username,))
            user = cur.fetchone()
            
            if user:
                # user[0]: id, user[1]: username, user[2]: email, user[3]: password hash
                if check_password_hash(user[3], password): 
                    # სესიის ცვლადები შესწორებულია
                    session['user_id'] = user[0]
                    session['user_name'] = user[1] 
                    session['user_email'] = user[2]
                    flash('Login successful!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Invalid username or password.', 'error') 
            else:
                flash('Invalid username or password.', 'error') 
                
            return redirect(url_for('sign_in'))
            
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            flash('Database error during login. Please try again', 'error')
            return redirect(url_for('sign_in')) # შესწორებულია
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
    
    return render_template('main_page.html')

#Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        errors = []

        if not all([username, email, password, confirm_password]):
            errors.append('All fields are required.')
        if password != confirm_password:
            errors.append('Passwords do not match.') # შესწორებულია
        if len(password) < 8:
            errors.append('Password must be at least 8 characters long.')
        if not re.fullmatch(r'[^@]+@[^@]+\.[^@]+', email):
            errors.append('Invalid email format.')

        if errors:
            for msg in errors:
                flash(msg, 'error')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        sql = """
            INSERT INTO users (username, email, password)
            VALUES (%s, %s, %s)
        """
        conn = db_connection()
        if not conn:
            flash('Database connection error.', 'error')
            return redirect(url_for('register'))
        
        try:
            cur = conn.cursor()
            cur.execute(sql, (username, email, hashed_password))
            conn.commit()
            
            # შეტყობინება შესწორებულია
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('sign_in'))
            
        except psycopg2.IntegrityError:
            if conn:
                conn.rollback()
            # დავამატე Username-ის შემოწმებაც
            flash('Username or Email already exists.', 'error') 
            return redirect(url_for('register'))
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            flash('Database error during registration. Please try again.', 'error')
            return redirect(url_for('register'))
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
    
    # GET მოთხოვნა register-ზე აჩვენებს მთავარ გვერდს
    return render_template('main_page.html') 

#Dashboard page
# როუტი შესწორებულია
@app.route('/dashboard') 
def dashboard():
    if 'user_id' not in session:
        # Flash შეტყობინება შესწორებულია
        flash('Please log in to access the dashboard.', 'error') 
        return redirect(url_for('sign_in'))
    
    # ცვლადების ამოღება სესიიდან შესწორებულია
    username = session.get('user_name', 'Guest')
    email = session.get('user_email', 'No Email')
    
    # შაბლონის სახელი და ცვლადების გადაცემა შესწორებულია
    return render_template('dashboard_page.html', user_email=email, user_name=username)

# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_email', None)
    session.pop('user_name', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('sign_in'))

if __name__ == '__main__':
    app.run(debug=True)