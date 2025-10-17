from flask import Flask, render_template, request, redirect, url_for, session
import json
import pandas as pd
import plotly
import plotly.express as px
import folium
from functools import wraps
import os  # ← ADD THIS IMPORT

app = Flask(__name__)
app.secret_key = 'chrono_minerals_final_2025'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

print("🚀 CHRONO MINERALS - FINAL WORKING VERSION")

# ==================== LOAD DATA FROM CSV FILES ====================
def load_csv_data(filename):
    """Generic function to load CSV data"""
    try:
        csv_path = os.path.join('data', filename)
        df = pd.read_csv(csv_path)
        print(f"✅ Loaded {len(df)} records from {filename}")
        return df.to_dict('records')
    except FileNotFoundError:
        print(f"❌ {filename} not found - using sample data")
        return []

# Load all data from CSV files
minerals_data = load_csv_data('minerals.csv')
countries_data = load_csv_data('countries.csv') 
production_data = load_csv_data('production_stats.csv')
sites_data = load_csv_data('sites.csv')

# Load all data from CSV files
minerals_data = load_csv_data('minerals.csv')
countries_data = load_csv_data('countries.csv') 
production_data = load_csv_data('production_stats.csv')
sites_data = load_csv_data('sites.csv')

# If CSV files are empty, use your sample data as fallback
if not minerals_data:
    minerals_data = [
        {"MineralID": 1, "MineralName": "Cobalt", "Description": "Used in batteries and superalloys", "MarketPriceUSD_per_tonne": 75000},
        {"MineralID": 2, "MineralName": "Lithium", "Description": "Essential for lithium-ion batteries", "MarketPriceUSD_per_tonne": 25000},
        {"MineralID": 3, "MineralName": "Graphite", "Description": "Used in batteries and lubricants", "MarketPriceUSD_per_tonne": 1200},
        {"MineralID": 4, "MineralName": "Manganese", "Description": "Used in steel production and batteries", "MarketPriceUSD_per_tonne": 1800},
        {"MineralID": 5, "MineralName": "Platinum", "Description": "Used in catalytic converters and fuel cells", "MarketPriceUSD_per_tonne": 32000},
        {"MineralID": 6, "MineralName": "Chromium", "Description": "Essential for stainless steel production", "MarketPriceUSD_per_tonne": 9500}
    ]

# ==================== ADD LOCAL IMAGES TO MINERALS ====================
# Map mineral names to your local JPEG image files
mineral_images = {
    "Cobalt": "cobalt.jpeg",
    "Lithium": "lithium.jpeg", 
    "Graphite": "graphite.jpeg",
    "Manganese": "manganese.jpeg",
    "Platinum": "platinum.jpeg",
    "Chromium": "chromium.jpeg"
}

# Add image filenames to each mineral
print("🖼️ Assigning mineral images:")
for mineral in minerals_data:
    mineral_name = mineral['MineralName']
    image_file = mineral_images.get(mineral_name, 'default.jpeg')
    mineral['Image'] = image_file
    print(f"   {mineral_name} → {image_file}")

print("✅ Mineral images assigned")

if not countries_data:
    countries_data = [
        {"CountryID": 1, "CountryName": "South Africa", "GDP_BillionUSD": 405, "MiningRevenue_BillionUSD": 55, "KeyProjects": "Bushveld Complex PGM mines, Kalahari Manganese Field"},
        {"CountryID": 2, "CountryName": "Democratic Republic of Congo", "GDP_BillionUSD": 58, "MiningRevenue_BillionUSD": 12, "KeyProjects": "Cobalt and copper mines in Katanga region"},
        {"CountryID": 3, "CountryName": "Zambia", "GDP_BillionUSD": 27, "MiningRevenue_BillionUSD": 8, "KeyProjects": "Copperbelt mining operations"},
        {"CountryID": 4, "CountryName": "Zimbabwe", "GDP_BillionUSD": 22, "MiningRevenue_BillionUSD": 3, "KeyProjects": "Great Dyke platinum and chrome mines"},
        {"CountryID": 5, "CountryName": "Namibia", "GDP_BillionUSD": 12, "MiningRevenue_BillionUSD": 2, "KeyProjects": "Uis tin mine, Rossing uranium mine"}
    ]

