import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

def create_synthetic_dataset():
    np.random.seed(42)
    # Generate 500 samples
    n_samples = 500
    
    # NPK values typically range from 0 to 140
    # Temperature 10 to 45 C
    # Humidity 20 to 100
    # pH 4.5 to 8.5
    
    crops = ['Rice', 'Maize', 'Chickpea', 'Kidneybeans', 'Pigeonpeas', 
             'Mothbeans', 'Mungbean', 'Blackgram', 'Lentil', 'Pomegranate', 
             'Banana', 'Mango', 'Grapes', 'Watermelon', 'Muskmelon', 
             'Apple', 'Orange', 'Papaya', 'Coconut', 'Cotton', 'Jute', 'Coffee']
    
    data = []
    for _ in range(n_samples):
        crop = np.random.choice(crops)
        
        # Base stats depending roughly on crop type to make it somewhat realistic
        if crop in ['Rice', 'Jute', 'Papaya', 'Coconut']:
            n = np.random.randint(60, 100)
            p = np.random.randint(35, 60)
            k = np.random.randint(35, 55)
            temperature = np.random.uniform(20.0, 35.0)
            humidity = np.random.uniform(70.0, 95.0)
            ph = np.random.uniform(5.5, 7.5)
        elif crop in ['Apple', 'Grapes']:
            n = np.random.randint(10, 40)
            p = np.random.randint(120, 145)
            k = np.random.randint(195, 205)
            temperature = np.random.uniform(10.0, 25.0)
            humidity = np.random.uniform(80.0, 95.0)
            ph = np.random.uniform(5.5, 6.5)
        else:
            n = np.random.randint(0, 140)
            p = np.random.randint(5, 145)
            k = np.random.randint(5, 205)
            temperature = np.random.uniform(10.0, 40.0)
            humidity = np.random.uniform(20.0, 100.0)
            ph = np.random.uniform(4.5, 8.5)
            
        data.append([n, p, k, temperature, humidity, ph, crop])
        
    df = pd.DataFrame(data, columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'label'])
    df.to_csv('dataset.csv', index=False)
    print("dataset.csv created successfully.")
    return df

def train_and_save_model():
    print("Loading data...")
    df = create_synthetic_dataset()
    
    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph']]
    y = df['label']
    
    print("Training RandomForestClassifier...")
    # Initialize the RandomForestClassifier
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y)
    
    # Save the trained model to model.pkl
    joblib.dump(rf, 'model.pkl')
    print("model.pkl saved successfully.")

if __name__ == '__main__':
    train_and_save_model()
