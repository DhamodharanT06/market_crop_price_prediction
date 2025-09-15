
    
from flask import Flask, render_template, request
import pickle
import os

@app.route('/debug-files')
def debug_files():
    return str(os.listdir('.')) + " | templates: " + str(os.listdir('templates'))

app = Flask(__name__,template_folder="templates")

with open('Crop_price_pred_pick.pkl', 'rb') as f:
    rf_model = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def crop_input(): 
    predicted_value = None 

    if request.method == 'POST':
        
        state = request.form['stnam']
        crop_name = int(request.form['crp'])
        production = float(request.form['production'])
        yield_value = float(request.form['yield'])
        temperature = float(request.form['temperature'])
        rainfall = float(request.form['rainfall'])

        print(f"State: {state}")
        print(f"Crop Name: {crop_name}")
        print(f"Production: {production} tons")
        print(f"Yield: {yield_value} per acre")
        print(f"Temperature: {temperature}°C")
        print(f"Rainfall: {rainfall} mm")
      
        
        input_data = [state , crop_name , rf_model["avg_price1"][crop_name//5] , rf_model["avg_price2"][crop_name//5] , production, yield_value, temperature, rainfall]  

        predicted_value = rf_model["rf"].predict([input_data])[0]  
        predicted_value = round(predicted_value , 2)
        print(predicted_value)
        print(f"Predicted Value: {predicted_value}")
        

    return render_template('croppage.html', prediction=predicted_value)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

