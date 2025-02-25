# Coronavirus Data Analysis Dashboard

This is a **Dash** web application that visualizes COVID-19 data using **Plotly**, **Pandas**, and **Bootstrap** for styling. The dashboard displays total cases, active cases, recovered cases, and deaths, along with a bar chart for state-wise COVID-19 case distribution.

## Features
- **Total COVID-19 cases summary** (Total, Active, Recovered, Deaths)
- **Interactive Bar Chart** to display cases based on selected category (All, Hospitalized, Recovered, Deceased)
- **Bootstrap Styling** for a responsive layout

## Technologies Used
- **Python**
- **Dash** (by Plotly)
- **Pandas**
- **Plotly Graph Objects**
- **Bootstrap CSS**

## Installation & Setup

### 1. Clone the Repository
```sh
git clone https://github.com/your-username/corona-dashboard.git
cd corona-dashboard
```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```

### 3. Run the Application
```sh
python app.py
```

The dashboard will be accessible at **http://127.0.0.1:8050/** in your browser.

## Project Structure
```
corona-dashboard/
│── Dataset/
│   └── IndividualDetails.csv
│── app.py
│── requirements.txt
│── README.md
```

## Dataset
The project requires a dataset (`IndividualDetails.csv`) that contains COVID-19 cases information, including:
- **detected_state**: State where the case was detected
- **current_status**: Hospitalized, Recovered, or Deceased

Ensure that the dataset is placed in the `Dataset/` folder before running the application.

## Contributing
Contributions are welcome! Feel free to fork the repository and submit a pull request.

## License
This project is open-source under the **MIT License**.

---
Made with ❤️ using Dash and Plotly.

