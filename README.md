# Delivery Marketplace Growth Dashboard

![Cury Logo](images/cury.png)

An end-to-end Business Intelligence dashboard built with Python, Streamlit, Plotly, Pandas and Folium to monitor strategic KPIs for a food delivery marketplace.

## Technologies

- Python
- Pandas
- Plotly
- Streamlit
- Folium
- Git
- GitHub

## Skills Demonstrated

- Exploratory Data Analysis (EDA)
- Data Cleaning
- Data Visualization
- KPI Design
- Business Intelligence
- Geospatial Analysis
- Dashboard Development
- Executive Reporting

## Dashboard Preview
(image)

## Project Structure

```
PYTHON_PROJECT_DA/
├── dataset/          # raw and processed data
├── codes_v1/         # auxiliary Python scripts
├── dashboards/        # dashboard assets and views
├── images/            # images used in the project and README (includes cury.png)
├── pages/              # Streamlit multipage app pages
├── Home.py             # main Streamlit entry point
├── requirements.txt
└── README.md
```

> Note: `.ipynb_checkpoints/` is a local Jupyter cache folder and is excluded from version control via `.gitignore`.

# 1. Business Problem

Cury Company is a technology company that has developed a platform that connects restaurants, delivery drivers, and customers.

Through the platform, customers can order meals from registered restaurants and have them delivered to their homes by registered delivery drivers.

As a platform, Cury Company generates a large amount of operational data, including delivery information, order types, weather conditions, driver ratings, and more. Although the business has experienced significant growth, the CEO lacks a centralized view of the company's key performance indicators (KPIs).

You have been hired as a Data Scientist to develop data-driven solutions for the business. Before building predictive models, however, the immediate need is to organize the company's strategic KPIs into a single dashboard, enabling the CEO to monitor business performance and support data-driven decision-making.

Cury Company operates as a marketplace connecting three primary stakeholders:

- Restaurants
- Delivery drivers
- Customers

To monitor business growth, the CEO requested the following metrics.

## Company View

1. Number of orders per day.
2. Number of orders per week.
3. Distribution of orders by traffic conditions.
4. Comparasion of order volume by city and traffic conditions.
5. Number of orders per delivery driver per week.
6. Geographical center of each city by traffic conditions.

## Delivery Driver View

1. Youngest and oldest delivery driver.
2. Best and worst vehicle condition.
3. Average rating per delivery driver.
4. Average rating and standard deviation by traffic conditions.
5. Average rating and standard deviation by weather conditions.
6. Top 10 fastest delivery drivers by city.
7. Top 10 slowest delivery drivers by city.

## Restaurant View

1. Number of unique delivery drivers.
2. Average distance between restaurants and delivery locations.
3. Average delivery time and standard deviation by city.
4. Average delivery time and standard deviation by city and order type.
5. Average delivery time and standard deviation by city and traffic conditions.
6. Average delivery time during festivals.

The objective of this project is to build an interactive dashboard that presents these KPIs in a clear and intuitive way, enabling executive-level decision-making.

---

# 2. Assumptions

- The analysis uses data collected between **February 11-2022, and April 6-2022**.
- The assumed business model is **Marketplace**.
- The analysis focuses on three business perspectives:
  - Company
  - Restaurants
  - Delivery Drivers

---

# 3. Solution Strategy

The dashboard was designed to provide insights across the 3 core business perspectives of the marketplace.

## Company Growth View

- Orders per day
- Percentage of orders by traffic conditions
- Number of orders by city and order type
- Orders per week
- Number of orders by delivery type
- Number of orders by traffic conditions and city type

## Restaurant Growth View

- Number of unique orders
- Average delivery distance
- Average delivery time during festivals and regular days
- Standard deviation of delivery time during festivals and regular days
- Average delivery time by city
- Distribution of average delivery time by city
- Average delivery time by order type

## Delivery Driver Growth View

- Youngest and oldest delivery driver
- Best and worst vehicle condition ratings
- Average rating per delivery driver
- Average rating by traffic conditions
- Average rating by weather conditions
- Average delivery time of the fastest drivers
- Average delivery time of the fastest drivers by city

---

# 4. Top 3 Business Insights

1. Order demand follows a strong daily seasonality, with approximately a **10% variation** between consecutive days.
2. Semi-Urban cities do not experience **Low Traffic** conditions.
3. The largest delivery time variability occurs during **Sunny** weather conditions.

---

# 5. Final Product

Cloud-hosted interactive dashboard accessible from any internet-connected device.

## Live Dashboard

https://curycompany1.streamlit.app/

---

# 6. Conclusion

This project successfully consolidates the company's strategic KPIs into a single dashboard, providing executives with a comprehensive view of business performance.

From the Company View, the analysis indicates a consistent increase in order volume between Week 06 and Week 13 of 2022.

---

# 7. Next Steps

- Simplify the dashboard by reducing the number of displayed metrics.
- Add new filtering options.
- Expand the dashboard with additional business perspectives.
