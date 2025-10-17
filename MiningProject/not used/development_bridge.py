# DEVELOPMENT BRIDGE - For easy code transfer from Colab
import folium
import pandas as pd
import plotly.express as px
import json

print("🧪 DEVELOPMENT BRIDGE - Testing Colab Code Locally")
print("=================================================")

def test_colab_map_creation():
    """TEST YOUR ACTUAL COLAB MAP CODE"""
    print("\n🗺️ Testing Colab Map Creation...")
    
    try:
        # PASTE YOUR ACTUAL COLAB MAP CODE HERE
        countries_map = pd.DataFrame({
            'Country': ['South Africa', 'DRC (Congo)', 'Namibia', 'Mozambique', 'Zambia', 'Zimbabwe'],
            'Latitude': [-30.5595, -2.8, -22.6, -18.6, -13.5, -19.0],
            'Longitude': [22.9375, 23.7, 17.1, 35.5, 27.8, 29.0],
            'GDP_BillionUSD': [350, 55, 15, 20, 27, 22],
            'MiningRevenue_BillionUSD': [25, 12, 3, 4, 8, 3],
        })

        deposits = pd.DataFrame({
            'Country': ['South Africa', 'South Africa', 'DRC (Congo)', 'Namibia', 'Mozambique', 'Zambia'],
            'DepositName': ['Waterberg Lithium', 'Bushveld PGMs', 'Kolwezi Cobalt', 'Otjozondu Manganese', 'Balama Graphite', 'Copperbelt Mines'],
            'Mineral': ['Lithium', 'Platinum', 'Cobalt', 'Manganese', 'Graphite', 'Copper'],
            'Latitude': [-24.5, -25.0, -10.7, -22.0, -13.3, -12.5],
            'Longitude': [28.5, 28.0, 25.5, 17.2, 38.2, 27.5],
            'Production_tonnes': [40000, 250000, 95000, 30000, 12000, 800000]
        })

        mineral_colors = {
            'Lithium': 'blue', 'Cobalt': 'darkblue', 'Manganese': 'brown', 
            'Graphite': 'gray', 'Platinum': 'purple', 'Copper': 'orange'
        }

        # Create the map
        map_center = [-10, 25]
        m = folium.Map(location=map_center, zoom_start=3, tiles='cartodb positron')

        # Add country markers
        for _, row in countries_map.iterrows():
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=f"<h4>{row['Country']}</h4><b>GDP:</b> ${row['GDP_BillionUSD']}B<br><b>Mining Revenue:</b> ${row['MiningRevenue_BillionUSD']}B",
                icon=folium.Icon(color='darkblue', icon='flag')
            ).add_to(m)

        # Add mineral deposits
        for _, row in deposits.iterrows():
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=8,
                color=mineral_colors.get(row['Mineral'], 'green'),
                fill=True,
                fill_color=mineral_colors.get(row['Mineral'], 'green'),
                fill_opacity=0.7,
                popup=f"<b>{row['DepositName']}</b><br><b>Mineral:</b> {row['Mineral']}<br><b>Production:</b> {row['Production_tonnes']:,} tonnes"
            ).add_to(m)

        # Test HTML conversion (what Flask needs)
        map_html = m.get_root().render()
        
        print("✅ Colab Map Test: PASSED!")
        print(f"   - Created map with {len(countries_map)} countries")
        print(f"   - Added {len(deposits)} mineral deposits")
        print(f"   - HTML generated successfully")
        return True
        
    except Exception as e:
        print(f"❌ Colab Map Test: FAILED - {e}")
        return False

def test_colab_charts():
    """TEST YOUR ACTUAL COLAB CHART CODE"""
    print("\n📊 Testing Colab Charts...")
    
    try:
        # Your chart data
        minerals_data = [
            {"MineralName": "Cobalt", "MarketPriceUSD_per_tonne": 75000},
            {"MineralName": "Lithium", "MarketPriceUSD_per_tonne": 25000},
            {"MineralName": "Graphite", "MarketPriceUSD_per_tonne": 1200},
            {"MineralName": "Manganese", "MarketPriceUSD_per_tonne": 1800}
        ]
        
        countries_data = [
            {"CountryName": "South Africa", "MiningRevenue_BillionUSD": 55},
            {"CountryName": "DRC Congo", "MiningRevenue_BillionUSD": 12},
            {"CountryName": "Zambia", "MiningRevenue_BillionUSD": 8},
            {"CountryName": "Zimbabwe", "MiningRevenue_BillionUSD": 3}
        ]

        # Test price chart
        minerals_df = pd.DataFrame(minerals_data)
        price_chart = px.bar(minerals_df, x='MineralName', y='MarketPriceUSD_per_tonne',
                            title='Critical Mineral Prices', color='MineralName')
        
        # Test revenue chart  
        countries_df = pd.DataFrame(countries_data)
        revenue_chart = px.bar(countries_df, x='CountryName', y='MiningRevenue_BillionUSD',
                              title='Mining Revenue by Country')
        
        print("✅ Colab Charts Test: PASSED!")
        print(f"   - Created {len(minerals_data)} mineral price chart")
        print(f"   - Created {len(countries_data)} country revenue chart")
        return True
        
    except Exception as e:
        print(f"❌ Colab Charts Test: FAILED - {e}")
        return False

def test_flask_integration():
    """TEST IF CODE WILL WORK IN FLASK"""
    print("\n🚀 Testing Flask Integration...")
    
    try:
        # Test if we can create what Flask needs
        from plotly.utils import PlotlyJSONEncoder
        
        minerals_data = [
            {"MineralName": "Cobalt", "MarketPriceUSD_per_tonne": 75000},
            {"MineralName": "Lithium", "MarketPriceUSD_per_tonne": 25000}
        ]
        
        minerals_df = pd.DataFrame(minerals_data)
        chart = px.bar(minerals_df, x='MineralName', y='MarketPriceUSD_per_tonne')
        
        # This is what Flask does - convert to JSON
        chart_json = json.dumps(chart, cls=PlotlyJSONEncoder)
        
        print("✅ Flask Integration Test: PASSED!")
        print("   - Chart to JSON conversion works")
        print("   - Ready for Flask template rendering")
        return True
        
    except Exception as e:
        print(f"❌ Flask Integration Test: FAILED - {e}")
        return False

# Run all tests
if __name__ == "__main__":
    print("🧪 DEVELOPMENT BRIDGE - Comprehensive Testing")
    print("============================================")
    
    # Run all tests
    map_test = test_colab_map_creation()
    chart_test = test_colab_charts() 
    flask_test = test_flask_integration()
    
    print("\n📋 TEST SUMMARY:")
    print("================")
    print(f"🗺️  Map Creation: {'✅ PASS' if map_test else '❌ FAIL'}")
    print(f"📊 Charts: {'✅ PASS' if chart_test else '❌ FAIL'}")
    print(f"🚀 Flask Ready: {'✅ PASS' if flask_test else '❌ FAIL'}")
    
    if all([map_test, chart_test, flask_test]):
        print("\n🎉 ALL TESTS PASSED! Your Colab code is ready for Flask!")
        print("💡 You can now safely transfer code to app.py")
    else:
        print("\n⚠️  Some tests failed. Fix issues before transferring to Flask.")