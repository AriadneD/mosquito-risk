from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from scipy.interpolate import UnivariateSpline
from calendar import monthrange
import pickle

app = Flask(__name__)

# Read the data
data = pd.read_csv('output_table.csv')

# Convert monthly risk columns to numerical values
risk_mapping = {'Low': 1, 'Moderate': 2, 'High': 3}
for month in ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']:
    data[month] = data[month].map(risk_mapping)

# Function to predict mosquito risk based on month, elevation, and distance from water
def predict_risk(date_string):
    date_obj = datetime.strptime(date_string, '%Y-%m-%d')
    current_month = date_obj.strftime('%B').lower()
    current_day = date_obj.day

    # Determine the next month
    if date_obj.month == 12:
        next_month = "january"
    else:
        next_month = datetime(date_obj.year, date_obj.month + 1, 1).strftime('%B').lower()

    days_in_current_month = monthrange(date_obj.year, date_obj.month)[1]

    # Calculate weights based on the day of the month
    weight_current_month = (days_in_current_month - current_day) / days_in_current_month
    weight_next_month = current_day / days_in_current_month

    # Calculate the risk using a weighted average of current and next month risks, along with elevation and distance from water
    data['risk_output'] = (weight_current_month * data[current_month] + weight_next_month * data[next_month]) - 0.0001 * data['elevation'] + 0.00001 * data['dist_from_water']

    # Ensure the risk output is between 1 (Low) and 3 (High)
    data['risk_output'] = data['risk_output'].clip(1, 3)

    # Return the modified list containing name, risk, latitude, and longitude
    return data[['location', 'risk_output', 'Latitude', 'Longitude']].to_dict('records')

# Prepare data for KNN
X = data[['Latitude', 'Longitude']]
y_elevation = data['elevation']
y_dist = data['dist_from_water']

knn_elevation = KNeighborsRegressor(n_neighbors=5)
knn_dist = KNeighborsRegressor(n_neighbors=5)

knn_elevation.fit(X, y_elevation)
knn_dist.fit(X, y_dist)

def month_from_vector(month_vector):
    return month_vector.index(1) + 1

def predict_risk_for_location(date, latitude, longitude, elevation=None, climate=None, dist_to_water=None):
    """
    Predicts the risk for a given location and date.
    
    Args:
    - date (str): The date in the format 'YYYY-MM-DD'
    - latitude (float): Latitude of the location
    - longitude (float): Longitude of the location
    - elevation (float, optional): Elevation of the location. If not provided, a default value will be used.
    - climate (str, optional): Climate type of the location. If not provided, a default value will be used.
    - dist_to_water (float, optional): Distance from water. If not provided, a default value will be used.
    
    Returns:
    - float: Predicted risk for the location and date.
    """
    # Load the models
    with open('trained_classifier.pkl', 'rb') as file:
        loaded_clf = pickle.load(file)

    with open('knn_elevation_model.pkl', 'rb') as file:
        knn_elevation = pickle.load(file)

    with open('knn_dist_to_water_model.pkl', 'rb') as file:
        knn_dist_to_water = pickle.load(file)

    if elevation is None:
        elevation = knn_elevation.predict([[latitude, longitude]])[0]
        
    if dist_to_water is None:
        dist_to_water = knn_dist_to_water.predict([[latitude, longitude]])[0]
    
    # Extract month from date to get the relevant monthly risk.
    month = int(date.split('-')[1])
    monthly_risks = [0] * 12  # Initialize with zeros
    monthly_risks[month - 1] = 1  # Set the relevant month's risk to 1
    
    # Create the input feature vector. Ensure the order matches the training data's order.

    month = month_from_vector(monthly_risks)

    features = [latitude, longitude] + [month] + [elevation, dist_to_water]
    
    # Predict risk using the loaded classifier.
    predicted_risk = loaded_clf.predict([features])[0]
    
    return predicted_risk

def plot_risk_over_time(start_date, end_date, address_latitude, address_longitude):
    # Convert start and end dates to datetime objects
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Create a date range between start and end dates
    date_range = pd.date_range(start=start_date_obj, end=end_date_obj)
    
    # Calculate the risk for each day in the date range
    risk_values = [predict_risk_for_location(date.strftime('%Y-%m-%d'), address_latitude, address_longitude) for date in date_range]
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(date_range, risk_values, '-o', color='blue', label='Mosquito Risk')
    
    # Mark the mean risk value on the graph
    mean_risk = np.mean(risk_values)
    plt.axhline(y=mean_risk, color='r', linestyle='--', label=f'Mean Risk: {mean_risk:.2f}')
    
    # Set titles and labels
    plt.title(f'Mosquito Risk from {start_date} to {end_date} at ({address_latitude}, {address_longitude})')
    plt.xlabel('Date')
    plt.ylabel('Risk Level')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)
    
    # Show the plot
    plt.show()

# Example usage:
# all risks
'''date_input = '2023-01-01'
result = predict_risk(date_input)
print(result)'''

@app.route('/get-location-info')
def get_location_info():
    location_name = request.args.get('location')
    location_data = data[data['location'] == location_name].iloc[0].to_dict()
    return jsonify(location_data)

@app.route('/custom_point_risk', methods=['GET'])
def get_custom_point_risk():
    if 'date' in request.args and 'lat' in request.args and 'lng' in request.args:
        date_input = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))

        risk_data = predict_risk_for_location(date_input, lat, lng)
        print("Risk data: ", risk_data)
        return jsonify(risk_data)

@app.route('/', methods=['GET', 'POST'])
def index():
    # add marker
    if request.method == 'POST':
        lat = request.form.get('lat', type=float)
        lng = request.form.get('lng', type=float)
        # Using today's date for this example, you can modify as needed
        date_input = datetime.now().strftime('%Y-%m-%d')

        # use new function
        risk_output = predict_risk_for_location(date_input, lat, lng)
        print(jsonify({'risk_output': risk_output}))
        return jsonify({'risk_output': risk_output})

    # custom date
    if 'date' in request.args:
        date_input = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        risk_data = predict_risk(date_input)
        return jsonify(risk_data)
    
    # default to current date
    date_input = datetime.now().strftime('%Y-%m-%d') # Assuming you want to use the current date
    risk_data = predict_risk(date_input)
    
    return render_template('map.html', risk_data=risk_data)

if __name__ == '__main__':
    app.run(debug=True)