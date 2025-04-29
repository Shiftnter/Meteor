import pandas as pd
import numpy as np
from sklearn.preprocessing import PowerTransformer
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv("weather_forecast_cleaned.csv")

# Optionally visualize original distributions
sns.histplot(df['temp'], kde=True).set(title='Temperature Before Skew Fix')
plt.show()
sns.histplot(df['humidity'], kde=True).set(title='Humidity Before Skew Fix')
plt.show()

# Apply log transformation to reduce skewness (only on positive values)
df['temp_log'] = np.log1p(df['temp'])
df['humidity_log'] = np.log1p(df['humidity'])

# OR use PowerTransformer (Yeo-Johnson handles 0/negative values)
pt = PowerTransformer(method='yeo-johnson')
df[['temp_skew_fixed', 'humidity_skew_fixed']] = pt.fit_transform(df[['temp', 'humidity']])

# Optional: visualize after transformation
sns.histplot(df['temp_skew_fixed'], kde=True).set(title='Temperature After Skew Fix')
plt.show()
sns.histplot(df['humidity_skew_fixed'], kde=True).set(title='Humidity After Skew Fix')
plt.show()

# Save the transformed data
df.to_csv("weather_forecast_transformed.csv", index=False)