# ==================== AUTHENTICATION ====================
users_data = [
    {"username": "admin01", "password": "admin123", "role": "administrator"},
    {"username": "investor01", "password": "invest123", "role": "investor"}, 
    {"username": "researcher01", "password": "research123", "role": "researcher"}
]
# ==================== ROLE-BASED ACCESS CONTROL ====================
def role_required(required_roles):
    """Decorator to check if user has required role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session:
                return redirect(url_for('login'))
            
            user_role = session['user'].get('role')  # Get role from user session
            if user_role not in required_roles:
                return redirect(url_for('dashboard'))  # Or show access denied page
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Define role permissions
ADMIN_ROLES = ['administrator']
RESEARCHER_ROLES = ['administrator', 'researcher']  
INVESTOR_ROLES = ['administrator', 'investor']
ALL_ROLES = ['administrator', 'researcher', 'investor']

# ==================== ROUTES ====================
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        for user in users_data:
            # Direct comparison - no CSV complications
            if user['username'] == username and user['password'] == password:
                session['user'] = user
                print(f"✅ Login successful: {username} as {user['role']}")
                return redirect(url_for('dashboard'))
        
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
@role_required(ALL_ROLES)  # All roles can access dashboard
def dashboard():
    user = session['user']
    
    # Calculate stats
    stats = {
        'total_minerals': len(minerals_data),
        'total_countries': len(countries_data),
        'total_sites': 12,  # Hardcoded for demo
        'avg_price': f"${sum(m['MarketPriceUSD_per_tonne'] for m in minerals_data) // len(minerals_data):,}"
    }
    
    return render_template('dashboard_final.html', user=user, stats=stats)

@app.route('/minerals')
@login_required  
@role_required(RESEARCHER_ROLES)  # Only researchers and admin
def minerals():
    user = session['user']
    return render_template('minerals_final.html', user=user, minerals=minerals_data)

@app.route('/countries')
@login_required
@role_required(ALL_ROLES)  # All roles can access countries
def countries():
    user = session['user']
    return render_template('countries_final.html', user=user, countries=countries_data)

@app.route('/analytics')
@login_required
@role_required(RESEARCHER_ROLES)
def analytics():
    user = session['user']
    
    print("📊 Creating interactive charts...")
    
    # Convert to DataFrames
    minerals_df = pd.DataFrame(minerals_data)
    countries_df = pd.DataFrame(countries_data)
    production_df = pd.DataFrame(production_data)
    sites_df = pd.DataFrame(sites_data)
    
    # Chart 1: Mineral Prices (Original)
    price_chart = px.bar(
        minerals_df, 
        x='MineralName', 
        y='MarketPriceUSD_per_tonne',
        title='💎 Critical Mineral Prices (USD per tonne)',
        color='MineralName',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    price_html = price_chart.to_html(include_plotlyjs='cdn')
    
    # Chart 2: Country Revenue (Original)
    revenue_chart = px.bar(
        countries_df,
        x='CountryName', 
        y='MiningRevenue_BillionUSD',
        title='🌍 Mining Revenue by Country (Billion USD)',
        color='CountryName'
    )
    revenue_html = revenue_chart.to_html(include_plotlyjs=False)
    
    # Chart 3: GDP vs Revenue (Original)
    gdp_chart = px.scatter(
        countries_df,
        x='GDP_BillionUSD', 
        y='MiningRevenue_BillionUSD',
        size='MiningRevenue_BillionUSD',
        color='CountryName',
        title='📊 GDP vs Mining Revenue Relationship',
        hover_name='CountryName',
        size_max=60
    )
    gdp_html = gdp_chart.to_html(include_plotlyjs=False)
    
    # NEW CHART 4: Production Trends by Country
    if not production_df.empty and not countries_df.empty and not minerals_df.empty:
        # Merge data for production trends
        merged_line = production_df.merge(
            minerals_df[['MineralID', 'MineralName']], on='MineralID', how='left'
        ).merge(
            countries_df[['CountryID', 'CountryName']], on='CountryID', how='left'
        )
        
        production_trends = px.line(
            merged_line,
            x='Year',
            y='Production_tonnes',
            color='CountryName',
            markers=True,
            title='📈 Production Trends by Country',
            template='plotly_white'
        )
        production_trends.update_yaxes(tick0=0, dtick=20000, title_text="Production (tonnes)")
        production_trends_html = production_trends.to_html(include_plotlyjs=False)
    else:
        production_trends_html = "<p>No production trend data available</p>"
    
    # NEW CHART 5: Mineral Price Distribution
    price_distribution = px.box(
        minerals_df,
        x="MarketPriceUSD_per_tonne",
        hover_data=["MineralName", "Description"],
        points="all",
        title="📦 Distribution of Mineral Market Prices"
    )
    price_distribution.update_traces(marker_color="teal", boxmean=True)
    price_distribution.update_layout(
        xaxis_title="Market Price (USD per tonne)",
        yaxis_title="",
        template="plotly_white"
    )
    price_distribution_html = price_distribution.to_html(include_plotlyjs=False)
    
    # NEW CHART 6: Export Value vs Market Price
    if not production_df.empty:
        merged_export = production_df.merge(
            minerals_df[['MineralID', 'MineralName', 'MarketPriceUSD_per_tonne']], 
            on='MineralID', how='left'
        )
        
        export_vs_price = px.scatter(
            merged_export,
            x='MarketPriceUSD_per_tonne',
            y='ExportValue_BillionUSD',
            color='MineralName',
            hover_name='MineralName',
            title='💰 Export Value vs Market Price',
            size='ExportValue_BillionUSD',
            size_max=30,
            template='plotly_white'
        )
        export_vs_price.update_layout(
            xaxis_title='Market Price (USD per tonne)',
            yaxis_title='Export Value (Billion USD)'
        )
        export_vs_price_html = export_vs_price.to_html(include_plotlyjs=False)
    else:
        export_vs_price_html = "<p>No export data available</p>"
    
    # NEW CHART 7: Production vs Market Price
    if not production_df.empty:
        production_vs_price = px.scatter(
            merged_export,
            x='Production_tonnes',
            y='MarketPriceUSD_per_tonne',
            color='MineralName',
            hover_name='MineralName',
            title='⚖️ Market Price vs Production Volume',
            size='ExportValue_BillionUSD',
            size_max=30,
            template='plotly_white'
        )
        production_vs_price.update_layout(
            xaxis_title='Production (tonnes)',
            yaxis_title='Market Price (USD per tonne)'
        )
        production_vs_price_html = production_vs_price.to_html(include_plotlyjs=False)
    else:
        production_vs_price_html = "<p>No production data available</p>"
    
    # NEW CHART 8: Average Export Value by Mineral
    if not production_df.empty:
        avg_export = production_df.groupby('MineralID', as_index=False)['ExportValue_BillionUSD'].mean()
        avg_export = avg_export.merge(
            minerals_df[['MineralID', 'MineralName']], on='MineralID', how='left'
        )
        
        avg_export_chart = px.bar(
            avg_export.sort_values(by='ExportValue_BillionUSD', ascending=False),
            x='MineralName',
            y='ExportValue_BillionUSD',
            text='ExportValue_BillionUSD',
            title='📊 Average Export Value by Mineral',
            color='ExportValue_BillionUSD',
            color_continuous_scale='Viridis',
            template='plotly_white'
        )
        avg_export_chart.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        avg_export_chart.update_layout(
            xaxis_title='Mineral',
            yaxis_title='Average Export Value (Billion USD)',
            xaxis_tickangle=-45
        )
        avg_export_html = avg_export_chart.to_html(include_plotlyjs=False)
    else:
        avg_export_html = "<p>No export data available</p>"
    
    return render_template('analytics_final.html', user=user,
                         price_html=price_html,
                         revenue_html=revenue_html, 
                         gdp_html=gdp_html,
                         production_trends_html=production_trends_html,
                         price_distribution_html=price_distribution_html,
                         export_vs_price_html=export_vs_price_html,
                         production_vs_price_html=production_vs_price_html,
                         avg_export_html=avg_export_html)

@app.route('/interactive_map')
@login_required
@role_required(ALL_ROLES)  # All roles can access map
def interactive_map():
    """Interactive map with mineral deposits - WORKING VERSION"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    print("🗺️ Creating interactive map...")
    
    try:
        # Create map centered on Southern Africa
        m = folium.Map(
            location=[-15, 25], 
            zoom_start=4,
            tiles='OpenStreetMap'
        )
        
        # COUNTRY MARKERS (Flags)
        countries = [
            ([-30.5595, 22.9375], 'South Africa', '$405B', '$55B'),
            ([-2.8, 23.7], 'DRC Congo', '$58B', '$12B'),
            ([-22.6, 17.1], 'Namibia', '$12B', '$2B'),
            ([-18.6, 35.5], 'Mozambique', '$20B', '$4B'),
            ([-13.5, 27.8], 'Zambia', '$27B', '$8B'),
            ([-19.0, 29.0], 'Zimbabwe', '$22B', '$3B')
        ]
        
        for location, country, gdp, revenue in countries:
            folium.Marker(
                location=location,
                popup=f'<b>{country}</b><br>GDP: {gdp}<br>Mining Revenue: {revenue}',
                tooltip=country,
                icon=folium.Icon(color='red', icon='flag')
            ).add_to(m)
        
        # MINERAL DEPOSITS (Circles)
        minerals = [
            ([-24.5, 28.5], 'blue', 'Waterberg Lithium', 'Lithium', '40,000 tonnes'),
            ([-25.0, 28.0], 'purple', 'Bushveld PGMs', 'Platinum', '250,000 tonnes'),
            ([-10.7, 25.5], 'darkblue', 'Kolwezi Cobalt', 'Cobalt', '95,000 tonnes'),
            ([-22.0, 17.2], 'brown', 'Otjozondu Manganese', 'Manganese', '30,000 tonnes'),
            ([-13.3, 38.2], 'gray', 'Balama Graphite', 'Graphite', '12,000 tonnes'),
            ([-12.5, 27.5], 'orange', 'Copperbelt Mines', 'Copper', '800,000 tonnes')
        ]
        
        for location, color, name, mineral, production in minerals:
            folium.CircleMarker(
                location=location,
                radius=10,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
                popup=f'<b>{name}</b><br>Mineral: {mineral}<br>Production: {production}',
                tooltip=f"{mineral} Deposit"
            ).add_to(m)
        
        # Convert map to HTML
        map_html = m._repr_html_()
        print("✅ Map created successfully")
        
        user = session['user']
        return render_template('map.html', user=user, map_html=map_html)
        
    except Exception as e:
        print(f"❌ Map Error: {e}")
        return f"<h1>Map Error</h1><p>{e}</p>"

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# ==================== ADMIN DATA MANAGEMENT ROUTES ====================

