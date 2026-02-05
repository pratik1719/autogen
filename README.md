# 🚀 AutoGen-EDA: LLM-Assisted Automated Dataset Analysis

**Author:** Pratik Mohan Patil (pratik1719)  
**Course:** Data Science - CU Boulder  
**Assignment:** Automated Dataset Insight Generator

---

## 📖 Overview

AutoGen-EDA is an **intelligent exploratory data analysis system** that leverages Large Language Models (Google Gemini) to automatically analyze any CSV dataset and generate comprehensive, professional-quality insights.

### 🌟 Key Features

- **🧠 Adaptive Analysis**: LLM generates custom EDA strategy based on dataset characteristics
- **📊 Comprehensive Statistics**: Descriptive stats, outlier detection, correlation analysis
- **📈 Smart Visualizations**: Auto-generates 5+ relevant plots (histograms, boxplots, heatmaps, etc.)
- **💡 AI-Powered Insights**: LLM generates narrative insights grounded in verified statistics
- **📄 Dual Reports**: Both HTML and Markdown reports with embedded visualizations
- **🔒 Hallucination Prevention**: Two-stage LLM architecture ensures factual accuracy
- **🔍 Data Quality Checks**: Detects missing values, duplicates, outliers, and privacy concerns

---

## 🎯 Architecture

### **Two-Stage LLM Strategy**

```
┌─────────────────┐
│  Load Dataset   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────┐
│  Data Profiling │────▶│ LLM Stage 1: │
│  (Facts Only)   │     │ Plan Strategy│
└────────┬────────┘     └──────┬───────┘
         │                     │
         │                     ▼
         │          ┌──────────────────┐
         │          │ EDA Plan (JSON)  │
         │          │ - Which columns  │
         │          │ - Which plots    │
         │          │ - Which stats    │
         │          └────────┬─────────┘
         │                   │
         ▼                   ▼
┌─────────────────────────────────┐
│  Execute Analysis (NO LLM)      │
│  - Compute all statistics       │
│  - Generate visualizations      │
│  - Collect verified facts       │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────┐     ┌──────────────┐
│ Verified Facts  │────▶│ LLM Stage 2: │
│ (Numbers Only)  │     │ Write Insights│
└─────────────────┘     └──────┬───────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │ Final Reports    │
                    │ - HTML + Markdown│
                    │ - Embedded plots │
                    └──────────────────┘
```

### **Why This Prevents Hallucination**

1. **Stage 1 (Planning)**: LLM only suggests *what* to analyze, not the results
2. **Execution**: Pure Python/pandas compute all numbers - no LLM involved
3. **Stage 2 (Insights)**: LLM only interprets *provided* statistics, can't invent numbers

---

## 🛠️ Installation

### **Prerequisites**

- Python 3.8+
- Google Gemini API key (free tier available)

### **Setup Steps**

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd autogen-eda
```

2. **Create virtual environment:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Get Gemini API Key:**
   - Visit: https://aistudio.google.com/app/apikey
   - Sign in with Google
   - Click "Create API Key"
   - Copy the key (starts with `AIza...`)

5. **Configure environment:**
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your API key:
# GEMINI_API_KEY=your_api_key_here
```

---

## 🚀 Usage

### **Basic Usage**

```bash
python src/main.py data/your_dataset.csv
```

### **With Schema File**

```bash
python src/main.py data/your_dataset.csv --schema data/schema.json
```

### **Custom Output Directory**

```bash
python src/main.py data/your_dataset.csv --output custom_reports/
```

### **Full Example**

```bash
# Analyze the chronic disease dataset
python src/main.py data/chronic_disease.csv --output output/
```

---

## 📂 Project Structure

