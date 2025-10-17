from flask import Flask, render_template, request, redirect, url_for, session
import json
import pandas as pd
import plotly
import plotly.express as px
import folium
from functools import wraps

app = Flask(__name__)
app.secret_key = 'debug_app_2025'

print("🚀 STARTING DEBUG VERSION...")

# Sample data that DEFINITELY works
minerals_data = [
    {"MineralName": "Cobalt", "MarketPriceUSD_per_tonne": 75000},
    {"MineralName": "Lithium", "MarketPriceUSD_per_tonne": 25000},
    {"MineralName": "Graphite", "MarketPriceUSD_per_tonne": 1200},
    {"MineralName": "Manganese", "MarketPriceUSD_per_tonne": 1800}
]

countries_data = [
    {"CountryName": "South Africa", "MiningRevenue_BillionUSD": 55, "GDP_BillionUSD": 405},
    {"CountryName": "DRC Congo", "MiningRevenue_BillionUSD": 12, "GDP_BillionUSD": 58},
    {"CountryName": "Zambia", "MiningRevenue_BillionUSD": 8, "GDP_BillionUSD": 27},
    {"CountryName": "Zimbabwe", "MiningRevenue_BillionUSD": 3, "GDP_BillionUSD": 22}
]

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'admin123':
            session['user'] = {'username': 'admin', 'role': 'Admin'}
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard_debug.html', user=session['user'])

@app.route('/debug_analytics')
def debug_analytics():
    """SIMPLE analytics that DEFINITELY works"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    print("📊 DEBUG: Creating simple charts...")
    
    minerals_df = pd.DataFrame(minerals_data)
    countries_df = pd.DataFrame(countries_data)
    
    # Chart 1: Simple bar chart
    fig1 = px.bar(minerals_df, x='MineralName', y='MarketPriceUSD_per_tonne',
                 title='Mineral Prices', color='MineralName')
    chart1_html = fig1.to_html(include_plotlyjs='cdn')
    
    # Chart 2: Simple bar chart  
    fig2 = px.bar(countries_df, x='CountryName', y='MiningRevenue_BillionUSD',
                 title='Mining Revenue', color='CountryName')
    chart2_html = fig2.to_html(include_plotlyjs=False)
    
    return f"""
    <html>
    <head><title>Debug Analytics</title></head>
    <body>
        <h1>Debug Analytics - Charts Should Work</h1>
        {chart1_html}
        {chart2_html}
    </body>
    </html>
    """

@app.route('/debug_map')
def debug_map():
    """SIMPLE map that DEFINITELY works"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    print("🗺️ DEBUG: Creating simple map...")
    
    # Create a very basic map
    m = folium.Map(location=[-25, 25], zoom_start=4)
    
    # Add a few test markers
    folium.Marker([-25, 25], popup='South Africa').add_to(m)
    folium.Marker([-10, 25], popup='DRC Congo').add_to(m)
    folium.Marker([-20, 30], popup='Zimbabwe').add_to(m)
    
    return m.get_root().render()

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    print("✅ DEBUG APP READY!")
    app.run(debug=True, host='127.0.0.1', port=5000)