from flask import Flask, render_template, request
import pickle
import os
import traceback

app = Flask(__name__, template_folder="templates")

@app.route("/debug")
def debug():
    files = []
    for root, dirs, fs in os.walk("."):
        for f in fs:
            files.append(os.path.join(root, f))
    return "<br>".join(files)

MODEL_FILENAME = "Crop_price_pred_pick.pkl"
MODEL_PATH = os.path.join(os.path.dirname(__file__), MODEL_FILENAME)

rf_model = None
try:
    with open(MODEL_PATH, "rb") as f:
        rf_model = pickle.load(f)
    print(f"[cropflask] Loaded model from {MODEL_PATH}")
except Exception as e:
    print(f"[cropflask] ERROR loading model from {MODEL_PATH}: {e}")
    traceback.print_exc()

@app.route('/', methods=['GET', 'POST'])
def crop_input():
    predicted_value = None

    if request.method == 'POST':
        try:
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

            if rf_model is None:
                print("[cropflask] rf_model is None — model not loaded")
                return "Model not loaded on server. Check logs.", 500

            
            avg1 = rf_model["avg_price1"][crop_name // 5]
            avg2 = rf_model["avg_price2"][crop_name // 5]
            input_data = [state, crop_name, avg1, avg2, production, yield_value, temperature, rainfall]

            predicted_value = rf_model["rf"].predict([input_data])[0]
            predicted_value = round(predicted_value, 2)
            print(f"Predicted Value: {predicted_value}")

        except Exception as e:
            print(f"[crop_input] Exception: {e}")
            traceback.print_exc()
            return f"Prediction error: {e}", 500

    return render_template('croppage.html', prediction=predicted_value)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
