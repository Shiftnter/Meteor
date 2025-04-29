import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import numpy as np

# Load and clean the data
df = pd.read_csv("weather_forecast.csv")

# Convert data types
df['Datetime'] = pd.to_datetime(df['Datetime'], errors='coerce')
df['Temperature (°C)'] = pd.to_numeric(df['Temperature (°C)'], errors='coerce')
df['Humidity (%)'] = pd.to_numeric(df['Humidity (%)'], errors='coerce')

# Rename for simplicity
df.rename(columns={
    'Temperature (°C)': 'temp',
    'Humidity (%)': 'humidity',
    'Weather Description': 'description',
    'City': 'city',
    'Datetime': 'date'
}, inplace=True)

# Drop missing values
df = df.dropna(subset=['temp', 'humidity'])

# ----------- Skewness Fix (Log Transform) -----------
# Add 1 to avoid log(0)
df['temp'] = np.log1p(df['temp'])
df['humidity'] = np.log1p(df['humidity'])

# ----------- Scaling -----------
scaler = MinMaxScaler()
df[['temp', 'humidity']] = scaler.fit_transform(df[['temp', 'humidity']])

# ----------- Classification Setup -----------
# Create binary label: 1 if temp > 0.5, else 0
df['temp_class'] = (df['temp'] > 0.5).astype(int)

# ----------- Train Classifier -----------
X = df[['humidity']]  # You can add more features like 'description' if encoded
y = df['temp_class']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

# ----------- Heatmap of Correlation -----------
plt.figure(figsize=(6, 4))
sns.heatmap(df[['temp', 'humidity']].corr(), annot=True, cmap='coolwarm')
plt.title("Feature Correlation")
plt.tight_layout()
plt.show()

# ----------- Confusion Matrix -----------
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Low Temp", "High Temp"])
disp.plot(cmap="Blues")
plt.title("Confusion Matrix (Decision Tree)")
plt.show()
