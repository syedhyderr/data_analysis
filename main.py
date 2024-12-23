import pandas as pd

# Load the Excel file to examine its contents
file_path = '/content/Data Analyst Intern Assignment - Excel.xlsx'
excel_data = pd.ExcelFile(file_path)

# Check the sheet names to understand the dataset structure
excel_data.sheet_names


# Correctly load and preview the first few rows of each dataset
user_details = pd.read_excel(file_path, sheet_name='UserDetails.csv')
cooking_sessions = pd.read_excel(file_path, sheet_name='CookingSessions.csv')
order_details = pd.read_excel(file_path, sheet_name='OrderDetails.csv')

# Display the first few rows of each dataset
user_details_preview = user_details.head()
cooking_sessions_preview = cooking_sessions.head()
order_details_preview = order_details.head()

user_details_preview, cooking_sessions_preview, order_details_preview


# Check for missing values in each dataset
missing_values = {
    "UserDetails": user_details.isnull().sum(),
    "CookingSessions": cooking_sessions.isnull().sum(),
    "OrderDetails": order_details.isnull().sum(),
}

# Check for duplicates in each dataset
duplicates = {
    "UserDetails": user_details.duplicated().sum(),
    "CookingSessions": cooking_sessions.duplicated().sum(),
    "OrderDetails": order_details.duplicated().sum(),
}

missing_values, duplicates


# Check for missing values
print("Missing values in UserDetails:")
print(user_details.isnull().sum())

print("\nMissing values in CookingSessions:")
print(cooking_sessions.isnull().sum())

print("\nMissing values in OrderDetails:")
print(order_details.isnull().sum())




# Convert date columns to datetime format
user_details['Registration Date'] = pd.to_datetime(user_details['Registration Date'])
cooking_sessions['Session Start'] = pd.to_datetime(cooking_sessions['Session Start'])
cooking_sessions['Session End'] = pd.to_datetime(cooking_sessions['Session End'])
order_details['Order Date'] = pd.to_datetime(order_details['Order Date'])

# Check for duplicates
print("Duplicate rows in UserDetails:", user_details.duplicated().sum())
print("Duplicate rows in CookingSessions:", cooking_sessions.duplicated().sum())
print("Duplicate rows in OrderDetails:", order_details.duplicated().sum())

# Drop duplicates if found
user_details.drop_duplicates(inplace=True)
cooking_sessions.drop_duplicates(inplace=True)
order_details.drop_duplicates(inplace=True)


# Step 1: Merge UserDetails with CookingSessions on 'User ID'
user_cooking_merged = pd.merge(user_details, cooking_sessions, on='User ID', how='inner')

# Step 2: Merge the result with OrderDetails on 'Session ID'
final_merged_data = pd.merge(user_cooking_merged, order_details, on='Session ID', how='inner')

# Preview the merged dataset
final_merged_preview = final_merged_data.head()
final_merged_preview


# Analyze the relationship between cooking sessions and user orders

# Total number of users
total_users = user_details['User ID'].nunique()

# Users who attended cooking sessions
users_with_sessions = cooking_sessions['User ID'].nunique()

# Users who placed orders
users_with_orders = order_details['User ID'].nunique()

# Percentage of users who attended sessions and placed orders
percentage_sessions = (users_with_sessions / total_users) * 100
percentage_orders = (users_with_orders / total_users) * 100

# Correlation between session ratings and order ratings
correlation = final_merged_data[['Session Rating', 'Rating']].corr().iloc[0, 1]

# Average number of orders for users attending cooking sessions
avg_orders_per_user = (
    final_merged_data.groupby('User ID_x')['Order ID']
    .nunique()
    .mean()
)

# Most cooked dishes during sessions
popular_cooked_dishes = (
    cooking_sessions['Dish Name']
    .value_counts()
    .head(5)
)

# Most ordered dishes
popular_ordered_dishes = (
    order_details['Dish Name']
    .value_counts()
    .head(5)
)

# Results
{
    "total_users": total_users,
    "users_with_sessions": users_with_sessions,
    "users_with_orders": users_with_orders,
    "percentage_sessions": percentage_sessions,
    "percentage_orders": percentage_orders,
    "correlation_ratings": correlation,
    "avg_orders_per_user": avg_orders_per_user,
    "popular_cooked_dishes": popular_cooked_dishes.to_dict(),
    "popular_ordered_dishes": popular_ordered_dishes.to_dict()
}


