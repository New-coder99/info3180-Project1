"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

import uuid

import psycopg2
from app import app
from flask import Flask, flash, render_template, request, redirect, url_for
from wtforms import StringField, SelectField, TextAreaField, FileField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
import os


###
# Routing for your application.
###

def get_db_connection():
    conn = psycopg2.connect(
        dbname="info3180project1",
        user="postgres",
        password="chickenback",
        host="localhost",
        port="5432"  # Default PostgreSQL port
    )
    return conn


# Define your routes
@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Jonoi Graham")







@app.route('/properties/create',methods=['GET','POST'])
def create_prop():
    if request.method=='GET':
        return render_template('create_property.html')
    if request.method=='POST':
        title = request.form.get('title')
        bedrooms = request.form.get('bedrooms')
        bathrooms = request.form.get('bathrooms')
        location = request.form.get('location')
        price = request.form.get('price')
        prop_type = request.form.get('type')
        description = request.form.get('description')
        photo_data=request.form.get('photo')
        conn = get_db_connection()
        cursor = conn.cursor()
        insert_query = """
    INSERT INTO properties (title, bedrooms, bathrooms, location, price, type, description, photo)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""
        cursor.execute(insert_query, (title, bedrooms, bathrooms, location, price, prop_type, description, photo_data))
        conn.commit()
        conn.close()
        return redirect(url_for('prop_list'))










@app.route('/properties/<int:property_id>',methods=['GET'])
def prop_det(property_id):
    
    conn = get_db_connection()
    
    cur = conn.cursor()

    
    cur.execute("SELECT title, bedrooms, bathrooms, location, price, type, description, photo FROM properties WHERE id = %s", (property_id,))
    property_details = cur.fetchone()

   
    cur.close()
    conn.close()

   
    if property_details:
       
        title = property_details[0]
        bedrooms = property_details[1]
        bathrooms = property_details[2]
        location = property_details[3]
        price = property_details[4]
        prop_type = property_details[5]
        description = property_details[6]
        photo_data = property_details[7]
        return render_template('property_details.html',title=title, bedrooms=bedrooms,bathrooms=bathrooms, location=location,  price=price, prop_type=prop_type, description=description, photo=photo_data)
    else:
        
        return "Property not found"


@app.route('/properties/')
def prop_list():
    # Connect to the PostgreSQL database
    conn = get_db_connection()
    cur = conn.cursor()

    # Execute a query to fetch all properties
    cur.execute("SELECT * FROM properties")

    # Fetch all rows
    properties = cur.fetchall()

    # Close cursor and connection
    cur.close()
    conn.close()

    # Pass the properties to the template for rendering
    return render_template('property_list.html', properties=properties)