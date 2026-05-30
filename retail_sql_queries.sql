CREATE DATABASE retail_db;
USE retail_db;

CREATE TABLE customers (
    Customer_ID VARCHAR(10),
    Gender VARCHAR(10),
    Age INT,
    City VARCHAR(50),
    State VARCHAR(50),
    Annual_Income INT,
    Spending_Score INT,
    Membership_Type VARCHAR(20),
    Product_Category VARCHAR(30),
    Purchase_Amount INT,
    Payment_Method VARCHAR(20),
    Join_Date DATE,
    Last_Purchase_Date DATE,
    Tenure_Months INT
);
USE retail_db;
SELECT COUNT(*) FROM customers;

SELECT Gender, COUNT(*) AS Total_Customers
FROM customers
GROUP BY Gender;

SELECT Membership_Type,
COUNT(*) AS Total_Customers,
ROUND(AVG(Purchase_Amount), 2) AS Avg_Purchase,
SUM(Purchase_Amount) AS Total_Revenue
FROM customers
GROUP BY Membership_Type
ORDER BY Total_Revenue DESC;

SELECT City,
COUNT(*) AS Total_Customers,
SUM(Purchase_Amount) AS Total_Revenue
FROM customers
GROUP BY City
ORDER BY Total_Revenue DESC
LIMIT 5;

SELECT Product_Category,
COUNT(*) AS Total_Orders,
SUM(Purchase_Amount) AS Total_Revenue,
ROUND(AVG(Purchase_Amount), 2) AS Avg_Purchase
FROM customers
GROUP BY Product_Category
ORDER BY Total_Revenue DESC;

SELECT Payment_Method,
COUNT(*) AS Total_Transactions,
ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM customers), 1) AS Percentage
FROM customers
GROUP BY Payment_Method
ORDER BY Total_Transactions DESC;

SELECT 
CASE
    WHEN Age BETWEEN 18 AND 25 THEN '18-25'
    WHEN Age BETWEEN 26 AND 35 THEN '26-35'
    WHEN Age BETWEEN 36 AND 45 THEN '36-45'
    WHEN Age BETWEEN 46 AND 55 THEN '46-55'
    ELSE '55+'
END AS Age_Group,
COUNT(*) AS Total_Customers,
ROUND(AVG(Purchase_Amount), 2) AS Avg_Purchase,
ROUND(AVG(Spending_Score), 2) AS Avg_Spending_Score
FROM customers
GROUP BY Age_Group
ORDER BY Avg_Purchase DESC;

SELECT Customer_ID, Gender, Age, City,
Annual_Income, Purchase_Amount, Spending_Score
FROM customers
WHERE Membership_Type = 'Platinum'
ORDER BY Purchase_Amount DESC
LIMIT 10;

SELECT State,
COUNT(*) AS Total_Customers,
SUM(Purchase_Amount) AS Total_Revenue,
ROUND(AVG(Purchase_Amount), 2) AS Avg_Purchase
FROM customers
GROUP BY State
ORDER BY Total_Revenue DESC;

SELECT 
CASE
    WHEN Annual_Income < 400000 THEN 'Low'
    WHEN Annual_Income < 700000 THEN 'Medium'
    WHEN Annual_Income < 1000000 THEN 'High'
    ELSE 'Very High'
END AS Income_Group,
COUNT(*) AS Total_Customers,
ROUND(AVG(Spending_Score), 2) AS Avg_Spending_Score,
ROUND(AVG(Purchase_Amount), 2) AS Avg_Purchase
FROM customers
GROUP BY Income_Group
ORDER BY Avg_Purchase DESC;

SELECT Gender, Membership_Type,
COUNT(*) AS Total,
ROUND(AVG(Purchase_Amount), 2) AS Avg_Purchase
FROM customers
GROUP BY Gender, Membership_Type
ORDER BY Gender, Avg_Purchase DESC;

SELECT Customer_ID, Gender, Age, City,
Membership_Type, Purchase_Amount, Tenure_Months
FROM customers
WHERE Tenure_Months > 36
ORDER BY Tenure_Months DESC
LIMIT 10;