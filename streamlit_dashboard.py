import os
import pandas as pd
import plotly.express as px
import joblib
from prophet import Prophet
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import io
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the environment variable
excel_file_path = os.getenv('EXCEL_FILE_PATH')

# Load Trained Prophet Models
#@st.cache_data
def load_trained_models():
    model_bookings = joblib.load('model_bookings.pkl')
    model_cpb = joblib.load('model_cpb.pkl')
    model_impressions = joblib.load('model_impressions.pkl')
    return model_bookings, model_cpb, model_impressions

# Load and preprocess the data
# Load the data from the data source
def load_data():
    data = pd.read_excel(excel_file_path)
    data['Date'] = pd.to_datetime(data['Date'])
    data = data[data['Date'] >= '2023-03-01']
    return data


# Function to calculate main metrics
def calculate_metrics(df):
    return {
        'Total Spend': f"${df['Spend'].sum():,.2f}",
        'Total Impressions': f"{df['Impressions'].sum():,.2f}",
        'Total Bookings': f"{df['Bookings'].sum():.2f}",
        'Average Cost Per Booking (CPB)': f"${df['CPB'].mean():.2f}",
        'Average Cost Per Click (CPC)': f"${df['CPC'].mean():.2f}",
    }

# Function to make predictions for the next week and return forecast dataframe
def make_week_predictions(model, future_periods=7):
    future = model.make_future_dataframe(periods=future_periods)
    future['Spend'] = estimated_spend  # Use the estimated spend value
    forecast = model.predict(future)
    fig = px.line(forecast, x='ds', y='yhat', labels={'ds': 'Date', 'yhat': 'Prediction'})
    fig.update_layout(title='Prediction', xaxis_title='Date', yaxis_title='Value')
    fig.update_traces(line=dict(color='RoyalBlue'))
    return fig, forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

# Streamlit UI Components
st.sidebar.title("Filters")

excel_data = load_data()
min_date, max_date = excel_data['Date'].min(), excel_data['Date'].max()
start_date = st.sidebar.date_input('Start date', value=min_date.date(), min_value=min_date.date(), max_value=max_date.date())
end_date = st.sidebar.date_input('End date', value=max_date.date(), min_value=min_date.date(), max_value=max_date.date())

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

filtered_data = excel_data[(excel_data['Date'] >= start_date) & (excel_data['Date'] <= end_date)]

st.title('Performance Dashboard')

# Display main metrics
main_metrics = calculate_metrics(filtered_data)
for metric, value in main_metrics.items():
    st.metric(label=metric, value=value)

# Load the models
model_bookings, model_cpb, model_impressions = load_trained_models()

# Initialize a dictionary to store user commentaries
user_commentaries = {}

# Interactive Bar Charts
def create_interactive_bar_chart(df, metric):
    return px.bar(df, x='Date', y=metric, color='Channel', title=f"{metric} Over Time")

# Display Interactive Bar Charts for selected metrics and collect commentaries
for metric in ['Spend', 'Impressions', 'Bookings', 'CPB', 'CPC']:
    if metric in filtered_data.columns:
        chart = create_interactive_bar_chart(filtered_data, metric)
        st.plotly_chart(chart, use_container_width=True)
        user_commentary = st.text_area(f"Commentary for {metric}", key=f"commentary_{metric}")
        user_commentaries[metric] = user_commentary


estimated_spend = st.sidebar.number_input('Estimated Spend for Next Week', min_value=0)

# Generate and display predictions for the next week
if st.button('Predict for the Next Week'):
    st.subheader("Predictions for the Next Week")

    chart_bookings, forecast_bookings = make_week_predictions(model_bookings)
    st.plotly_chart(chart_bookings, use_container_width=True)
    st.dataframe(forecast_bookings)

    chart_cpb, forecast_cpb = make_week_predictions(model_cpb)
    st.plotly_chart(chart_cpb, use_container_width=True)
    st.dataframe(forecast_cpb)

    chart_impressions, forecast_impressions = make_week_predictions(model_impressions)
    st.plotly_chart(chart_impressions, use_container_width=True)
    st.dataframe(forecast_impressions)

# Function to generate a PDF report
def generate_pdf_report(filtered_data, start_date, end_date, commentaries, main_metrics):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    def add_page():
        nonlocal y_position
        p.showPage()
        y_position = height - 60

    y_position = height - 60
    p.setFont("Helvetica-Bold", 18)
    p.drawString(72, y_position, "Performance Dashboard Report")
    y_position -= 30
    p.setFont("Helvetica", 12)
    p.drawString(72, y_position, f"Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    y_position -= 20

    # Add main metrics to the PDF
    y_position -= 20
    p.drawString(72, y_position, "Main Metrics:")
    y_position -= 15
    for metric, value in main_metrics.items():
        if y_position < 100:
            add_page()
        y_position -= 20
        p.drawString(72, y_position, f"{metric}: {value}")
    y_position -= 20
    if y_position < 100:
        add_page()
    p.setStrokeColor(colors.black)
    p.line(72, y_position, width - 72, y_position)
    y_position -= 20

    for metric in ['Spend', 'Impressions', 'Bookings', 'CPB', 'CPC']:
        if metric in filtered_data.columns:
            commentary = commentaries.get(metric, "")
            if commentary:
                if y_position < 100:
                    add_page()
                y_position -= 30
                p.drawString(72, y_position, f"Commentary for {metric}:")
                y_position -= 15
                text_object = p.beginText(72, y_position)
                text_object.textLines(commentary)
                p.drawText(text_object)
                y_position = text_object.getY() - 20
            if y_position < 240:
                add_page()

            plt.figure(figsize=(8, 4))
            sns.barplot(x='Date', y=metric, data=filtered_data, ci=None)
            plt.title(f"{metric} Over Time")
            plt.xticks(rotation=45)
            plt.tight_layout()

            temp_image_path = f"{metric}.png"
            plt.savefig(temp_image_path)
            plt.close()

            y_position -= 30
            p.drawString(72, y_position, f"{metric} Over Time:")
            y_position -= 220
            p.drawImage(temp_image_path, 72, y_position, width=400, height=200)
            y_position -= 40

            os.remove(temp_image_path)

    p.save()
    buffer.seek(0)
    return buffer

# Generate and Download PDF Report
if st.button('Generate PDF Report'):
    main_metrics = calculate_metrics(filtered_data)  # Calculate main metrics for the selected date range
    pdf_report_buffer = generate_pdf_report(filtered_data, start_date, end_date, user_commentaries, main_metrics)
    st.download_button(
        label='Download PDF Report',
        data=pdf_report_buffer,
        file_name='dashboard_report.pdf',
        mime='application/pdf'
    )