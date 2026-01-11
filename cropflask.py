
    
from flask import Flask, render_template, request, jsonify
import pickle

app = Flask(__name__)

with open('Crop_price_pred_pick.pkl', 'rb') as f:
    rf_model = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def crop_input(): 
    if request.method == 'GET':
        return render_template('croppage.html')
    
    if request.method == 'POST':
        try:
            state = request.form['stnam']
            crop_name = int(request.form['crp'])
            production = float(request.form['production'])
            yield_value = float(request.form['yield'])
            temperature = float(request.form['temperature'])
            rainfall = float(request.form['rainfall'])

            input_data = [state , crop_name , rf_model["avg_price1"][crop_name//5] , rf_model["avg_price2"][crop_name//5] , production, yield_value, temperature, rainfall]  

            predicted_value = rf_model["rf"].predict([input_data])[0]  
            predicted_value = round(predicted_value , 2)
            print(f"Predicted Value: {predicted_value}")
            
            return jsonify({
                'success': True,
                'prediction': predicted_value
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400

if __name__ == '__main__':
    app.run(debug=True)

