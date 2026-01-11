# Crop Price Prediction - Professional Platform

A sophisticated AI-powered crop price prediction platform built with Flask and machine learning. Predict crop prices based on agricultural data to make informed farming decisions.

## Features

✅ **AI-Powered Predictions** - Advanced machine learning models for accurate price forecasting  
✅ **Multi-Crop Support** - 10+ major Indian crops across all agricultural states  
✅ **Real-Time Data Analysis** - Based on production, yield, temperature, and rainfall  
✅ **Professional UI** - Modern, responsive design with smooth animations  
✅ **Mobile Friendly** - Works seamlessly on all devices  
✅ **Fast Results** - Instant price predictions in seconds  

## Project Structure

```
├── cropflask.py              # Main Flask application
├── Crop_price_pred_pick.pkl  # Pre-trained ML model
├── Crop Price Dataset.csv    # Training dataset
├── Crop_price_pred.ipynb     # Model training notebook
├── requirements.txt          # Python dependencies
├── vercel.json              # Vercel deployment config
└── templates/
    ├── index.html           # Landing page
    └── croppage.html        # Prediction form page
```

## Installation & Local Development

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup

1. **Clone or download the project**
```bash
cd "Market Crop Price Prediction"
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python cropflask.py
```

4. **Open in browser**
- Navigate to `http://localhost:5000`
- You'll see the professional landing page
- Click "Start Predicting" to access the prediction engine

## Usage

1. **Home Page** - View features, benefits, and how the platform works
2. **Prediction Page** - Enter your crop details:
   - Select your agricultural state
   - Choose your crop type
   - Input production, yield, temperature, and rainfall data
   - Click "Predict Price" for instant results

## Deploying to Vercel

### Prerequisites
- Vercel account (free at [vercel.com](https://vercel.com))
- Git and GitHub account

### Deployment Steps

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git push -u origin main
```

2. **Connect to Vercel**
   - Visit [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Select "Python" as the framework
   - Click "Deploy"

3. **Environment Variables** (if needed)
   - Vercel will automatically detect `requirements.txt`
   - Your app will deploy to a live URL

### Configuration Files Included

- **vercel.json** - Configured for Python/Flask on Vercel
- **requirements.txt** - All necessary Python packages

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript
- **ML Model**: Scikit-learn Random Forest
- **Hosting**: Vercel (Serverless deployment)

## Color Scheme

The app uses a professional agricultural theme:
- Primary Green: `#2a7f62` (Trust, growth)
- Accent Cyan: `#6dd5ed` (Energy, freshness)
- Action Green: `hsl(100, 54.20%, 51.20%)` (Growth, action)

## Performance Optimizations

- **Responsive Design** - Mobile-first approach
- **CSS Animations** - Smooth, performant transitions
- **Fast Loading** - Optimized assets and minimal dependencies
- **SEO Ready** - Proper meta tags and semantic HTML

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Android)

## API Endpoints

```
GET  /              - Home page (landing page)
GET  /predict       - Prediction form page
POST /predict       - Submit form and get prediction
```

## Future Enhancements

- Historical price data visualization
- Crop comparison tool
- Weather integration API
- User accounts for saved predictions
- Mobile app
- Multi-language support

## License

Free to use and modify for educational and commercial purposes.

## Support

For issues or questions, please refer to the project documentation or create an issue.

---

**Built with ❤️ for farmers and agricultural professionals**
