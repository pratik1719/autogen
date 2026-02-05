# ⚡ Quick Start Guide

Get AutoGen-EDA running in 5 minutes!

## 🚀 Step 1: Setup (2 minutes)

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

## 🔑 Step 2: Get API Key (2 minutes)

1. Go to: **https://aistudio.google.com/app/apikey**
2. Sign in with Google
3. Click **"Create API Key"**
4. Copy the key (starts with `AIza...`)

## ⚙️ Step 3: Configure (30 seconds)

```bash
# 1. Copy example env file
cp .env.example .env

# 2. Edit .env file and paste your API key:
# GEMINI_API_KEY=AIza... (your key here)
```

On Windows, you can edit with:
```cmd
notepad .env
```

On Mac/Linux:
```bash
nano .env
```

## 📥 Step 4: Download Test Data (30 seconds)

### **Option A: Use Pre-Selected Datasets**

Download these two datasets and place in `data/` folder:

1. **U.S. Chronic Disease Indicators**
   - URL: https://catalog.data.gov/dataset/u-s-chronic-disease-indicators
   - Click "Download" → "CSV"
   - Save as: `data/chronic_disease.csv`

2. **Nutrition, Physical Activity, and Obesity**
   - URL: https://catalog-beta.data.gov/dataset/nutrition-physical-activity-and-obesity-behavioral-risk-factor-surveillance-system
   - Click "Download" → "CSV"
   - Save as: `data/nutrition_obesity.csv`

### **Option B: Use Your Own Dataset**

Just place any CSV file in the `data/` folder!

## ▶️ Step 5: Run! (30 seconds)

```bash
# Analyze your dataset
python src/main.py data/your_dataset.csv

# Example with chronic disease data:
python src/main.py data/chronic_disease.csv
```

## 🎉 Step 6: View Results

Open the generated files in `output/`:

- **`eda_report_*.html`** ← Open this in your browser!
- **`eda_report_*.md`** ← Markdown version
- **`*.png`** ← Individual plots

## 📊 Full Example Command

```bash
# Complete command with all options
python src/main.py data/chronic_disease.csv --output results/
```

## 🐛 Troubleshooting

### **"No module named 'google.generativeai'"**
```bash
pip install --upgrade google-generativeai
```

### **"GEMINI_API_KEY not found"**
- Make sure `.env` file exists
- Check that you pasted your API key correctly
- No quotes needed around the key

### **"CSV file not found"**
- Check the file path
- Make sure file is in `data/` folder
- Use forward slashes: `data/file.csv` not `data\file.csv`

## 🎬 Next Steps

1. ✅ Run on first dataset
2. ✅ Run on second dataset (different type)
3. 📹 Record your demo video
4. 📦 Zip and submit!

## 💡 Pro Tips

- **Start with a smaller dataset** (< 10MB) for faster testing
- **Check `logs/genai_log.md`** to see all LLM interactions
- **HTML report has embedded plots** - very convenient!
- **Markdown report** is great for version control

---

**Need help?** Check the full README.md or contact Pratik (pratik1719)