@app.route('/admin/minerals', methods=['GET', 'POST'])
@login_required
@role_required(ADMIN_ROLES)
def admin_minerals():
    """Admin panel to manage minerals data"""
    user = session['user']
    
    if request.method == 'POST':
        # Add new mineral
        new_mineral = {
            "MineralID": len(minerals_data) + 1,
            "MineralName": request.form['mineral_name'],
            "Description": request.form['description'],
            "MarketPriceUSD_per_tonne": int(request.form['price'])
        }
        minerals_data.append(new_mineral)
        
        # ✅ UPDATED: Save to CSV in data folder
        df = pd.DataFrame(minerals_data)
        csv_path = os.path.join('data', 'minerals.csv')  # Save to your data folder
        df.to_csv(csv_path, index=False)
        print(f"✅ Updated minerals.csv with {len(minerals_data)} records")
        
        return redirect(url_for('admin_minerals'))
    
    return render_template('admin_minerals.html', user=user, minerals=minerals_data)

@app.route('/admin/countries', methods=['GET', 'POST'])
@login_required
@role_required(ADMIN_ROLES)
def admin_countries():
    """Admin panel to manage countries data"""
    user = session['user']
    
    if request.method == 'POST':
        # Add new country
        new_country = {
            "CountryID": len(countries_data) + 1,
            "CountryName": request.form['country_name'],
            "GDP_BillionUSD": int(request.form['gdp']),
            "MiningRevenue_BillionUSD": int(request.form['revenue']),
            "KeyProjects": request.form['projects']
        }
        countries_data.append(new_country)
        
        # ✅ UPDATED: Save to CSV in data folder
        df = pd.DataFrame(countries_data)
        csv_path = os.path.join('data', 'countries.csv')  # Save to your data folder
        df.to_csv(csv_path, index=False)
        print(f"✅ Updated countries.csv with {len(countries_data)} records")
        
        return redirect(url_for('admin_countries'))
    
    return render_template('admin_countries.html', user=user, countries=countries_data)

