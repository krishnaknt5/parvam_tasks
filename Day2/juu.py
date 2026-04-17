import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import io
import math

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="Student Dashboard", layout="wide")

# -----------------------
# LOGIN SYSTEM
# -----------------------
def login():
    st.markdown("<h1 style='text-align:center;'>📊 Student Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>🔐 Login</h3>", unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if username == "admin" and password == "1234":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

# -----------------------
# SIDEBAR
# -----------------------
st.sidebar.title("⚙️ Controls")

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

# -----------------------
# FILE UPLOAD
# -----------------------
st.sidebar.header("📁 Upload Data")

uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.sidebar.success("File uploaded successfully ✅")

    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()
else:
    st.warning("Using Sample Data")

    np.random.seed(42)
    students = [f"Student_{i}" for i in range(1, 21)]
    df = pd.DataFrame({
        'Student': students,
        'Math': np.random.randint(20, 100, 20),
        'Science': np.random.randint(20, 100, 20),
        'English': np.random.randint(20, 100, 20)
    })

# -----------------------
# VALIDATION
# -----------------------
required_cols = ['Student', 'Math', 'Science', 'English']
if not all(col in df.columns for col in required_cols):
    st.error("CSV must contain: Student, Math, Science, English")
    st.stop()

# -----------------------
# ANALYTICS
# -----------------------
df['Average'] = df[['Math', 'Science', 'English']].mean(axis=1)

def grade(avg):
    if avg >= 85:
        return 'A'
    elif avg >= 70:
        return 'B'
    elif avg >= 50:
        return 'C'
    else:
        return 'Fail'

df['Grade'] = df['Average'].apply(grade)
df['Status'] = np.where(df['Average'] >= 50, 'Pass', 'Fail')
df['Rank'] = df['Average'].rank(ascending=False)

df = df.sort_values(by='Average', ascending=False)

# -----------------------
# DASHBOARD
# -----------------------
st.title("📊 Student Performance Dashboard")

c1, c2, c3 = st.columns(3)
c1.metric("Total Students", len(df))
c2.metric("Average Score", round(df['Average'].mean(), 2))
c3.metric("Pass %", f"{(df['Status']=='Pass').mean()*100:.2f}%")

# -----------------------
# SEARCH + FILTER
# -----------------------
search = st.text_input("🔍 Search Student")
grade_filter = st.selectbox("Filter by Grade", ["All", "A", "B", "C", "Fail"])

filtered_df = df.copy()

if search:
    filtered_df = filtered_df[filtered_df['Student'].str.contains(search, case=False)]

if grade_filter != "All":
    filtered_df = filtered_df[filtered_df['Grade'] == grade_filter]

st.subheader("📋 Student Data")
st.dataframe(filtered_df, use_container_width=True)

# -----------------------
# DETAILS
# -----------------------
selected_student = st.selectbox("Select Student", df['Student'])
st.subheader("📌 Student Details")
st.dataframe(df[df['Student'] == selected_student], use_container_width=True)

# -----------------------
# TOPPER & WEAK
# -----------------------
topper = df.iloc[0]
weak_students = df[df['Average'] < 50]

st.subheader("🏆 Top Performer")
st.success(f"{topper['Student']} ({topper['Average']:.2f})")

st.subheader("⚠️ Weak Students")
st.dataframe(weak_students, use_container_width=True)

# -----------------------
# COMPARISON
# -----------------------
st.subheader("⚖️ Compare Students")

col1, col2 = st.columns(2)
s1 = col1.selectbox("Student 1", df['Student'], key="s1")
s2 = col2.selectbox("Student 2", df['Student'], key="s2")

st.dataframe(df[df['Student'].isin([s1, s2])], use_container_width=True)

# -----------------------
# INSIGHTS
# -----------------------
st.subheader("🧠 Insights")

avg_scores = df[['Math', 'Science', 'English']].mean()
st.warning(f"Weakest Subject: {avg_scores.idxmin()}")
st.success(f"Strongest Subject: {avg_scores.idxmax()}")

# -----------------------
# DASHBOARD CHARTS
# -----------------------
st.subheader("📊 Analytics Dashboard")

charts = []

def style_dark(ax, fig):
    ax.set_facecolor('#0E1117')
    fig.patch.set_facecolor('#0E1117')
    ax.tick_params(colors='white')

# Chart 1
fig1, ax1 = plt.subplots(figsize=(5,3))
ax1.bar(df['Student'], df['Average'], color='#4CAF50')
plt.xticks(rotation=45)
style_dark(ax1, fig1)
charts.append(fig1)

# Chart 2
fig2, ax2 = plt.subplots(figsize=(5,3))
df[['Math','Science','English']].plot(ax=ax2)
style_dark(ax2, fig2)
charts.append(fig2)

# Chart 3
fig3, ax3 = plt.subplots(figsize=(5,3))
df['Grade'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax3)
style_dark(ax3, fig3)
charts.append(fig3)

# Chart 4
fig4, ax4 = plt.subplots(figsize=(5,3))
df['Status'].value_counts().plot(kind='bar', ax=ax4)
style_dark(ax4, fig4)
charts.append(fig4)

# AUTO GRID
cols_per_row = 2 if len(charts) <= 4 else 3

for i in range(0, len(charts), cols_per_row):
    cols = st.columns(cols_per_row)
    for j, col in enumerate(cols):
        if i + j < len(charts):
            col.pyplot(charts[i + j])

# -----------------------
# PDF EXPORT (FIXED)
# -----------------------
def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Student Report", ln=True, align='C')

    for _, row in data.iterrows():
        line = f"{row['Student']} | Avg: {row['Average']:.2f} | Grade: {row['Grade']}"
        pdf.cell(200, 10, txt=line, ln=True)

    return bytes(pdf.output(dest='S'))  # ✅ FIXED

st.subheader("📄 Export Report")

st.download_button(
    "⬇️ Download PDF",
    generate_pdf(df),
    "student_report.pdf",
    "application/pdf"
)

# -----------------------
# EXCEL EXPORT
# -----------------------
buffer = io.BytesIO()
df.to_excel(buffer, index=False)

st.download_button(
    "📥 Download Excel",
    buffer.getvalue(),
    "student_report.xlsx"
)