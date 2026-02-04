
import sys
sys.path.append("/content/AI-Data-Analyzer-App")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from ai_analyzer.data_loader import load_data
from ai_analyzer.data_cleaner import handle_missing_values
from ai_analyzer.profiler import profile_data
from ai_analyzer.stats_analyzer import compute_statistics
from ai_analyzer.anomaly_detector import detect_anomalies
from ai_analyzer.insight_generator import generate_insights

st.set_page_config(page_title="AI Data Analyzer", layout="wide")
st.title("📊 AI Data Analyzer System")

uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv","xlsx"])

if uploaded_file:
    df = load_data(uploaded_file)
    df = handle_missing_values(df)
    profile = profile_data(df)
    stats = compute_statistics(df)
    df = detect_anomalies(df, profile["Numeric Columns"])
    insights = generate_insights(stats, df)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Overview", "Visuals", "AI Report", "Downloads"]
    )

    with tab1:
        st.json(profile)
        st.dataframe(df.head())

    with tab2:
        for col in profile["Numeric Columns"]:
            fig, ax = plt.subplots()
            sns.histplot(df[col], kde=True, ax=ax)
            st.pyplot(fig)

    with tab3:
        st.text(insights)

    with tab4:
        st.download_button(
            "Download CSV",
            df.to_csv(index=False).encode("utf-8"),
            "analyzed_data.csv",
            "text/csv"
        )

        excel_buf = BytesIO()
        with pd.ExcelWriter(excel_buf, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Data")
            pd.DataFrame(stats).T.to_excel(writer, sheet_name="Stats")

        st.download_button(
            "Download Excel",
            excel_buf.getvalue(),
            "analysis.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        pdf_buf = BytesIO()
        c = canvas.Canvas(pdf_buf, pagesize=A4)
        text = c.beginText(40, 800)
        for line in insights.split("\n"):
            text.textLine(line)
        c.drawText(text)
        c.save()

        st.download_button(
            "Download PDF",
            pdf_buf.getvalue(),
            "analysis.pdf",
            "application/pdf"
        )