@app.route('/admin/delete_mineral/<int:mineral_id>')
@login_required
@role_required(ADMIN_ROLES)
def delete_mineral(mineral_id):
    """Delete a mineral (admin only)"""
    global minerals_data
    minerals_data = [m for m in minerals_data if m['MineralID'] != mineral_id]
    
    # ✅ UPDATED: Also update the CSV file
    df = pd.DataFrame(minerals_data)
    csv_path = os.path.join('data', 'minerals.csv')
    df.to_csv(csv_path, index=False)
    print(f"✅ Updated minerals.csv after deletion - {len(minerals_data)} records remain")
    
    return redirect(url_for('admin_minerals'))

@app.route('/admin/delete_country/<int:country_id>')
@login_required
@role_required(ADMIN_ROLES)
def delete_country(country_id):
    """Delete a country (admin only)"""
    global countries_data
    countries_data = [c for c in countries_data if c['CountryID'] != country_id]
    
    # ✅ UPDATED: Also update the CSV file
    df = pd.DataFrame(countries_data)
    csv_path = os.path.join('data', 'countries.csv')
    df.to_csv(csv_path, index=False)
    print(f"✅ Updated countries.csv after deletion - {len(countries_data)} records remain")
    
    return redirect(url_for('admin_countries'))

if __name__ == '__main__':
    print("✅ CHRONO MINERALS - READY FOR SUBMISSION!")
    print("👤 Demo accounts: admin01/admin123, investor01/invest123, researcher01/research123")
    print("🌐 Open: http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)