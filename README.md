# Performance Dashboard

This project is a Performance Dashboard built using Streamlit, Prophet, Plotly, and other libraries. It loads data from an Excel file, displays key performance metrics, and generates predictions for future performance using trained Prophet models. Additionally, it allows users to generate and download a PDF report of the performance data.

## Features

- Load and preprocess performance data from an Excel file.
- Display key performance metrics.
- Generate interactive bar charts for various metrics.
- Predict future performance using trained Prophet models.
- Generate and download a PDF report of the performance data and user commentaries.

## Requirements

- Python 3.7+
- pandas
- plotly
- joblib
- prophet
- matplotlib
- seaborn
- reportlab
- streamlit
- python-dotenv

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/performance-dashboard.git
    cd performance-dashboard
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the project directory and add the following line with the path to your Excel file:

    ```plaintext
    EXCEL_FILE_PATH=C:/Users/19452/Downloads/Performance Detail (1).xlsx
    ```

## Usage

1. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

2. Open your web browser and go to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Use the sidebar filters to select the date range and input the estimated spend for the next week.

4. View the performance metrics, interactive charts, and make predictions for the next week.

5. Add commentaries for each metric and generate a PDF report by clicking the "Generate PDF Report" button.

## Deployment

To deploy this application to a cloud platform such as AWS, follow these steps:

### Deploy to AWS (Elastic Beanstalk)

1. Install the AWS Elastic Beanstalk CLI:

    ```bash
    pip install awsebcli
    ```

2. Initialize your Elastic Beanstalk application:

    ```bash
    eb init -p python-3.7 performance-dashboard
    ```

3. Create an Elastic Beanstalk environment:

    ```bash
    eb create performance-dashboard-env
    ```

4. Deploy the application:

    ```bash
    eb deploy
    ```

5. Set the environment variable for the Excel file path in Elastic Beanstalk:

    ```bash
    eb setenv EXCEL_FILE_PATH=/path/to/your_excel_file.xlsx
    ```

6. Open the deployed app in your web browser:

    ```bash
    eb open
    ```

## Video Demonstration

For a video demonstration of the application, please watch this YouTube video:

[![Performance Dashboard Demo](https://img.youtube.com/vi/Dwd0LCfZY_I/0.jpg)](https://youtu.be/Dwd0LCfZY_I)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Streamlit: https://streamlit.io/
- Prophet: https://facebook.github.io/prophet/
- Plotly: https://plotly.com/python/
- ReportLab: https://www.reportlab.com/
