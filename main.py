import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns

#HEADER
def init_session_state():
    for key, value in {"data_visible": False, "df": None, "info": None, "filter": ""}.items():
        if key not in st.session_state:
            st.session_state[key] = value
init_session_state()


st.set_page_config(page_title="Data Visualization", layout="wide")
st.title("👾 Data Visualization Using Pandas")


#FILE UPLOAD
st.header("Upload Your CSV", divider='gray')
file = st.file_uploader("", label_visibility="collapsed", type='csv')

def load_data():
    df = pd.read_csv(file)
    buffer = io.StringIO()
    df.info(buf=buffer)
    info = buffer.getvalue()
    return df, info

if file is not None:
    st.session_state.df, st.session_state.info = load_data()
    st.session_state["data_visible"] = True
    st.success("✅ File uploaded successfully!")

if st.session_state.df is not None:
    df = st.session_state.df
    
    #DATA PREVIEW
    st.header("🗂 1. Data Preview & Info")
    with st.expander("📄 Show DataFrame"):    
        st.dataframe(df)

    with st.expander("📈 Summary Statistics"):
        st.write(df.describe())
        
    with st.expander("📌 Dataset Info"):
        st.code(st.session_state.info)

    with st.expander("📐 Dataset Size"):
        st.write(df.shape)
                    
    with st.expander("🔢 Column Data Types"):
        st.write(df.dtypes)

    with st.expander("🚫 Null/NaN Count"):
        st.write(df.isnull().sum())

    with st.expander("📛 Duplicate Rows"):
        st.write(df.duplicated().sum())

    #FILTER
    st.header("🔎 2. Filtering Section")
    st.subheader("🔍 Preview Rows")
    option = st.radio("View From:", ["Head", "Tail"])
    n_rows = st.number_input("Number of Rows to Show:", 0, len(df), value=5)
    if option == "Head":
        st.dataframe(df.head(n_rows))
    else:
        st.dataframe(df.tail(n_rows))
        
    with st.expander("📋 Show Column Names"):
        def show_cols(df):
            selected = st.multiselect("Select Columns to Show", list(df.columns))
            st.subheader("Display Columns")
            st.dataframe(df[selected])
        show_cols(df)
    with st.expander("🧪 Apply Custom Filter"): 
        def filter_row(df):
            with st.expander("📘 How to use the filter box"):
                st.markdown("""
                ### 🔢 Numeric filters (via `query()`):
                - `Age > 25`
                - `Score <= 90`
                - `` `IFR RANK` > 25 `` *(backticks needed for column names with spaces)*

                ### 🔤 String filters (via `eval()` with `.str` methods):
                - `df["Name"].str.contains("Ali", case=False)`
                - `df["Country"].str.startswith("Ph", case=False)`
                - `df["Email"].str.endswith(".edu", case=False)`

                ### 🧪 Combine multiple filters:
                **With `.query()` (for numeric & categorical columns):**
                - `` `IFR RANK` > 25 and `Research Output` == 'High' ``
                - `Age > 20 or Score < 60`

                **With `.str` filters (via `eval()`):**
                - `(df["Country"].str.contains("ph", case=False)) & (df["Status"].str.contains("active", case=False))`
                - `(df["Email"].str.endswith(".edu")) | (df["Email"].str.endswith(".org"))`

                ### ⚠️ Syntax reminders:
                - Use **backticks** for column names with spaces in `query()`
                - Use **&** (AND), **|** (OR), and wrap each condition in `(...)` when using `.str` filters
                - Use double quotes (`" "`) inside `.str.contains()` or `.startswith()`

                ---
                🧠 Tip: Use `.str.lower()` if you want to normalize case first (e.g., `df["Name"].str.lower().contains("ali")`)
                """)
            col = st.selectbox("Choose a column to filter", list(df.columns))
            method = st.selectbox("Choose a string method to use", [".contains", ".startswith", ".endswith"])
            if st.button("Generate .str.contains filter"):
                st.session_state["filter"] = f'df["{col}"].str{method}("your text")'
            input = st.text_input("Enter filter condition", value=st.session_state.get("filter", ""))
            st.subheader("Display Filtered Rows")
            if input:
                try:
                    if ".str" in input:
                        if input.strip().startswith('df['):
                            filtered_df = df[eval(input)]
                            st.dataframe(filtered_df)
                        else:
                            st.error("For `.str` filters, use this format: df[\"ColumnName\"].str.contains(\"value\")")
                    else:
                        def auto_wrap(input_str, df_columns):
                            for col in df_columns:
                                if " " in col and f"`{col}`" not in input_str:
                                    input_str = input_str.replace(col, f"`{col}`")
                            return input_str
                        wrapped_input = auto_wrap(input, df.columns)
                        filtered_df = df.query(wrapped_input)
                        st.dataframe(filtered_df)
                except Exception as e:
                    st.error(f'Invalid query: {e}')
            else:
                st.info("Please enter a filter condition")
        filter_row(df)


    #GRAPH
    st.header("📊 3. Visualization Section")
    chart_type = st.selectbox("Choose a chart type", ["Histogram", "Bar Chart", "Scatter Plot", "Box Plot", "Line Chart", "Correlation Heatmap"])

    if chart_type == "Histogram":
        col = st.selectbox("Column", df.select_dtypes(include="number").columns)
        fig, ax = plt.subplots()
        sns.histplot(df[col], kde=True, ax=ax)
        st.pyplot(fig)
    elif chart_type == "Bar Chart":
        col = st.selectbox("Column", df.select_dtypes(include="object").columns)
        st.bar_chart(df[col].value_counts())

    elif chart_type == "Scatter Plot":
        col1 = st.selectbox("X-axis", df.select_dtypes(include="number").columns)
        col2 = st.selectbox("Column", df.select_dtypes(include="number").columns, index=1)
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x=col1, y=col2, ax=ax)
        st.pyplot(fig)
    elif chart_type == "Box Plot":
        numeric_col = st.selectbox("Numeric Column", df.select_dtypes(include='number').columns)
        category_col = st.selectbox("Category Column", df.select_dtypes(include='object').columns)
        fig, ax = plt.subplots()
        sns.boxplot(data=df, x=category_col, y=numeric_col, ax=ax)
        st.pyplot(fig)
    elif chart_type == "Line Chart":
        date_col = st.selectbox("Date Column", df.select_dtypes(include='datetime64[ns]').columns)
        value_col = st.selectbox("Value Column", df.select_dtypes(include='number').columns)
        try:
            st.line_chart(df.set_index(date_col)[value_col])
        except:
            st.info("There's no Date/Time Column in the dataset")
    elif chart_type == "Correlation Heatmap":
        fig, ax = plt.subplots()
        corr =df.select_dtypes(include='number').corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)
    

else:
    st.info("📂 Please upload a CSV file to start.")

