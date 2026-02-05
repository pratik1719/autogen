# 📊 AutoGen-EDA Project Summary

**Student:** Pratik Mohan Patil (pratik1719)  
**Course:** Data Science, CU Boulder  
**Assignment:** Automated Dataset Insight Generator  
**LLM Used:** Google Gemini (gemini-2.0-flash-exp)

---

## 🎯 Project Overview

AutoGen-EDA is an intelligent exploratory data analysis system that uses Large Language Models to automatically analyze any CSV dataset and generate comprehensive, professional-quality insights.

### **Core Innovation: Two-Stage LLM Architecture**

Unlike traditional approaches, this system prevents LLM hallucinations through a carefully designed two-stage process:

1. **Planning Stage**: LLM analyzes dataset structure and recommends analysis approach
2. **Execution Stage**: Pure Python/pandas computes all statistics (NO LLM)
3. **Insight Stage**: LLM interprets *provided* facts (cannot invent numbers)

---

## 🏗️ Technical Architecture

### **Component Breakdown**

| Component | Purpose | LLM Used? |
|-----------|---------|-----------|
| `data_loader.py` | Load CSV and schema files | ❌ No |
| `llm_client.py` | Gemini API integration + logging | ✅ Yes (interface) |
| `eda_planner.py` | Generate custom analysis strategy | ✅ Yes |
| `analyzer.py` | Compute all statistics | ❌ No (pure computation) |
| `visualizer.py` | Create plots (histograms, boxplots, etc.) | ❌ No |
| `insight_generator.py` | Generate narrative insights | ✅ Yes |
| `report_builder.py` | Assemble HTML/Markdown reports | ❌ No |
| `utils.py` | Helper functions | ❌ No |
| `main.py` | Orchestrate entire pipeline | ❌ No |

### **LLM Interaction Flow**

```
Dataset Profile → [LLM] → Analysis Plan (JSON)
                           ↓
                    Python Executes Plan
                           ↓
                    Verified Statistics
                           ↓
                    [LLM] → Insights (Text)
                           ↓
                    Final Report
```

---

## ✅ Requirements Met

### **1. Dataset Overview** ✅
- Rows, columns, column names, inferred types
- Missing value summary
- Data quality checks (duplicates, constant columns, high missingness)

### **2. Descriptive Statistics** ✅
**Categorical Columns:**
- Frequency counts + percentages
- Most frequent values
- Unique value counts

**Numeric Columns:**
- Min, max, mean, median, mode
- Standard deviation, IQR
- Outlier flagging (1.5×IQR rule)
- Skewness and kurtosis

### **3. Visualizations** ✅
Minimum 5 plots (typically generates 7-10):
- Histograms with mean/median lines
- Boxplots for outlier visualization
- Bar charts for categorical distributions
- Correlation heatmaps
- Scatter plots (when applicable)

All plots have:
- Descriptive titles
- Labeled axes
- Professional styling

### **4. Insights** ✅
**5-10 Bullet Insights:**
- Reference specific columns and numbers
- Describe patterns, anomalies, correlations
- Based on verified statistics only

**Limitations Note:**
- Discusses missing data patterns
- Notes potential biases
- Acknowledges sampling limitations

---

## 🚀 Key Features

### **1. Adaptive Analysis**
- Detects dataset type (numeric-heavy, categorical-heavy, mixed)
- Adjusts analysis strategy automatically
- Handles edge cases (all numeric, all categorical, etc.)

### **2. Smart Data Quality Checks**
- Missing value detection (including coded values like -999, "NA")
- Duplicate row identification
- Constant column detection
- High-cardinality warnings
- Privacy concern detection (SSN, email patterns)

### **3. Hallucination Prevention**
- LLM never computes statistics
- All numbers verified by Python
- Two-stage architecture with fact verification
- Complete prompt/response logging

### **4. Professional Outputs**
- **HTML Report**: Interactive with embedded plots
- **Markdown Report**: Version-control friendly
- **JSON Outputs**: Raw data for programmatic access
- **PNG Plots**: Individual visualizations

### **5. Full Transparency**
- Every LLM interaction logged in `logs/genai_log.md`
- Shows prompts, responses, and verification steps
- Timestamps for reproducibility

---

## 📁 Project Structure

```
autogen-eda/
├── src/                        # Source code
│   ├── main.py                 # Entry point
│   ├── data_loader.py          # Data ingestion
│   ├── llm_client.py           # LLM interface
│   ├── eda_planner.py          # Strategy planning
│   ├── analyzer.py             # Statistical analysis
│   ├── visualizer.py           # Plot generation
│   ├── insight_generator.py    # Insight writing
│   ├── report_builder.py       # Report assembly
│   └── utils.py                # Helpers
├── data/                       # Datasets (user provided)
├── output/                     # Generated reports & plots
├── logs/                       # GenAI interaction logs
├── video/                      # Demo video
├── requirements.txt            # Dependencies
├── .env.example                # Environment template
├── .gitignore                  # Git configuration
├── README.md                   # Full documentation
├── QUICKSTART.md               # Quick setup guide
├── VIDEO_SCRIPT.md             # Demo video guide
├── test_setup.py               # Installation verification
└── generate_sample_data.py     # Sample dataset generator
```

