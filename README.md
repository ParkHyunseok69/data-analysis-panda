## 🐼 Data Visualization App (Streamlit + Pandas)

This is a simple and interactive **Streamlit web app** that lets users upload a CSV file and instantly visualize, filter, and analyze their data — all without writing code.

---

### 🚀 Features

* 📂 **Upload CSV files**
* 🧠 **View dataset info**: shape, column types, nulls, duplicates
* 📊 **Filter rows** using:

  * `.query()` for numeric and categorical data
  * `.str.contains()` and other `.str` methods for strings
* 🔢 **Preview top/bottom rows**
* 📋 **Select columns to view**
* 📈 **Visualize data** with:

  * Histogram
  * Bar chart
  * Scatter plot
  * Box plot
  * Line chart
  * Correlation heatmap

---

### 🖥️ How to Run

1. Clone the repo:

   ```bash
   git clone https://github.com/ParkHyunseok69/data-analysis-panda.git
   cd data-analysis-panda
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   streamlit run app.py
   ```

---


### 🧪 Example Filters

#### 🔢 Numeric:

```python
Age > 25
Score <= 90
`IFR RANK` > 30
```

#### 🔤 String:

```python
df["Name"].str.contains("Ali", case=False)
df["Country"].str.startswith("Ph")
df["Email"].str.endswith(".edu")
```

---

### 📌 To-Do / Improvements (Optional)

* Add date filtering
* Export filtered data
* More chart types (Pie, Violin, etc.)
* Light/Dark theme toggle

---


### 🧑‍💻 Author

**Lawrence Andre' Q. Cabana**
[GitHub](https://github.com/ParkHyunseok69)

---

