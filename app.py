from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
import os
from werkzeug.utils import secure_filename
import numpy as np
import pickle

# Initialize Flask App
app = Flask(__name__)
app.secret_key = '12345y78'


users = {}




# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Home Page After Login
@app.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html', user=session['user'])
    return redirect(url_for('login'))

#Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if email in users and users[email] == password:
            session['user'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password!', 'danger')
    
    return render_template('login.html')

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
        elif email in users:
            flash('Email is already registered!', 'warning')
        else:
            users[email] = password
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')


with open('Grid_Model1.pkl', 'rb') as file:  # Open in binary mode
    knn_model = pickle.load(file)

# Performance Page After Login
@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if 'user' in session:
        if request.method == 'POST':
            try:
                # Extract form data
                location = float(request.form['location'])  # Dropdown value
                year = float(request.form['time'])         # Dropdown value
                mri_units = float(request.form['mri_units'])  # Text input
                ct_scanners = float(request.form['ct_scanners'])  # Text input
                hospital_beds = float(request.form['hospital_beds'])  # Text input

                # Prepare the input for prediction
                features = np.array([[location, year, mri_units, ct_scanners, hospital_beds]])

                # Make prediction
                prediction_result = knn_model.predict(features)[0]
                print("Prediction: ", prediction_result)

                # Render the result page with prediction
                return render_template('result.html', 
                                       user=session['user'], 
                                       prediction=prediction_result)

            except Exception as e:
                # Handle errors (e.g., invalid input types)
                return render_template('prediction.html', 
                                       user=session['user'], 
                                       error=f"An error occurred: {e}")
        # Render the prediction form on GET request
        return render_template('prediction.html', user=session['user'])
    return redirect(url_for('login'))

# Performance Page After Login
@app.route('/performance')
def performance():
    if 'user' in session:
        return render_template('performance.html', user=session['user'])
    return redirect(url_for('login'))

# Charts Page After Login
@app.route('/charts')
def charts():
    if 'user' in session:
        return render_template('charts.html', user=session['user'])
    return redirect(url_for('login'))


# Logout Route
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out!', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