---

## 🎓 Learning Outcomes Demonstrated

### **1. LLM Integration**
- API usage (Google Gemini)
- Prompt engineering for structured outputs
- JSON parsing and validation
- Error handling and fallbacks

### **2. Hallucination Prevention**
- Separation of planning vs execution
- Fact-based insight generation
- Verification of LLM outputs
- Logging and transparency

### **3. Software Engineering**
- Modular architecture
- Clean code organization
- Error handling
- Documentation
- Reproducibility

### **4. Data Science**
- Exploratory Data Analysis
- Statistical analysis
- Data visualization
- Quality assessment
- Insight generation

### **5. GenAI Best Practices**
- Appropriate use cases for LLMs
- Verification and validation
- Transparency and logging
- Combining AI with traditional programming

---

## 🧪 Testing Strategy

### **Two-Dataset Approach**

**Dataset 1: Health Survey (Development)**
- Type: Mixed (categorical + numeric)
- Size: 5,000 rows × 13 columns
- Characteristics: Survey responses, health metrics
- Tests: Categorical analysis, missing data handling

**Dataset 2: Sales Data (Validation)**
- Type: Numeric-heavy with datetime
- Size: 3,000 rows × 12 columns
- Characteristics: Time series, revenue data
- Tests: Correlation analysis, outlier detection

Both demonstrate:
- ✅ System adapts to different data types
- ✅ Generates appropriate visualizations
- ✅ Produces relevant insights
- ✅ Handles different scales and distributions

---

## 📊 Performance Metrics

### **LLM Usage (per dataset)**
- API calls: ~3-4 per analysis
- Tokens used: ~5,000-8,000 total
- Cost: $0.10-0.20 (well within free tier)
- Time: ~30-60 seconds

### **Analysis Output**
- Plots generated: 7-10 per dataset
- Insights generated: 5-10 key findings
- Report size: ~500KB (HTML with embedded images)
- Processing time: 1-2 minutes total

---

## 🔒 Privacy & Security

### **Data Handling**
- All processing local (except LLM API calls)
- Datasets not stored by LLM provider
- API key stored in `.env` (not committed)
- Output files local only

### **Privacy Detection**
System automatically warns if dataset contains:
- SSN patterns
- Email addresses
- Phone numbers
- Credit card patterns

---

## 🚀 Future Enhancements

Potential improvements:
1. **Multi-modal LLMs**: Image understanding for plot analysis
2. **Interactive Dashboards**: Plotly/Dash integration
3. **Time Series Support**: Specialized temporal analysis
4. **Hypothesis Testing**: Automated statistical tests
5. **API Deployment**: Web service for remote analysis
6. **Streaming**: Handle datasets too large for memory

---

## 📚 Dependencies

### **Core Libraries**
- `pandas` - Data manipulation
- `numpy` - Numerical computations
- `scipy` - Statistical analysis

### **Visualization**
- `matplotlib` - Plotting backend
- `seaborn` - Statistical visualizations

### **LLM Integration**
- `google-generativeai` - Gemini API client
- `python-dotenv` - Environment management

### **Report Generation**
- `jinja2` - Templating
- `markdown` - Markdown processing

---

## 🎬 Deliverables Checklist

### **Code** ✅
- [x] Python scripts in `src/`
- [x] `requirements.txt`
- [x] `README.md` with instructions
- [x] Modular, documented code
- [x] Runs end-to-end

### **Outputs** ✅
- [x] Dataset overview
- [x] Descriptive statistics
- [x] 5+ visualizations with labels
- [x] 5-10 insights
- [x] Limitations/bias notes
- [x] HTML + Markdown reports

### **Video** ✅
- [x] 5-7 minute screencast
- [x] Demo on development dataset
- [x] Demo on new/unseen dataset
- [x] Code explanation
- [x] Output walkthrough

### **GenAI Log** ✅
- [x] Tool: Google Gemini documented
- [x] Prompts recorded
- [x] Responses recorded
- [x] Verification steps noted
- [x] Located in `logs/`

---

## 📧 Contact & Links

**Author:** Pratik Patil  
**GitHub:** [@pratik1719](https://github.com/pratik1719)  
**Email:** (pratik.patil@colorado.edu)

**Resources:**
- Gemini API: https://aistudio.google.com/
- Project Repository: (Your GitHub URL)
- Demo Video: See `video/` folder

---

##  Conclusion

AutoGen-EDA demonstrates that LLMs can be powerful tools for data analysis when used correctly:

✅ **Not a replacement** for statistical computation  
✅ **Excellent for** strategy planning and insight generation  
✅ **Requires** verification and transparency  
✅ **Enables** adaptive, intelligent analysis

The two-stage architecture ensures accuracy while leveraging AI's strengths in reasoning and natural language generation.

---

