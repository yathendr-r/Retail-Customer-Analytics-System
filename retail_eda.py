"""
RETAIL CUSTOMER ANALYTICS SYSTEM — Python EDA + Visualizations
Author: Yathendra Kumar Pasumarthi
Tools: Pandas, NumPy, Matplotlib, Seaborn
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────
df = pd.read_csv('Retail_Customer_Dataset.csv')
df.columns = df.columns.str.strip()

# ─────────────────────────────────────
# DATA CLEANING
# ─────────────────────────────────────
print("=" * 55)
print("  RETAIL CUSTOMER ANALYTICS SYSTEM")
print("=" * 55)
print(f"\nTotal Records     : {len(df)}")
print(f"Missing Values    : {df.isnull().sum().sum()}")
print(f"Duplicate Records : {df.duplicated().sum()}")

df.drop_duplicates(inplace=True)
df.dropna(inplace=True)

# Feature Engineering
df['Join_Date'] = pd.to_datetime(df['Join_Date'])
df['Last_Purchase_Date'] = pd.to_datetime(df['Last_Purchase_Date'])
df['Join_Year'] = df['Join_Date'].dt.year
df['Join_Month'] = df['Join_Date'].dt.month
df['Join_Month_Name'] = df['Join_Date'].dt.strftime('%b')

df['Age_Group'] = pd.cut(df['Age'],
    bins=[0, 25, 35, 45, 55, 100],
    labels=['18-25', '26-35', '36-45', '46-55', '55+'])

df['Income_Group'] = pd.cut(df['Annual_Income'],
    bins=[0, 400000, 700000, 1000000, 2000000],
    labels=['Low', 'Medium', 'High', 'Very High'])

# ─────────────────────────────────────
# KEY METRICS
# ─────────────────────────────────────
total_customers = len(df)
avg_purchase    = round(df['Purchase_Amount'].mean(), 2)
total_revenue   = df['Purchase_Amount'].sum()
avg_income      = round(df['Annual_Income'].mean(), 2)
avg_spending    = round(df['Spending_Score'].mean(), 2)
avg_tenure      = round(df['Tenure_Months'].mean(), 1)
male_pct        = round((df['Gender']=='Male').mean()*100, 1)
female_pct      = round((df['Gender']=='Female').mean()*100, 1)

print(f"\n{'─'*55}")
print("  KEY METRICS")
print(f"{'─'*55}")
print(f"  Total Customers      : {total_customers}")
print(f"  Total Revenue        : Rs {total_revenue:,}")
print(f"  Avg Purchase Amount  : Rs {avg_purchase:,}")
print(f"  Avg Annual Income    : Rs {avg_income:,}")
print(f"  Avg Spending Score   : {avg_spending}")
print(f"  Avg Tenure           : {avg_tenure} months")
print(f"  Male Customers       : {male_pct}%")
print(f"  Female Customers     : {female_pct}%")

# Membership Analysis
print(f"\n{'─'*55}")
print("  MEMBERSHIP TYPE ANALYSIS")
print(f"{'─'*55}")
membership = df.groupby('Membership_Type').agg(
    Total=('Customer_ID','count'),
    Avg_Purchase=('Purchase_Amount','mean'),
    Avg_Spending=('Spending_Score','mean'),
    Total_Revenue=('Purchase_Amount','sum')
).reset_index()
membership['Avg_Purchase'] = membership['Avg_Purchase'].round(2)
membership['Avg_Spending'] = membership['Avg_Spending'].round(2)
print(membership.to_string(index=False))

# City Analysis
print(f"\n{'─'*55}")
print("  TOP 5 CITIES BY REVENUE")
print(f"{'─'*55}")
city_rev = df.groupby('City')['Purchase_Amount'].sum().sort_values(ascending=False).head(5)
print(city_rev)

# Category Analysis
print(f"\n{'─'*55}")
print("  PRODUCT CATEGORY ANALYSIS")
print(f"{'─'*55}")
cat = df.groupby('Product_Category').agg(
    Total=('Customer_ID','count'),
    Total_Revenue=('Purchase_Amount','sum'),
    Avg_Purchase=('Purchase_Amount','mean')
).reset_index().sort_values('Total_Revenue', ascending=False)
print(cat.to_string(index=False))

# Age Group Analysis
print(f"\n{'─'*55}")
print("  AGE GROUP ANALYSIS")
print(f"{'─'*55}")
age = df.groupby('Age_Group', observed=True).agg(
    Total=('Customer_ID','count'),
    Avg_Purchase=('Purchase_Amount','mean'),
    Avg_Spending=('Spending_Score','mean')
).reset_index()
print(age.to_string(index=False))

# ─────────────────────────────────────
# VISUALIZATIONS — 12 CHARTS
# ─────────────────────────────────────
sns.set_theme(style="whitegrid")
fig = plt.figure(figsize=(20, 24))
fig.suptitle('Retail Customer Analytics Dashboard\nAuthor: Yathendra Kumar Pasumarthi',
             fontsize=20, fontweight='bold', y=0.98)

# Chart 1 — KPI Cards
ax0 = fig.add_subplot(4, 3, 1)
ax0.axis('off')
kpis = [
    ("Total Customers", str(total_customers)),
    ("Total Revenue", f"Rs {total_revenue//100000}L"),
    ("Avg Purchase", f"Rs {int(avg_purchase):,}"),
    ("Avg Spending Score", str(avg_spending)),
]
for idx, (label, val) in enumerate(kpis):
    y = 0.85 - idx * 0.21
    ax0.text(0.5, y, val, ha='center', fontsize=20,
             fontweight='bold', color='#1F4E79', transform=ax0.transAxes)
    ax0.text(0.5, y-0.09, label, ha='center', fontsize=9,
             color='gray', transform=ax0.transAxes)
ax0.set_title('Key Metrics', fontweight='bold', fontsize=12)

# Chart 2 — Gender Pie
ax1 = fig.add_subplot(4, 3, 2)
gc = df['Gender'].value_counts()
ax1.pie(gc, labels=gc.index, autopct='%1.1f%%',
        colors=['#2E75B6', '#E91E8C'], startangle=90,
        textprops={'fontsize': 11})
ax1.set_title('Gender Distribution', fontweight='bold')

# Chart 3 — Membership Distribution
ax2 = fig.add_subplot(4, 3, 3)
mc = df['Membership_Type'].value_counts()
colors = ['#CD7F32', '#C0C0C0', '#FFD700', '#E5E4E2']
ax2.pie(mc, labels=mc.index, autopct='%1.1f%%',
        colors=colors, startangle=90, textprops={'fontsize': 10})
ax2.set_title('Membership Type Distribution', fontweight='bold')

# Chart 4 — Age Group Distribution
ax3 = fig.add_subplot(4, 3, 4)
ag = df['Age_Group'].value_counts().sort_index()
bars = ax3.bar(ag.index.astype(str), ag.values,
               color='#2E75B6', edgecolor='white')
ax3.set_title('Customer Age Group Distribution', fontweight='bold')
ax3.set_xlabel('Age Group')
ax3.set_ylabel('Number of Customers')
for bar, val in zip(bars, ag.values):
    ax3.text(bar.get_x()+bar.get_width()/2, bar.get_height()+2,
             str(val), ha='center', fontsize=9, fontweight='bold')

# Chart 5 — Top Cities by Revenue
ax4 = fig.add_subplot(4, 3, 5)
city_data = df.groupby('City')['Purchase_Amount'].sum().sort_values(ascending=True).tail(8)
bars = ax4.barh(city_data.index, city_data.values,
                color='#2E75B6', edgecolor='white')
ax4.set_title('Top Cities by Revenue', fontweight='bold')
ax4.set_xlabel('Total Revenue (Rs)')
for bar, val in zip(bars, city_data.values):
    ax4.text(bar.get_width()+1000, bar.get_y()+bar.get_height()/2,
             f'Rs {val//1000}K', va='center', fontsize=8, fontweight='bold')

# Chart 6 — Product Category Revenue
ax5 = fig.add_subplot(4, 3, 6)
cat_rev = df.groupby('Product_Category')['Purchase_Amount'].sum().sort_values(ascending=True)
bars = ax5.barh(cat_rev.index, cat_rev.values,
                color='#16A085', edgecolor='white')
ax5.set_title('Revenue by Product Category', fontweight='bold')
ax5.set_xlabel('Total Revenue (Rs)')

# Chart 7 — Membership vs Avg Purchase
ax6 = fig.add_subplot(4, 3, 7)
mem_purchase = df.groupby('Membership_Type')['Purchase_Amount'].mean().sort_values(ascending=False)
bars = ax6.bar(mem_purchase.index, mem_purchase.values,
               color=['#E5E4E2', '#FFD700', '#C0C0C0', '#CD7F32'],
               edgecolor='white')
ax6.set_title('Avg Purchase by Membership Type', fontweight='bold')
ax6.set_xlabel('Membership Type')
ax6.set_ylabel('Avg Purchase (Rs)')
for bar, val in zip(bars, mem_purchase.values):
    ax6.text(bar.get_x()+bar.get_width()/2, bar.get_height()+100,
             f'Rs {int(val):,}', ha='center', fontsize=8, fontweight='bold')

# Chart 8 — Spending Score Distribution
ax7 = fig.add_subplot(4, 3, 8)
df['Spending_Score'].plot(kind='hist', bins=20,
                          color='#2E75B6', alpha=0.8,
                          edgecolor='white', ax=ax7)
ax7.axvline(df['Spending_Score'].mean(), color='red',
            linestyle='--', linewidth=2,
            label=f'Mean: {avg_spending}')
ax7.set_title('Spending Score Distribution', fontweight='bold')
ax7.set_xlabel('Spending Score')
ax7.legend()

# Chart 9 — Income vs Spending Scatter
ax8 = fig.add_subplot(4, 3, 9)
colors_map = {'Bronze':'#CD7F32', 'Silver':'#C0C0C0',
              'Gold':'#FFD700', 'Platinum':'#E5E4E2'}
for mem, grp in df.groupby('Membership_Type'):
    ax8.scatter(grp['Annual_Income'], grp['Spending_Score'],
                c=colors_map[mem], label=mem, alpha=0.6, s=40)
ax8.set_title('Income vs Spending Score', fontweight='bold')
ax8.set_xlabel('Annual Income (Rs)')
ax8.set_ylabel('Spending Score')
ax8.legend(fontsize=8)

# Chart 10 — Payment Method
ax9 = fig.add_subplot(4, 3, 10)
pm = df['Payment_Method'].value_counts()
ax9.pie(pm, labels=pm.index, autopct='%1.1f%%',
        startangle=90, textprops={'fontsize': 9},
        colors=sns.color_palette('Blues', len(pm)))
ax9.set_title('Payment Method Distribution', fontweight='bold')

# Chart 11 — Customer Acquisition by Year
ax10 = fig.add_subplot(4, 3, 11)
yd = df['Join_Year'].value_counts().sort_index()
ax10.plot(yd.index, yd.values, marker='o',
          color='#2E75B6', linewidth=2.5, markersize=8)
ax10.fill_between(yd.index, yd.values, alpha=0.15, color='#2E75B6')
ax10.set_title('Customer Acquisition by Year', fontweight='bold')
ax10.set_xlabel('Year')
ax10.set_ylabel('New Customers')
for x, y in zip(yd.index, yd.values):
    ax10.text(x, y+1, str(y), ha='center', fontsize=9, fontweight='bold')

# Chart 12 — Correlation Heatmap
ax11 = fig.add_subplot(4, 3, 12)
corr_cols = df[['Age', 'Annual_Income', 'Spending_Score',
                'Purchase_Amount', 'Tenure_Months']]
sns.heatmap(corr_cols.corr(), annot=True, fmt='.2f',
            cmap='Blues', ax=ax11, linewidths=0.5,
            annot_kws={'size': 9})
ax11.set_title('Correlation Heatmap', fontweight='bold')
ax11.tick_params(axis='x', rotation=45)

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig('charts/retail_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()

print("\n✅ Dashboard saved: charts/retail_dashboard.png")
print("✅ EDA Complete!")
