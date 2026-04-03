
    
from flask import Flask, render_template, request, jsonify
import pickle
import os
import sys

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'Crop_price_pred_pick.pkl')

try:
    print(f"Loading model from: {MODEL_PATH}")
    sys.stdout.flush()
    with open(MODEL_PATH, 'rb') as f:
        rf_model = pickle.load(f)
    print("Model loaded. Keys:", list(rf_model.keys()) if isinstance(rf_model, dict) else type(rf_model))
    sys.stdout.flush()
except Exception as e:
    print("Model load error:", type(e).__name__, str(e))
    sys.stdout.flush()
    rf_model = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def crop_input(): 
    if request.method == 'GET':
        return render_template('croppage.html')
    
    if request.method == 'POST':
        try:
            state = int(request.form['stnam'])
            crop_name = int(request.form['crp'])
            production = float(request.form['production'])
            yield_value = float(request.form['yield'])
            temperature = float(request.form['temperature'])
            rainfall = float(request.form['rainfall'])

            # Resolve crop index and robustly fetch avg prices from the model
            crop_index = crop_name // 5
            avg_price1_src = rf_model.get("avg_price1")
            avg_price2_src = rf_model.get("avg_price2")

            def fetch_avg(src, idx, key_alt):
                if src is None:
                    raise KeyError(f"missing_avg_source:{key_alt}")
                # list/tuple support
                if isinstance(src, (list, tuple)):
                    return src[idx]
                # dict-like support: try numeric/index keys and original crop code
                try:
                    return src[idx]
                except Exception:
                    pass
                try:
                    return src[crop_name]
                except Exception:
                    pass
                try:
                    return src[str(crop_name)]
                except Exception:
                    pass
                raise KeyError(f"avg_price_key_not_found:{key_alt}:{idx}")

            avg1 = fetch_avg(avg_price1_src, crop_index, 'avg_price1')
            avg2 = fetch_avg(avg_price2_src, crop_index, 'avg_price2')

            input_data = [state, crop_name, avg1, avg2, production, yield_value, temperature, rainfall]

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
                'error': f"{type(e).__name__}: {str(e)}"
            }), 400

if __name__ == '__main__':
    app.run(debug=True)