```
autogen-eda/
├── src/
│   ├── main.py                 # Entry point & orchestrator
│   ├── data_loader.py          # CSV & schema loading
│   ├── llm_client.py           # Gemini API integration
│   ├── eda_planner.py          # LLM-powered strategy generation
│   ├── analyzer.py             # Statistical computations (NO LLM)
│   ├── visualizer.py           # Plot generation
│   ├── insight_generator.py    # LLM insight generation
│   ├── report_builder.py       # HTML/Markdown report assembly
│   └── utils.py                # Helper functions
├── data/                       # Place your datasets here
├── output/                     # Generated reports & plots
├── logs/                       # GenAI prompt/response logs
├── video/                      # Demo video
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

---

## 📊 Output Files

After running, you'll get:

### **In `output/` directory:**
- `eda_report_<dataset>.html` - Interactive HTML report with embedded plots
- `eda_report_<dataset>.md` - Markdown report
- `eda_plan_<dataset>.json` - LLM-generated analysis strategy
- `analysis_results_<dataset>.json` - Raw statistical results
- Multiple `.png` plot files (histograms, boxplots, heatmaps, etc.)

### **In `logs/` directory:**
- `genai_log.md` - Complete record of all LLM interactions

---

## 🎬 Demo Video

The demo video shows:
1. Running the system on the development dataset (chronic disease)
2. Running on a new/unseen dataset (nutrition & obesity)
3. Explanation of the generated outputs
4. Walkthrough of the code architecture

**Video Location:** `video/demo.mp4` or see `video/video_link.txt`

---

## 🤖 GenAI Usage Documentation

All LLM interactions are logged in `logs/genai_log.md`:

- **Tool Used:** Google Gemini (gemini-1.5-flash)
- **Prompts:** Complete prompts sent to LLM
- **Responses:** Full responses received
- **Verification:** How outputs were validated before use

### **How GenAI Was Used**

1. **EDA Strategy Planning:**
   - Input: Dataset profile (shape, types, sample values)
   - Output: JSON plan specifying which analyses to run
   - Verification: Plan validated against dataset, fallback generated if invalid

2. **Insight Generation:**
   - Input: Verified statistical facts computed by Python
   - Output: Human-readable insights
   - Verification: Facts provided to LLM, not computed by it

3. **Executive Summary:**
   - Input: Top insights
   - Output: 2-3 sentence summary
   - Verification: Based only on generated insights

---

## 🧪 Testing with Different Datasets

### **Dataset 1: U.S. Chronic Disease Indicators**
- **Type:** Numeric-heavy with categorical breakdowns
- **Size:** Large (100k+ rows)
- **Source:** data.gov
- **URL:** https://catalog.data.gov/dataset/u-s-chronic-disease-indicators

### **Dataset 2: Nutrition, Physical Activity, and Obesity**
- **Type:** Survey data, categorical-heavy
- **Size:** Medium (50k+ rows)
- **Source:** data.gov
- **URL:** https://catalog-beta.data.gov/dataset/nutrition-physical-activity-and-obesity-behavioral-risk-factor-surveillance-system

Both datasets demonstrate the system's ability to:
- Adapt analysis strategy to data characteristics
- Handle different column types (numeric, categorical, datetime)
- Generate relevant visualizations automatically
- Produce meaningful insights

---

## ✨ Advanced Features

### **1. Adaptive Analysis**
- Detects if dataset is numeric-heavy vs categorical-heavy
- Adjusts analysis approach accordingly
- Handles edge cases (only one column type, high missing data, etc.)

### **2. Smart Data Quality Checks**
- Detects missing value codes (-999, "NA", "unknown")
- Identifies high-cardinality categorical columns
- Warns about potential privacy concerns (SSN, email patterns)
- Flags constant columns and duplicates

### **3. Robust Outlier Detection**
- Uses IQR method (1.5×IQR rule)
- Computes outlier counts and percentages
- Visualizes outliers in boxplots

### **4. Correlation Analysis**
- Generates correlation matrix for numeric variables
- Identifies strong correlations (|r| > 0.5)
- Creates heatmap visualization

### **5. Publication-Quality Visualizations**
- Professional styling with seaborn
- Proper labels, titles, legends
- Mean/median lines on histograms
- Embedded in HTML report

---

## 🔧 Customization

### **Change LLM Model**

Edit `.env`:
```
GEMINI_MODEL=gemini-1.5-pro  # For more complex reasoning
```

### **Adjust Plot Count**

Modify `eda_planner.py`:
```python
# Ensure at least N visualizations
if len(plan['recommended_visualizations']) < 7:  # Change from 5 to 7
```

### **Add Custom Visualizations**

Add new plot types in `visualizer.py`:
```python
def _plot_custom(self, spec: Dict[str, Any]):
    # Your custom plot logic
    pass
```

---

## 🐛 Troubleshooting

### **"GEMINI_API_KEY not found"**
- Make sure `.env` file exists in project root
- Check that API key is correctly set
- Don't put quotes around the key value

### **"Failed to load CSV"**
- Check file encoding (tool auto-detects, but try UTF-8)
- Ensure CSV is properly formatted
- Check file path is correct

### **"Error generating plan"**
- Check internet connection (requires API access)
- Verify API key is valid
- System will use fallback plan if LLM fails

### **Low quality visualizations**
- Some columns may have too many unique values
- System automatically limits to top 20 categories for bar charts
- Adjust in `visualizer.py` if needed

---

## 📝 Assignment Requirements Checklist

✅ **Code (GitHub repo, src/ subfolder):**
- Python scripts that run end-to-end
- requirements.txt included
- README.md with clear instructions

✅ **Outputs:**
- Dataset overview (rows, columns, types, missing values)
- Descriptive statistics (min/max/mean/median/std/IQR/outliers)
- At least 5 visualizations with titles and labels
- 5-10 bullet insights
- Limitations and bias notes

✅ **Video (video/ subfolder):**
- 5-7 minute screencast
- Demonstrates on 2 different datasets
- Shows generated outputs
- Explains how it works

✅ **GenAI Log (logs/ subfolder):**
- Tool used: Google Gemini
- Prompts and responses documented
- Verification steps noted

✅ **Constraints:**
- Uses public, non-sensitive datasets
- Reproducible (same inputs = same outputs)
- No private data exposure

---

## 🎓 Learning Outcomes

This project demonstrates:

1. **LLM Integration:** Practical use of generative AI for data analysis
2. **Hallucination Prevention:** Two-stage architecture with verification
3. **Prompt Engineering:** Crafting effective prompts for structured outputs
4. **Data Science Pipeline:** End-to-end automated EDA workflow
5. **Software Engineering:** Modular, maintainable code structure
6. **Report Generation:** Professional documentation and visualization

---

## 🤝 Contributing

This is a course assignment, but feedback is welcome! Feel free to:
- Report bugs
- Suggest features
- Improve documentation

---

## 📄 License

MIT License - Feel free to use for learning and educational purposes.

---

## 🙏 Acknowledgments

- **Course:** Data Science, CU Boulder
- **LLM Provider:** Google Gemini (free tier)
- **Datasets:** data.gov (U.S. government open data)
- **Libraries:** pandas, matplotlib, seaborn, scipy

---

## 📧 Contact

**Pratik Mohan Patil**
- GitHub: [@pratik1719](https://github.com/pratik1719)
- Project: AutoGen-EDA

---

**Built with ❤️ and 🤖 for CU Boulder Data Science**
