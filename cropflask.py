
    
from flask import Flask, render_template, request, jsonify
import pickle
import os
import sys

app = Flask(__name__)

CROP_LABELS_BY_CODE = {
    0: "ARHAR",
    5: "COTTON",
    10: "GRAM",
    15: "GROUNDNUT",
    20: "MAIZE",
    25: "MOONG",
    30: "MUSTARD",
    35: "PADDY",
    40: "SUGARCANE",
    45: "WHEAT",
}

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
            crop_label = CROP_LABELS_BY_CODE.get(crop_name, "")

            def fetch_avg(src, idx, key_alt):
                if src is None:
                    raise KeyError(f"missing_avg_source:{key_alt}")

                # Build broad candidate keys to support different serialization formats.
                candidate_keys = [
                    idx,
                    crop_name,
                    str(idx),
                    str(crop_name),
                    f"{idx}.0",
                    f"{crop_name}.0",
                    crop_label,
                    crop_label.lower() if crop_label else "",
                ]

                # pandas Series/DataFrame-like objects
                if hasattr(src, "iloc"):
                    try:
                        return float(src.iloc[idx])
                    except Exception:
                        pass

                # dict-like objects (including plain dict)
                if hasattr(src, "keys"):
                    for k in candidate_keys:
                        if k == "":
                            continue
                        try:
                            return float(src[k])
                        except Exception:
                            continue

                    # Try normalized integer matching for weird key types like 0.0
                    try:
                        normalized = {}
                        for k, v in src.items():
                            try:
                                normalized[int(float(k))] = v
                            except Exception:
                                continue
                        if idx in normalized:
                            return float(normalized[idx])
                        if crop_name in normalized:
                            return float(normalized[crop_name])
                    except Exception:
                        pass

                # list/tuple/ndarray-like support
                try:
                    if len(src) > idx:
                        return float(src[idx])
                except Exception:
                    pass

                # Last-resort fallback: use first numeric value to avoid 400 in production.
                try:
                    if hasattr(src, "values"):
                        values = list(src.values())
                    else:
                        values = list(src)
                    if values:
                        return float(values[0])
                except Exception:
                    pass

                raise KeyError(f"avg_price_key_not_found:{key_alt}:{idx}:{crop_name}:{crop_label}")

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