import matplotlib.pyplot as plt
import seaborn as sns

# Step 2: Demographic Breakdown

# 2.1 Age Distribution
plt.figure(figsize=(10, 6))
sns.histplot(user_details['Age'], kde=True, bins=15)
plt.title('Age Distribution of Users')
plt.xlabel('Age')
plt.ylabel('Number of Users')
plt.show()

# 2.2 Location Distribution
location_counts = user_details['Location'].value_counts().head(10)  # Top 10 locations
plt.figure(figsize=(10, 6))
sns.barplot(x=location_counts.index, y=location_counts.values)
plt.title('Top 10 Locations of Users')
plt.xlabel('Location')
plt.ylabel('Number of Users')
plt.xticks(rotation=45)
plt.show()

# 2.3 Favorite Meal Analysis
meal_counts = user_details['Favorite Meal'].value_counts().head(5)  # Top 5 favorite meals
plt.figure(figsize=(10, 6))
sns.barplot(x=meal_counts.index, y=meal_counts.values)
plt.title('Top 5 Favorite Meals of Users')
plt.xlabel('Favorite Meal')
plt.ylabel('Number of Users')
plt.xticks(rotation=45)
plt.show()


# Step 3: Behavioral Analysis

# 3.1 Total Orders by Age
total_orders_by_age = final_merged_data.groupby('Age')['Order ID'].nunique().reset_index()
plt.figure(figsize=(10, 6))
sns.scatterplot(x=total_orders_by_age['Age'], y=total_orders_by_age['Order ID'])
plt.title('Total Orders by Age')
plt.xlabel('Age')
plt.ylabel('Total Orders')
plt.show()

# 3.2 Total Orders by Location
total_orders_by_location = final_merged_data.groupby('Location')['Order ID'].nunique().reset_index()
top_locations_orders = total_orders_by_location.sort_values(by='Order ID', ascending=False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_locations_orders['Location'], y=top_locations_orders['Order ID'])
plt.title('Total Orders by Location')
plt.xlabel('Location')
plt.ylabel('Total Orders')
plt.xticks(rotation=45)
plt.show()


# Step 4: Correlations and Insights

# Select relevant columns for correlation analysis
correlation_data = final_merged_data[['Age', 'Order ID', 'Session Rating', 'Rating']]
correlation_matrix = correlation_data.corr()

# Plotting the heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix of Demographic and Behavioral Factors')
plt.show()


import matplotlib.pyplot as plt
import seaborn as sns

# 2.1 Age Distribution
plt.figure(figsize=(10, 6))
sns.histplot(user_details['Age'], kde=True, bins=15)
plt.title('Age Distribution of Users')
plt.xlabel('Age')
plt.ylabel('Number of Users')
plt.show()

# 2.2 Location Distribution
location_counts = user_details['Location'].value_counts().head(10)  # Top 10 locations
plt.figure(figsize=(10, 6))
sns.barplot(x=location_counts.index, y=location_counts.values)
plt.title('Top 10 Locations of Users')
plt.xlabel('Location')
plt.ylabel('Number of Users')
plt.xticks(rotation=45)
plt.show()

# 2.3 Favorite Meal Analysis
meal_counts = user_details['Favorite Meal'].value_counts().head(5)  # Top 5 favorite meals
plt.figure(figsize=(10, 6))
sns.barplot(x=meal_counts.index, y=meal_counts.values)
plt.title('Top 5 Favorite Meals of Users')
plt.xlabel('Favorite Meal')
plt.ylabel('Number of Users')
plt.xticks(rotation=45)
plt.show()


# 3.1 Total Orders by Age
total_orders_by_age = final_merged_data.groupby('Age')['Order ID'].nunique().reset_index()
plt.figure(figsize=(10, 6))
sns.scatterplot(x=total_orders_by_age['Age'], y=total_orders_by_age['Order ID'])
plt.title('Total Orders by Age')
plt.xlabel('Age')
plt.ylabel('Total Orders')
plt.show()

