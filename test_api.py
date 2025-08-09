import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    print("Testing Vehicle Registration Dashboard API...")
    print("=" * 50)
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/")
        print(f"Health Check: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data.get('status')}")
            print(f"Data Source: {data.get('data_source')}")
            print(f"Vehicle Records: {data.get('data_status', {}).get('vehicle_registrations')}")
            print(f"Manufacturer Records: {data.get('data_status', {}).get('manufacturer_registrations')}")
        print()
    except Exception as e:
        print(f"Health Check Error: {e}")
        print()
    
    # Test registrations endpoint
    try:
        response = requests.get(f"{base_url}/api/registrations")
        print(f"Registrations: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data.get('status')}")
            if data.get('status') == 'success':
                chart_data = data.get('data', {}).get('chart_data', [])
                print(f"Chart Data Points: {len(chart_data)}")
                if chart_data:
                    print(f"Sample Data Keys: {list(chart_data[0].keys())}")
                    print(f"First Month: {chart_data[0].get('month')}")
                    print(f"Available Categories: {[k for k in chart_data[0].keys() if k not in ['month', 'total']]}")
        print()
    except Exception as e:
        print(f"Registrations Error: {e}")
        print()
    
    # Test manufacturer filtering
    try:
        response = requests.get(f"{base_url}/api/registrations?manufacturers=Hero%20MotoCorp,Honda")
        print(f"Manufacturer Filter: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data.get('status')}")
            if data.get('status') == 'success':
                chart_data = data.get('data', {}).get('chart_data', [])
                print(f"Filtered Chart Data Points: {len(chart_data)}")
                if chart_data:
                    print(f"Filtered Data Keys: {list(chart_data[0].keys())}")
        print()
    except Exception as e:
        print(f"Manufacturer Filter Error: {e}")
        print()
    
    # Test category filtering
    try:
        response = requests.get(f"{base_url}/api/registrations?category=3W")
        print(f"Category Filter (3W): {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data.get('status')}")
            if data.get('status') == 'success':
                chart_data = data.get('data', {}).get('chart_data', [])
                print(f"3W Chart Data Points: {len(chart_data)}")
                if chart_data:
                    print(f"3W Data Keys: {list(chart_data[0].keys())}")
        print()
    except Exception as e:
        print(f"Category Filter Error: {e}")
        print()

if __name__ == "__main__":
    test_api()
