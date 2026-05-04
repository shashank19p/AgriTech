# Python Project – Smart Crop Advisory System for Small and Marginal Farmers

Welcome to the Smart Crop Advisory System! This application uses Machine Learning to recommend the best crop for your soil and environment, alongside making practical fertilizer suggestions. It also includes an integration with the OpenWeatherMap API for live checking of weather metrics in any given city.

## 📁 Project Structure

```
crop-project/
│
├── app.py               # Main Streamlit UI Code
├── model.pkl            # Trained RandomForestClassifier Model
├── dataset.csv          # Sample dataset used for training the model
├── utils.py             # Helper module for fertilizer and weather API logic
├── train_model.py       # Script used to generate synthetic dataset and train the model
├── requirements.txt     # Python Dependencies
├── README.md            # Documentation
```

## ⚙️ How to Run the Project

1. **Install Dependencies:**
   Open your terminal in this directory and run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate the Model (If `model.pkl` is missing):**
   If you want to re-train the model or regenerate the dataset:
   ```bash
   python train_model.py
   ```

3. **Run the Streamlit Application:**
   Start the user interface:
   ```bash
   streamlit run app.py
   ```

## 🌟 Features
* **Crop Recommendation:** Fast prediction using a trained `RandomForestClassifier` interpreting Nitrogen, Phosphorus, Potassium, Temperature, Humidity, and pH.
* **Fertilizer Guidance:** Tailored suggestions mapping your soil NPK value to fertilizers like Urea, MOP, or DAP.
* **Weather Insights:** Input your city and see current weather and humidity pulled from the OpenWeatherMap API. (Add your API key inside the sidebar!).
* **Bonus - Leaf Disease Check:** A mock file uploader showing how you could integrate a computer-vision endpoint for crop health analysis!

## 🧪 Sample Input & Output

**Sample Input:**
- Nitrogen = 45
- Phosphorus = 45
- Potassium = 45
- Temperature = 27
- Humidity = 85
- pH = 6.2

**Sample Output:**
- ✅ **Recommended Crop:** Rice
- 💊 **Fertilizer Suggestion:** NPK 19:19:19 (Balanced) (since N,P,K all are below 80, showing slightly lower nutrient levels needing balance, or other based on algorithm logic limits)

Enjoy the application! 🌱🌾