# 3.2 Total Orders by Location
total_orders_by_location = final_merged_data.groupby('Location')['Order ID'].nunique().reset_index()
top_locations_orders = total_orders_by_location.sort_values(by='Order ID', ascending=False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_locations_orders['Location'], y=top_locations_orders['Order ID'])
plt.title('Total Orders by Location')
plt.xlabel('Location')
plt.ylabel('Total Orders')
plt.xticks(rotation=45)
plt.show()


# Segment users by Age and calculate total orders per user
age_order_segment = final_merged_data.groupby('Age')['User ID_x'].nunique().reset_index()
age_order_segment['Total Orders'] = final_merged_data.groupby('Age')['Order ID'].nunique().reset_index()['Order ID']

# Segment users by Location and calculate total orders per user
location_order_segment = final_merged_data.groupby('Location')['User ID_x'].nunique().reset_index()
location_order_segment['Total Orders'] = final_merged_data.groupby('Location')['Order ID'].nunique().reset_index()['Order ID']

# Segment users by Favorite Meal and calculate total orders per user
meal_order_segment = final_merged_data.groupby('Favorite Meal')['User ID_x'].nunique().reset_index()
meal_order_segment['Total Orders'] = final_merged_data.groupby('Favorite Meal')['Order ID'].nunique().reset_index()['Order ID']

# Display segments
age_order_segment, location_order_segment, meal_order_segment


# Users who attended more sessions vs. those who attended fewer sessions
session_participation = final_merged_data.groupby('User ID_x')['Session ID'].nunique().reset_index()
session_participation['Order Frequency'] = final_merged_data.groupby('User ID_x')['Order ID'].nunique().reset_index()['Order ID']

# Users attending multiple sessions (more than 2) vs. fewer sessions
multiple_sessions = session_participation[session_participation['Session ID'] > 2]
few_sessions = session_participation[session_participation['Session ID'] <= 2]

# Compare their order frequencies
multiple_sessions_avg_order = multiple_sessions['Order Frequency'].mean()
few_sessions_avg_order = few_sessions['Order Frequency'].mean()

# Display comparison
multiple_sessions_avg_order, few_sessions_avg_order


# Correlation between session rating and order frequency
session_order_correlation = final_merged_data[['Session Rating', 'Order ID']].groupby('Session Rating').nunique()
session_order_correlation['Order Frequency'] = session_order_correlation['Order ID']
session_order_correlation = session_order_correlation[['Order Frequency']]

# Correlation between meal type and order frequency
meal_type_order_correlation = final_merged_data.groupby('Meal Type_y')['Order ID'].nunique().reset_index()
meal_type_order_correlation = meal_type_order_correlation.rename(columns={'Order ID': 'Order Frequency'})

# Display results
session_order_correlation, meal_type_order_correlation


import matplotlib.pyplot as plt
import seaborn as sns

# Plot: Most popular dishes cooked in sessions
plt.figure(figsize=(10, 6))
popular_cooked_dishes.plot(kind='bar', color='skyblue')
plt.title('Most Popular Cooked Dishes in Cooking Sessions')
plt.xlabel('Dish Name')
plt.ylabel('Number of Sessions')
plt.xticks(rotation=45)
plt.show()

# Plot: Most ordered dishes
plt.figure(figsize=(10, 6))
popular_ordered_dishes.plot(kind='bar', color='lightcoral')
plt.title('Most Ordered Dishes')
plt.xlabel('Dish Name')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)
plt.show()

# Correlation heatmap between Session Rating and Order Rating
corr_matrix = final_merged_data[['Session Rating', 'Rating']].corr()
plt.figure(figsize=(6, 4))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Between Session Rating and Order Rating')
plt.show()

# Age vs Total Orders (bar plot)
plt.figure(figsize=(10, 6))
age_order_segment.plot(kind='bar', x='Age', y='Total Orders', color='lightgreen')
plt.title('Total Orders vs. Age Group')
plt.xlabel('Age Group')
plt.ylabel('Total Orders')
plt.xticks(rotation=45)
plt.show()

# Location vs Total Orders (bar plot)
plt.figure(figsize=(10, 6))
location_order_segment.plot(kind='bar', x='Location', y='Total Orders', color='lightblue')
plt.title('Total Orders vs. Location')
plt.xlabel('Location')
plt.ylabel('Total Orders')
plt.xticks(rotation=45)
plt.show()
