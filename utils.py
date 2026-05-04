import requests


CROP_GUIDE = {
    "Rice": {
        "watering": "Keep the field consistently moist. In normal conditions, irrigate lightly every 1-2 days.",
        "panchagavya_litre_per_acre": 3.0,
        "vermicompost_kg_per_acre": 2000,
        "booster_components": ["Azolla compost", "Neem cake", "Farmyard manure", "Jeevamrutham"],
        "crop_advice": "Maintain standing moisture during early growth and avoid water stress during tillering and flowering.",
    },
    "Maize": {
        "watering": "Provide moderate irrigation every 4-5 days, and increase during tasseling and cob formation.",
        "panchagavya_litre_per_acre": 2.5,
        "vermicompost_kg_per_acre": 1500,
        "booster_components": ["Vermiwash", "Neem cake", "Bone meal", "Compost tea"],
        "crop_advice": "Keep the root zone loose and well-drained. Moisture is most important during flowering and grain filling.",
    },
    "Chickpea": {
        "watering": "Use light irrigation every 8-10 days only when the soil becomes dry. Avoid overwatering.",
        "panchagavya_litre_per_acre": 2.0,
        "vermicompost_kg_per_acre": 1000,
        "booster_components": ["Rhizobium culture", "Wood ash", "Compost", "Phosphate-rich organic manure"],
        "crop_advice": "Too much water reduces performance. Keep the field aerated and support root nodulation with organic inoculants.",
    },
    "Kidneybeans": {
        "watering": "Water every 5-6 days with moderate depth. Do not allow waterlogging.",
        "panchagavya_litre_per_acre": 2.0,
        "vermicompost_kg_per_acre": 1200,
        "booster_components": ["Rhizobium culture", "Vermicompost", "Neem cake", "Seaweed extract"],
        "crop_advice": "Focus on balanced moisture and improve flowering with foliar organic sprays.",
    },
    "Pigeonpeas": {
        "watering": "Usually water every 7-10 days in dry periods. Reduce irrigation once the crop is established.",
        "panchagavya_litre_per_acre": 2.0,
        "vermicompost_kg_per_acre": 1000,
        "booster_components": ["Farmyard manure", "Jeevamrutham", "Rhizobium culture", "Neem cake"],
        "crop_advice": "Pigeonpea does well with moderate moisture and deep root development. Avoid excess irrigation.",
    },
    "Mothbeans": {
        "watering": "Give light irrigation every 7-8 days only if rainfall is insufficient.",
        "panchagavya_litre_per_acre": 1.5,
        "vermicompost_kg_per_acre": 800,
        "booster_components": ["Compost", "Wood ash", "Neem cake", "Biofertilizer inoculants"],
        "crop_advice": "This crop tolerates dry conditions well. Keep irrigation light and infrequent.",
    },
    "Mungbean": {
        "watering": "Irrigate every 5-7 days with light watering. Avoid heavy wetting at flowering.",
        "panchagavya_litre_per_acre": 1.5,
        "vermicompost_kg_per_acre": 800,
        "booster_components": ["Rhizobium culture", "Vermiwash", "Compost tea", "Neem cake"],
        "crop_advice": "Support pod set with steady but not excessive moisture and a light foliar organic spray.",
    },
    "Blackgram": {
        "watering": "Water every 5-7 days depending on heat. Keep the soil moist but never soggy.",
        "panchagavya_litre_per_acre": 1.5,
        "vermicompost_kg_per_acre": 900,
        "booster_components": ["Compost", "Rhizobium culture", "Wood ash", "Neem cake"],
        "crop_advice": "Use organic matter to improve soil life and avoid water stagnation.",
    },
    "Lentil": {
        "watering": "A light irrigation every 8-10 days is usually enough in dry weather.",
        "panchagavya_litre_per_acre": 1.5,
        "vermicompost_kg_per_acre": 900,
        "booster_components": ["Phosphate-rich organic manure", "Compost", "Rhizobium culture", "Wood ash"],
        "crop_advice": "Lentil performs best in cool, lightly moist soil with low to moderate irrigation.",
    },
    "Pomegranate": {
        "watering": "Water deeply every 5-7 days and maintain consistent moisture during fruit development.",
        "panchagavya_litre_per_acre": 3.0,
        "vermicompost_kg_per_acre": 2500,
        "booster_components": ["Vermicompost", "Banana pseudostem extract", "Neem cake", "Fish amino acid"],
        "crop_advice": "Mulching and regular organic feeding improve fruit size, sweetness, and plant strength.",
    },
    "Banana": {
        "watering": "Banana needs frequent water. Irrigate every 2-3 days in hot weather.",
        "panchagavya_litre_per_acre": 3.0,
        "vermicompost_kg_per_acre": 3000,
        "booster_components": ["Vermicompost", "Panchagavya", "Banana waste compost", "Neem cake"],
        "crop_advice": "Heavy feeding and steady moisture are important. Mulch around the base to reduce water loss.",
    },
    "Mango": {
        "watering": "Water young trees every 5-7 days. Mature trees need deeper watering every 7-10 days in dry months.",
        "panchagavya_litre_per_acre": 2.5,
        "vermicompost_kg_per_acre": 2000,
        "booster_components": ["Farmyard manure", "Neem cake", "Fish amino acid", "Jeevamrutham"],
        "crop_advice": "Focus on deep root moisture, mulching, and organic micronutrient support near flowering.",
    },
    "Grapes": {
        "watering": "Provide controlled irrigation every 3-4 days and avoid excess moisture near harvest.",
        "panchagavya_litre_per_acre": 3.0,
        "vermicompost_kg_per_acre": 2500,
        "booster_components": ["Vermicompost", "Seaweed extract", "Neem cake", "Compost tea"],
        "crop_advice": "Pruning, drainage, and well-timed organic feeding are key for vine vigor and fruit quality.",
    },
    "Watermelon": {
        "watering": "Irrigate every 3-4 days early on, then maintain steady moisture during fruit set.",
        "panchagavya_litre_per_acre": 2.5,
        "vermicompost_kg_per_acre": 1800,
        "booster_components": ["Vermicompost", "Bone meal", "Seaweed extract", "Compost tea"],
        "crop_advice": "Avoid irregular watering because it can affect fruit development and sweetness.",
    },
    "Muskmelon": {
        "watering": "Water every 3-4 days, then reduce slightly near maturity to improve fruit quality.",
        "panchagavya_litre_per_acre": 2.5,
        "vermicompost_kg_per_acre": 1800,
        "booster_components": ["Vermicompost", "Neem cake", "Seaweed extract", "Wood ash"],
        "crop_advice": "Keep irrigation even in the fruiting stage and support the soil with rich compost.",
    },
    "Apple": {
        "watering": "Deep watering every 6-7 days is usually enough, depending on temperature and soil type.",
        "panchagavya_litre_per_acre": 2.5,
        "vermicompost_kg_per_acre": 2200,
        "booster_components": ["Farmyard manure", "Bone meal", "Neem cake", "Compost tea"],
        "crop_advice": "Healthy orchard mulch and seasonal organic feeding improve flowering and fruit retention.",
    },
    "Orange": {
        "watering": "Water every 5-6 days and maintain stable moisture during flowering and fruit set.",
        "panchagavya_litre_per_acre": 2.5,
        "vermicompost_kg_per_acre": 2200,
        "booster_components": ["Vermicompost", "Neem cake", "Fish amino acid", "Compost tea"],
        "crop_advice": "Citrus responds well to organic matter around the drip line and regular mulching.",
    },
    "Papaya": {
        "watering": "Give light irrigation every 2-3 days. Papaya prefers frequent moisture without stagnation.",
        "panchagavya_litre_per_acre": 3.0,
        "vermicompost_kg_per_acre": 2500,
        "booster_components": ["Vermicompost", "Panchagavya", "Neem cake", "Jeevamrutham"],
        "crop_advice": "Papaya is a quick feeder, so small frequent organic applications work better than one heavy dose.",
    },
    "Coconut": {
        "watering": "Water deeply every 4-7 days depending on age, temperature, and soil moisture.",
        "panchagavya_litre_per_acre": 3.0,
        "vermicompost_kg_per_acre": 3000,
        "booster_components": ["Cocopeat compost", "Neem cake", "Vermicompost", "Seaweed extract"],
        "crop_advice": "Apply organic matter around the basin and mulch heavily to preserve soil moisture.",
    },
    "Cotton": {
        "watering": "Irrigate every 5-6 days and avoid excess water during boll development.",
        "panchagavya_litre_per_acre": 2.5,
        "vermicompost_kg_per_acre": 1500,
        "booster_components": ["Neem cake", "Vermicompost", "Compost tea", "Fish amino acid"],
        "crop_advice": "Balanced organic nutrition and controlled irrigation support stronger bolls and fiber quality.",
    },
    "Jute": {
        "watering": "Keep the soil evenly moist. In dry spells, water every 3-4 days.",
        "panchagavya_litre_per_acre": 2.5,
        "vermicompost_kg_per_acre": 1800,
        "booster_components": ["Farmyard manure", "Jeevamrutham", "Neem cake", "Vermicompost"],
        "crop_advice": "Jute responds well to moisture-retentive soil rich in decomposed organic matter.",
    },
    "Coffee": {
        "watering": "Water every 5-7 days in dry weather and maintain mulch to protect root moisture.",
        "panchagavya_litre_per_acre": 2.5,
        "vermicompost_kg_per_acre": 2000,
        "booster_components": ["Compost", "Neem cake", "Fish amino acid", "Vermicompost"],
        "crop_advice": "Shade, mulch, and gradual organic feeding are important for sustained coffee productivity.",
    },
}

DEFAULT_CROP_GUIDE = {
    "watering": "Irrigate based on soil moisture and crop stage. In general, provide moderate watering every 4-6 days and avoid waterlogging.",
    "panchagavya_litre_per_acre": 2.5,
    "vermicompost_kg_per_acre": 1500,
    "booster_components": ["Vermicompost", "Neem cake", "Compost tea", "Farmyard manure"],
    "crop_advice": "Maintain good organic matter, mulch the soil, and adjust watering based on weather and crop age.",
}

REGION_SPECIFIC_TIPS = {
    "Andhra Pradesh": "Favour moisture conservation and monitor heat stress in coastal and delta zones.",
    "Punjab": "Balanced irrigation and residue management are important for intensive farming regions.",
    "Tamil Nadu": "Plan irrigation carefully because many belts depend on tank water and variable rainfall.",
}

SOIL_SEASON_RULES = {
    "Rice": {"seasons": ["Kharif"], "soils": ["Alluvial", "Black"]},
    "Maize": {"seasons": ["Kharif", "Rabi", "Summer"], "soils": ["Alluvial", "Black", "Red"]},
    "Cotton": {"seasons": ["Kharif"], "soils": ["Black"]},
    "Chickpea": {"seasons": ["Rabi"], "soils": ["Black", "Alluvial"]},
    "Lentil": {"seasons": ["Rabi"], "soils": ["Alluvial", "Black"]},
    "Banana": {"seasons": ["Kharif", "Summer"], "soils": ["Alluvial", "Red"]},
    "Mango": {"seasons": ["Summer"], "soils": ["Red", "Alluvial"]},
    "Pigeonpeas": {"seasons": ["Kharif"], "soils": ["Black", "Red"]},
}

CROP_PRICES = {
    "Rice": 2400,
    "Maize": 2200,
    "Chickpea": 5400,
    "Kidneybeans": 6200,
    "Pigeonpeas": 7000,
    "Mothbeans": 4800,
    "Mungbean": 7600,
    "Blackgram": 7400,
    "Lentil": 6000,
    "Pomegranate": 9000,
    "Banana": 1800,
    "Mango": 3500,
    "Grapes": 4200,
    "Watermelon": 1600,
    "Muskmelon": 2200,
    "Apple": 8000,
    "Orange": 3600,
    "Papaya": 2500,
    "Coconut": 2800,
    "Cotton": 7200,
    "Jute": 4700,
    "Coffee": 9500,
}

DISEASE_LIBRARY = {
    "Rice": [
        {"name": "Blast", "remedy": "Use clean seed, avoid excess nitrogen, and spray recommended fungicide if symptoms spread."},
        {"name": "Bacterial Leaf Blight", "remedy": "Improve drainage, avoid water stagnation, and remove severely affected leaves."},
        {"name": "Brown Spot", "remedy": "Maintain balanced nutrition and apply fungicide only when infection becomes serious."},
    ],
    "Maize": [
        {"name": "Leaf Blight", "remedy": "Maintain spacing, reduce leaf wetness, and use disease-tolerant seed if available."},
        {"name": "Rust", "remedy": "Remove infected leaves early and spray fungicide when rust spreads rapidly."},
        {"name": "Downy Mildew", "remedy": "Use treated seed and avoid repeated cropping in the same field."},
    ],
    "Cotton": [
        {"name": "Leaf Curl", "remedy": "Control whiteflies, remove infected plants, and keep the field weed-free."},
        {"name": "Wilt", "remedy": "Improve drainage and avoid growing cotton continuously in the same plot."},
        {"name": "Root Rot", "remedy": "Use seed treatment and avoid excess irrigation."},
    ],
    "Banana": [
        {"name": "Sigatoka", "remedy": "Remove infected leaves and maintain good air movement between plants."},
        {"name": "Panama Wilt", "remedy": "Use disease-free suckers and prevent water movement from infected fields."},
        {"name": "Bunchy Top", "remedy": "Control aphids and remove infected clumps immediately."},
    ],
    "Mango": [
        {"name": "Anthracnose", "remedy": "Prune crowded branches and spray fungicide before flowering if disease is common."},
        {"name": "Powdery Mildew", "remedy": "Monitor new flush and flowering stage closely and use sulfur-based spray when needed."},
        {"name": "Die Back", "remedy": "Trim infected twigs and apply protective paste on cut surfaces."},
    ],
}

DEFAULT_DISEASES = [
    {"name": "Leaf Spot", "remedy": "Remove affected leaves and avoid overhead irrigation when possible."},
    {"name": "Root Rot", "remedy": "Improve drainage and avoid excess watering around the root zone."},
    {"name": "Nutrient Stress", "remedy": "Apply balanced nutrients and monitor fresh leaf growth for recovery."},
]

BASE_UI_TRANSLATIONS = {
    "Crop Recommendation": {"Telugu": "పంట సిఫార్సు", "Hindi": "फसल सिफारिश", "Tamil": "பயிர் பரிந்துரை", "Kannada": "ಬೆಳೆ ಶಿಫಾರಸು"},
    "Disease Detection": {"Telugu": "వ్యాధి గుర్తింపు", "Hindi": "रोग पहचान", "Tamil": "நோய் கண்டறிதல்", "Kannada": "ರೋಗ ಪತ್ತೆ"},
    "Market Info": {"Telugu": "మార్కెట్ సమాచారం", "Hindi": "बाज़ार जानकारी", "Tamil": "சந்தை தகவல்", "Kannada": "ಮಾರುಕಟ್ಟೆ ಮಾಹಿತಿ"},
    "Recommended Crop": {"Telugu": "సిఫార్సు చేసిన పంట", "Hindi": "सिफारिश की गई फसल", "Tamil": "பரிந்துரைக்கப்பட்ட பயிர்", "Kannada": "ಶಿಫಾರಸು ಮಾಡಿದ ಬೆಳೆ"},
    "Fertilizer Advice": {"Telugu": "ఎరువు సలహా", "Hindi": "उर्वरक सलाह", "Tamil": "உர பரிந்துரை", "Kannada": "ರಸಗೊಬ್ಬರ ಸಲಹೆ"},
    "Organic Farming Plan": {"Telugu": "సేంద్రియ వ్యవసాయ ప్రణాళిక", "Hindi": "जैविक खेती योजना", "Tamil": "இயற்கை விவசாய திட்டம்", "Kannada": "ಸಾವಯವ ಕೃಷಿ ಯೋಜನೆ"},
    "State Advice": {"Telugu": "రాష్ట్ర ఆధారిత సలహా", "Hindi": "राज्य आधारित सलाह", "Tamil": "மாநில அடிப்படையிலான ஆலோசனை", "Kannada": "ರಾಜ್ಯ ಆಧಾರಿತ ಸಲಹೆ"},
    "Season Fit": {"Telugu": "సీజన్ అనుకూలత", "Hindi": "मौसम उपयुक्तता", "Tamil": "பருவ பொருத்தம்", "Kannada": "ಋತು ಹೊಂದಿಕೆ"},
    "Soil Fit": {"Telugu": "నేల అనుకూలత", "Hindi": "मिट्टी उपयुक्तता", "Tamil": "மண் பொருத்தம்", "Kannada": "ಮಣ್ಣಿನ ಹೊಂದಿಕೆ"},
    "Estimated Market Price": {"Telugu": "అంచనా మార్కెట్ ధర", "Hindi": "अनुमानित बाज़ार मूल्य", "Tamil": "மதிப்பிடப்பட்ட சந்தை விலை", "Kannada": "ಅಂದಾಜು ಮಾರುಕಟ್ಟೆ ಬೆಲೆ"},
    "Why this crop?": {"Telugu": "ఈ పంట ఎందుకు?", "Hindi": "यह फसल क्यों?", "Tamil": "ஏன் இந்த பயிர்?", "Kannada": "ಈ ಬೆಳೆ ಏಕೆ?"},
    "Weather Alerts": {"Telugu": "వాతావరణ హెచ్చరికలు", "Hindi": "मौसम चेतावनी", "Tamil": "வானிலை எச்சரிக்கைகள்", "Kannada": "ಹವಾಮಾನ ಎಚ್ಚರಿಕೆಗಳು"},
    "Possible Diseases": {"Telugu": "సంభావ్య వ్యాధులు", "Hindi": "संभावित रोग", "Tamil": "சாத்தியமான நோய்கள்", "Kannada": "ಸಂಭಾವ್ಯ ರೋಗಗಳು"},
    "Remedy": {"Telugu": "పరిష్కారం", "Hindi": "उपाय", "Tamil": "தீர்வு", "Kannada": "ಉಪಾಯ"},
    "No crop predicted yet.": {"Telugu": "ఇంకా పంట అంచనా వేయబడలేదు.", "Hindi": "अभी तक कोई फसल अनुमानित नहीं हुई है।", "Tamil": "இன்னும் பயிர் கணிக்கப்படவில்லை.", "Kannada": "ಇನ್ನೂ ಬೆಳೆ ಊಹಿಸಲಾಗಿಲ್ಲ."},
    "Good fit": {"Telugu": "మంచి అనుకూలత", "Hindi": "अच्छा मेल", "Tamil": "நல்ல பொருத்தம்", "Kannada": "ಉತ್ತಮ ಹೊಂದಿಕೆ"},
    "Moderate fit": {"Telugu": "మధ్యస్థ అనుకూలత", "Hindi": "मध्यम मेल", "Tamil": "மிதமான பொருத்தம்", "Kannada": "ಮಧ್ಯಮ ಹೊಂದಿಕೆ"},
    "Check suitability": {"Telugu": "అనుకూలతను తనిఖీ చేయండి", "Hindi": "उपयुक्तता जांचें", "Tamil": "பொருத்தத்தை சரிபார்க்கவும்", "Kannada": "ಹೊಂದಿಕೆಯನ್ನು ಪರಿಶೀಲಿಸಿ"},
    "Weather Panel": {"Telugu": "వాతావరణ ప్యానల్", "Hindi": "मौसम पैनल", "Tamil": "வானிலை பகுதி", "Kannada": "ಹವಾಮಾನ ಫಲಕ"},
    "Smart Crop Advisory System": {"Telugu": "స్మార్ట్ పంట సలహా వ్యవస్థ", "Hindi": "स्मार्ट क्रॉप सलाह प्रणाली", "Tamil": "ஸ்மார்ட் பயிர் ஆலோசனை அமைப்பு", "Kannada": "ಸ್ಮಾರ್ಟ್ ಬೆಳೆ ಸಲಹಾ ವ್ಯವಸ್ಥೆ"},
    "City Name:": {"Telugu": "నగరం పేరు:", "Hindi": "शहर का नाम:", "Tamil": "நகரின் பெயர்:", "Kannada": "ನಗರದ ಹೆಸರು:"},
    "OpenWeather API Key:": {"Telugu": "ఓపెన్‌వెదర్ API కీ:", "Hindi": "ओपनवेदर API कुंजी:", "Tamil": "OpenWeather API விசை:", "Kannada": "OpenWeather API ಕೀಲಿ:"},
    "Check Forecast": {"Telugu": "వాతావరణాన్ని చూడండి", "Hindi": "पूर्वानुमान देखें", "Tamil": "முன்னறிவிப்பைப் பார்க்கவும்", "Kannada": "ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ ನೋಡಿ"},
    "Temperature": {"Telugu": "ఉష్ణోగ్రత", "Hindi": "तापमान", "Tamil": "வெப்பநிலை", "Kannada": "ತಾಪಮಾನ"},
    "Humidity": {"Telugu": "తేమ", "Hindi": "आर्द्रता", "Tamil": "ஈரப்பதம்", "Kannada": "ಆದ್ರತೆ"},
    "Condition:": {"Telugu": "పరిస్థితి:", "Hindi": "स्थिति:", "Tamil": "நிலை:", "Kannada": "ಸ್ಥಿತಿ:"},
    "Showing default demo weather because no API key was provided.": {"Telugu": "API కీ ఇవ్వనందున డిఫాల్ట్ డెమో వాతావరణం చూపబడుతోంది.", "Hindi": "API कुंजी न होने के कारण डिफ़ॉल्ट डेमो मौसम दिखाया जा रहा है।", "Tamil": "API விசை வழங்கப்படாததால் இயல்புநிலை காட்சி வானிலை காட்டப்படுகிறது.", "Kannada": "API ಕೀ ನೀಡದ ಕಾರಣ ಡೀಫಾಲ್ಟ್ ಡೆಮೋ ಹವಾಮಾನವನ್ನು ತೋರಿಸಲಾಗುತ್ತಿದೆ."},
    "Language": {"Telugu": "భాష", "Hindi": "भाषा", "Tamil": "மொழி", "Kannada": "ಭಾಷೆ"},
    "This system supports farmer decisions, not replaces them.": {"Telugu": "ఈ వ్యవస్థ రైతుల నిర్ణయాలకు సహాయం చేస్తుంది, వాటిని భర్తీ చేయదు.", "Hindi": "यह प्रणाली किसान के निर्णयों में मदद करती है, उनकी जगह नहीं लेती।", "Tamil": "இந்த அமைப்பு விவசாயியின் முடிவுகளுக்கு உதவுகிறது, அவற்றை மாற்றாது.", "Kannada": "ಈ ವ್ಯವಸ್ಥೆ ರೈತರ ನಿರ್ಧಾರಗಳಿಗೆ ನೆರವಾಗುತ್ತದೆ, ಅವನ್ನು ಬದಲಾಯಿಸುವುದಿಲ್ಲ."},
    "Model file `model.pkl` is not loaded. Please run the training script before generating prediction.": {"Telugu": "`model.pkl` మోడల్ ఫైల్ లోడ్ కాలేదు. అంచనా వేయడానికి ముందు ట్రైనింగ్ స్క్రిప్ట్ నడపండి.", "Hindi": "`model.pkl` मॉडल फ़ाइल लोड नहीं हुई। भविष्यवाणी से पहले प्रशिक्षण स्क्रिप्ट चलाएँ।", "Tamil": "`model.pkl` மாடல் கோப்பு ஏற்றப்படவில்லை. கணிப்பிற்கு முன் பயிற்சி ஸ்கிரிப்டை இயக்கவும்.", "Kannada": "`model.pkl` ಮಾದರಿ ಫೈಲ್ ಲೋಡ್ ಆಗಿಲ್ಲ. ಊಹಿಸುವ ಮೊದಲು ತರಬೇತಿ ಸ್ಕ್ರಿಪ್ಟ್ ಅನ್ನು ಚಾಲನೆ ಮಾಡಿ."},
    "Model file `model.pkl` not found. Please run the training script.": {"Telugu": "`model.pkl` మోడల్ ఫైల్ కనబడలేదు. దయచేసి ట్రైనింగ్ స్క్రిప్ట్ నడపండి.", "Hindi": "`model.pkl` मॉडल फ़ाइल नहीं मिली। कृपया प्रशिक्षण स्क्रिप्ट चलाएँ।", "Tamil": "`model.pkl` மாடல் கோப்பு கிடைக்கவில்லை. தயவுசெய்து பயிற்சி ஸ்கிரிப்டை இயக்கவும்.", "Kannada": "`model.pkl` ಮಾದರಿ ಫೈಲ್ ಕಂಡುಬಂದಿಲ್ಲ. ದಯವಿಟ್ಟು ತರಬೇತಿ ಸ್ಕ್ರಿಪ್ಟ್ ಅನ್ನು ಚಾಲನೆ ಮಾಡಿ."},
    "Step 1: Location + Season": {"Telugu": "దశ 1: ప్రదేశం + సీజన్", "Hindi": "चरण 1: स्थान + मौसम", "Tamil": "படி 1: இடம் + பருவம்", "Kannada": "ಹಂತ 1: ಸ್ಥಳ + ಋತು"},
    "Step 2: Soil + NPK": {"Telugu": "దశ 2: నేల + NPK", "Hindi": "चरण 2: मिट्टी + NPK", "Tamil": "படி 2: மண் + NPK", "Kannada": "ಹಂತ 2: ಮಣ್ಣು + NPK"},
    "Step 3: Generate": {"Telugu": "దశ 3: రూపొందించండి", "Hindi": "चरण 3: तैयार करें", "Tamil": "படி 3: உருவாக்கவும்", "Kannada": "ಹಂತ 3: ರಚಿಸಿ"},
    "State": {"Telugu": "రాష్ట్రం", "Hindi": "राज्य", "Tamil": "மாநிலம்", "Kannada": "ರಾಜ್ಯ"},
    "Season": {"Telugu": "సీజన్", "Hindi": "मौसम", "Tamil": "பருவம்", "Kannada": "ಋತು"},
    "Land Area (acres)": {"Telugu": "భూమి విస్తీర్ణం (ఎకరాలు)", "Hindi": "भूमि क्षेत्रफल (एकड़)", "Tamil": "நில அளவு (ஏக்கர்)", "Kannada": "ಭೂಮಿ ವಿಸ್ತೀರ್ಣ (ಏಕರ್)"},
    "Soil Type": {"Telugu": "నేల రకం", "Hindi": "मिट्टी का प्रकार", "Tamil": "மண் வகை", "Kannada": "ಮಣ್ಣಿನ ಪ್ರಕಾರ"},
    "Nitrogen (N)": {"Telugu": "నత్రజని (N)", "Hindi": "नाइट्रोजन (N)", "Tamil": "நைட்ரஜன் (N)", "Kannada": "ನೈಟ್ರೋಜನ್ (N)"},
    "Phosphorus (P)": {"Telugu": "ఫాస్ఫరస్ (P)", "Hindi": "फॉस्फोरस (P)", "Tamil": "பாஸ்பரஸ் (P)", "Kannada": "ಫಾಸ್ಫರಸ್ (P)"},
    "Potassium (K)": {"Telugu": "పొటాషియం (K)", "Hindi": "पोटैशियम (K)", "Tamil": "பொட்டாசியம் (K)", "Kannada": "ಪೊಟ್ಯಾಸಿಯಂ (K)"},
    "Temperature (°C)": {"Telugu": "ఉష్ణోగ్రత (°C)", "Hindi": "तापमान (°C)", "Tamil": "வெப்பநிலை (°C)", "Kannada": "ತಾಪಮಾನ (°C)"},
    "Humidity (%)": {"Telugu": "తేమ (%)", "Hindi": "आर्द्रता (%)", "Tamil": "ஈரப்பதம் (%)", "Kannada": "ಆದ್ರತೆ (%)"},
    "Soil pH Level": {"Telugu": "నేల pH స్థాయి", "Hindi": "मिट्टी pH स्तर", "Tamil": "மண் pH நிலை", "Kannada": "ಮಣ್ಣಿನ pH ಮಟ್ಟ"},
    "🌱 Soil Details": {"Telugu": "🌱 నేల వివరాలు", "Hindi": "🌱 मिट्टी विवरण", "Tamil": "🌱 மண் விவரங்கள்", "Kannada": "🌱 ಮಣ್ಣಿನ ವಿವರಗಳು"},
    "🌤️ Weather Details": {"Telugu": "🌤️ వాతావరణ వివరాలు", "Hindi": "🌤️ मौसम विवरण", "Tamil": "🌤️ வானிலை விவரங்கள்", "Kannada": "🌤️ ಹವಾಮಾನ ವಿವರಗಳು"},
    "Adjust values based on your soil test report": {"Telugu": "మీ నేల పరీక్ష నివేదిక ఆధారంగా విలువలను సర్దండి", "Hindi": "अपने मिट्टी परीक्षण रिपोर्ट के अनुसार मान समायोजित करें", "Tamil": "உங்கள் மண் பரிசோதனை அறிக்கையின் அடிப்படையில் மதிப்புகளை அமைக்கவும்", "Kannada": "ನಿಮ್ಮ ಮಣ್ಣಿನ ಪರೀಕ್ಷಾ ವರದಿ ಆಧರಿಸಿ ಮೌಲ್ಯಗಳನ್ನು ಹೊಂದಿಸಿ"},
    "Use local climate or weather panel values for better guidance": {"Telugu": "మంచి సలహా కోసం స్థానిక వాతావరణం లేదా వెదర్ ప్యానల్ విలువలను వాడండి", "Hindi": "बेहतर सलाह के लिए स्थानीय मौसम या वेदर पैनल मानों का उपयोग करें", "Tamil": "சிறந்த வழிகாட்டலுக்கு உள்ளூர் காலநிலை அல்லது வானிலை மதிப்புகளை பயன்படுத்துங்கள்", "Kannada": "ಉತ್ತಮ ಸಲಹೆಗಾಗಿ ಸ್ಥಳೀಯ ಹವಾಮಾನ ಅಥವಾ ವೆದರ್ ಪ್ಯಾನಲ್ ಮೌಲ್ಯಗಳನ್ನು ಬಳಸಿ"},
    "Get Smart Recommendation": {"Telugu": "స్మార్ట్ సిఫార్సు పొందండి", "Hindi": "स्मार्ट सिफारिश प्राप्त करें", "Tamil": "ஸ்மார்ட் பரிந்துரையை பெறுங்கள்", "Kannada": "ಸ್ಮಾರ್ಟ್ ಶಿಫಾರಸು ಪಡೆಯಿರಿ"},
    "Analyzing data...": {"Telugu": "డేటాను విశ్లేషిస్తోంది...", "Hindi": "डेटा का विश्लेषण हो रहा है...", "Tamil": "தரவு பகுப்பாய்வு செய்யப்படுகிறது...", "Kannada": "ಡೇಟಾವನ್ನು ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ..."},
    "Recommendation generated successfully!": {"Telugu": "సిఫార్సు విజయవంతంగా రూపొందించబడింది!", "Hindi": "सिफारिश सफलतापूर्वक तैयार हुई!", "Tamil": "பரிந்துரை வெற்றிகரமாக உருவாக்கப்பட்டது!", "Kannada": "ಶಿಫಾರಸು ಯಶಸ್ವಿಯಾಗಿ ಸಿದ್ಧವಾಗಿದೆ!"},
    "Read Recommendation Aloud": {"Telugu": "సిఫార్సును శబ్దంగా చదవండి", "Hindi": "सिफारिश को आवाज़ में सुनें", "Tamil": "பரிந்துரையை சத்தமாக கேளுங்கள்", "Kannada": "ಶಿಫಾರಸನ್ನು ಜೋರಾಗಿ ಕೇಳಿ"},
    "pyttsx3 is not installed. Run `pip install pyttsx3` to enable voice output.": {"Telugu": "pyttsx3 ఇన్‌స్టాల్ కాలేదు. వాయిస్ అవుట్‌పుట్ కోసం `pip install pyttsx3` నడపండి.", "Hindi": "pyttsx3 इंस्टॉल नहीं है। वॉइस आउटपुट के लिए `pip install pyttsx3` चलाएँ।", "Tamil": "pyttsx3 நிறுவப்படவில்லை. ஒலி வெளியீட்டுக்கு `pip install pyttsx3` இயக்கவும்.", "Kannada": "pyttsx3 ಇನ್‌ಸ್ಟಾಲ್ ಆಗಿಲ್ಲ. ಧ್ವನಿ ಔಟ್‌ಪುಟ್‌ಗೆ `pip install pyttsx3` ಚಾಲನೆ ಮಾಡಿ."},
    "Voice output played on the local machine.": {"Telugu": "వాయిస్ అవుట్‌పుట్ లోకల్ మెషీన్‌లో ప్లే చేయబడింది.", "Hindi": "वॉइस आउटपुट स्थानीय मशीन पर चलाया गया।", "Tamil": "ஒலி வெளியீடு உள்ளூர் கணினியில் ஒலிக்கப்பட்டது.", "Kannada": "ಧ್ವನಿ ಔಟ್‌ಪುಟ್ ಸ್ಥಳೀಯ ಯಂತ್ರದಲ್ಲಿ ಪ್ಲೇ ಮಾಡಲಾಗಿದೆ."},
    "Voice output failed:": {"Telugu": "వాయిస్ అవుట్‌పుట్ విఫలమైంది:", "Hindi": "वॉइस आउटपुट विफल:", "Tamil": "ஒலி வெளியீடு தோல்வியடைந்தது:", "Kannada": "ಧ್ವನಿ ಔಟ್‌ಪುಟ್ ವಿಫಲವಾಗಿದೆ:"},
    "Top 3 Crop Suggestions": {"Telugu": "టాప్ 3 పంట సూచనలు", "Hindi": "शीर्ष 3 फसल सुझाव", "Tamil": "முதல் 3 பயிர் பரிந்துரைகள்", "Kannada": "ಟಾಪ್ 3 ಬೆಳೆ ಸಲಹೆಗಳು"},
    "Best Match": {"Telugu": "ఉత్తమ ఎంపిక", "Hindi": "सर्वश्रेष्ठ विकल्प", "Tamil": "சிறந்த தேர்வு", "Kannada": "ಅತ್ಯುತ್ತಮ ಆಯ್ಕೆ"},
    "Alternative 1": {"Telugu": "ప్రత్యామ్నాయం 1", "Hindi": "विकल्प 1", "Tamil": "மாற்று 1", "Kannada": "ಪರ್ಯಾಯ 1"},
    "Alternative 2": {"Telugu": "ప్రత్యామ్నాయం 2", "Hindi": "विकल्प 2", "Tamil": "மாற்று 2", "Kannada": "ಪರ್ಯಾಯ 2"},
    "Model confidence:": {"Telugu": "మోడల్ నమ్మకం:", "Hindi": "मॉडल भरोसा:", "Tamil": "மாதிரி நம்பிக்கை:", "Kannada": "ಮಾದರಿ ವಿಶ್ವಾಸ:"},
    "Rule-based backup suggestion": {"Telugu": "రూల్-బేస్డ్ ప్రత్యామ్నాయ సూచన", "Hindi": "नियम-आधारित बैकअप सुझाव", "Tamil": "விதி அடிப்படையிலான மாற்று பரிந்துரை", "Kannada": "ನಿಯಮ ಆಧಾರಿತ ಬ್ಯಾಕಪ್ ಸಲಹೆ"},
    "Region:": {"Telugu": "ప్రాంతం:", "Hindi": "क्षेत्र:", "Tamil": "பகுதி:", "Kannada": "ಪ್ರದೇಶ:"},
    "Suitability Summary:": {"Telugu": "అనుకూలత సారాంశం:", "Hindi": "उपयुक्तता सारांश:", "Tamil": "பொருத்த சுருக்கம்:", "Kannada": "ಹೊಂದಿಕೆಯ ಸಾರಾಂಶ:"},
    "Crop Advice for": {"Telugu": "పంట సలహా", "Hindi": "फसल सलाह", "Tamil": "பயிர் ஆலோசனை", "Kannada": "ಬೆಳೆ ಸಲಹೆ"},
    "Watering:": {"Telugu": "నీటిపారుదల:", "Hindi": "सिंचाई:", "Tamil": "நீர்ப்பாய்ச்சி:", "Kannada": "ನೀರಾವರಿ:"},
    "Field Guidance:": {"Telugu": "పొలం మార్గదర్శకం:", "Hindi": "खेत मार्गदर्शन:", "Tamil": "புலம் வழிகாட்டல்:", "Kannada": "ಹೊಲ ಮಾರ್ಗದರ್ಶನ:"},
    "Best Organic Components:": {"Telugu": "మంచి సేంద్రియ భాగాలు:", "Hindi": "श्रेष्ठ जैविक घटक:", "Tamil": "சிறந்த இயற்கை கூறுகள்:", "Kannada": "ಉತ್ತಮ ಸಾವಯವ ಅಂಶಗಳು:"},
    "Calculated for": {"Telugu": "లెక్కించబడింది", "Hindi": "गणना की गई", "Tamil": "கணக்கிடப்பட்டது", "Kannada": "ಲೆಕ್ಕಿಸಲಾಗಿದೆ"},
    "acre(s).": {"Telugu": "ఎకరాలకు.", "Hindi": "एकड़ के लिए।", "Tamil": "ஏக்கருக்கு.", "Kannada": "ಏಕರಿಗೆ."},
    "Panchagavya schedule:": {"Telugu": "పంచగవ్య షెడ్యూల్:", "Hindi": "पंचगव्य समय-सारणी:", "Tamil": "பஞ்சகவ்ய அட்டவணை:", "Kannada": "ಪಂಚಗವ್ಯ ವೇಳಾಪಟ್ಟಿ:"},
    "Vermicompost schedule:": {"Telugu": "వెర్మీ కంపోస్ట్ షెడ్యూల్:", "Hindi": "वर्मी कम्पोस्ट समय-सारणी:", "Tamil": "வெர்மிகம்போஸ்ட் அட்டவணை:", "Kannada": "ವರ್ಮಿಕಂಪೋಸ್ಟ್ ವೇಳಾಪಟ್ಟಿ:"},
    "No major weather warning based on the current weather panel values.": {"Telugu": "ప్రస్తుత వాతావరణ ప్యానల్ విలువల ఆధారంగా ప్రధాన హెచ్చరిక లేదు.", "Hindi": "वर्तमान मौसम मानों के आधार पर कोई बड़ी चेतावनी नहीं है।", "Tamil": "தற்போதைய வானிலை மதிப்புகளின் அடிப்படையில் பெரிய எச்சரிக்கை இல்லை.", "Kannada": "ಪ್ರಸ್ತುತ ಹವಾಮಾನ ಮೌಲ್ಯಗಳ ಆಧಾರದಲ್ಲಿ ಪ್ರಮುಖ ಎಚ್ಚರಿಕೆ ಇಲ್ಲ."},
    "This section explains the recommendation using your NPK, temperature, humidity, pH, season, soil, and location inputs.": {"Telugu": "ఈ విభాగం మీ NPK, ఉష్ణోగ్రత, తేమ, pH, సీజన్, నేల, మరియు ప్రదేశం ఆధారంగా సిఫార్సును వివరిస్తుంది.", "Hindi": "यह भाग आपके NPK, तापमान, आर्द्रता, pH, मौसम, मिट्टी और स्थान के आधार पर सिफारिश समझाता है।", "Tamil": "இந்த பகுதி உங்கள் NPK, வெப்பநிலை, ஈரப்பதம், pH, பருவம், மண் மற்றும் இடத்தை அடிப்படையாக கொண்டு பரிந்துரையை விளக்குகிறது.", "Kannada": "ಈ ವಿಭಾಗವು ನಿಮ್ಮ NPK, ತಾಪಮಾನ, ಆದ್ರತೆ, pH, ಋತು, ಮಣ್ಣು ಮತ್ತು ಸ್ಥಳವನ್ನು ಆಧರಿಸಿ ಶಿಫಾರಸನ್ನು ವಿವರಿಸುತ್ತದೆ."},
    "Upload a crop leaf image": {"Telugu": "పంట ఆకు చిత్రాన్ని అప్‌లోడ్ చేయండి", "Hindi": "फसल पत्ती की छवि अपलोड करें", "Tamil": "பயிர் இலை படத்தை பதிவேற்றவும்", "Kannada": "ಬೆಳೆ ಎಲೆಯ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ"},
    "Uploaded crop image": {"Telugu": "అప్‌లోడ్ చేసిన పంట చిత్రం", "Hindi": "अपलोड की गई फसल छवि", "Tamil": "பதிவேற்றப்பட்ட பயிர் படம்", "Kannada": "ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ ಬೆಳೆ ಚಿತ್ರ"},
    "Generate a crop recommendation first to unlock crop-based disease suggestions.": {"Telugu": "పంట ఆధారిత వ్యాధి సూచనలు చూడాలంటే ముందుగా పంట సిఫార్సు రూపొందించండి.", "Hindi": "फसल-आधारित रोग सुझाव देखने के लिए पहले फसल सिफारिश तैयार करें।", "Tamil": "பயிர் அடிப்படையிலான நோய் பரிந்துரைகளை பார்க்க முதலில் பயிர் பரிந்துரையை உருவாக்கவும்.", "Kannada": "ಬೆಳೆ ಆಧಾರಿತ ರೋಗ ಸಲಹೆಗಳನ್ನು ನೋಡಲು ಮೊದಲು ಬೆಳೆ ಶಿಫಾರಸು ಪಡೆಯಿರಿ."},
    "Based on your crop, these diseases are most likely.": {"Telugu": "మీ పంట ఆధారంగా ఈ వ్యాధులు ఎక్కువగా సంభవించే అవకాశముంది.", "Hindi": "आपकी फसल के आधार पर ये रोग सबसे अधिक संभावित हैं।", "Tamil": "உங்கள் பயிரை அடிப்படையாகக் கொண்டு இந்த நோய்கள் அதிகம் ஏற்படலாம்.", "Kannada": "ನಿಮ್ಮ ಬೆಳೆಯನ್ನು ಆಧರಿಸಿ ಈ ರೋಗಗಳು ಹೆಚ್ಚು ಸಂಭವಿಸಬಹುದು."},
    "Student-project note: this is rule-based advisory linked to the predicted crop. The image upload is included for the SIH-style workflow.": {"Telugu": "విద్యార్థి ప్రాజెక్ట్ గమనిక: ఇది అంచనా వేసిన పంటకు అనుసంధానమైన రూల్-బేస్డ్ సలహా. SIH తరహా వర్క్‌ఫ్లో కోసం చిత్రం అప్‌లోడ్ కూడా చేర్చబడింది.", "Hindi": "छात्र परियोजना नोट: यह अनुमानित फसल से जुड़ी नियम-आधारित सलाह है। SIH शैली कार्यप्रवाह के लिए छवि अपलोड शामिल है।", "Tamil": "மாணவர் திட்ட குறிப்பு: இது கணிக்கப்பட்ட பயிருடன் இணைக்கப்பட்ட விதி அடிப்படையிலான ஆலோசனை. SIH பாணி செயல்முறைக்காக படம் பதிவேற்றம் சேர்க்கப்பட்டுள்ளது.", "Kannada": "ವಿದ್ಯಾರ್ಥಿ ಯೋಜನೆ ಟಿಪ್ಪಣಿ: ಇದು ಊಹಿಸಲಾದ ಬೆಳೆಗೆ ಸಂಬಂಧಿಸಿದ ನಿಯಮ ಆಧಾರಿತ ಸಲಹೆಯಾಗಿದೆ. SIH ಶೈಲಿಯ ಕಾರ್ಯಪ್ರವಾಹಕ್ಕಾಗಿ ಚಿತ್ರ ಅಪ್‌ಲೋಡ್ ಸೇರಿಸಲಾಗಿದೆ."},
    "Generate a crop recommendation to view market information.": {"Telugu": "మార్కెట్ సమాచారం చూడాలంటే పంట సిఫార్సు రూపొందించండి.", "Hindi": "बाज़ार जानकारी देखने के लिए फसल सिफारिश तैयार करें।", "Tamil": "சந்தை தகவலை பார்க்க பயிர் பரிந்துரையை உருவாக்கவும்.", "Kannada": "ಮಾರುಕಟ್ಟೆ ಮಾಹಿತಿಯನ್ನು ನೋಡಲು ಬೆಳೆ ಶಿಫಾರಸು ಪಡೆಯಿರಿ."},
    "Location:": {"Telugu": "ప్రదేశం:", "Hindi": "स्थान:", "Tamil": "இடம்:", "Kannada": "ಸ್ಥಳ:"},
    "Use this as an approximate demo value for presentation. Real mandi prices can change by district and date.": {"Telugu": "ప్రదర్శన కోసం దీనిని సుమారు డెమో విలువగా ఉపయోగించండి. నిజమైన మార్కెట్ ధరలు జిల్లా మరియు తేదీ ప్రకారం మారవచ్చు.", "Hindi": "इसे प्रस्तुति के लिए अनुमानित डेमो मान मानें। वास्तविक मंडी कीमतें जिला और तारीख के अनुसार बदल सकती हैं।", "Tamil": "வழங்கலுக்காக இதை அண்மையான மாதிரி மதிப்பாக கருதுங்கள். உண்மையான சந்தை விலைகள் மாவட்டம் மற்றும் தேதியின் அடிப்படையில் மாறலாம்.", "Kannada": "ಪ್ರದರ್ಶನಕ್ಕಾಗಿ ಇದನ್ನು ಅಂದಾಜು ಮಾದರಿ ಮೌಲ್ಯವಾಗಿ ಪರಿಗಣಿಸಿ. ನಿಜವಾದ ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು ಜಿಲ್ಲೆ ಮತ್ತು ದಿನಾಂಕದಂತೆ ಬದಲಾಗಬಹುದು."},
    "Compare market price with another crop": {"Telugu": "ఇంకో పంటతో మార్కెట్ ధరను పోల్చండి", "Hindi": "किसी अन्य फसल से बाज़ार मूल्य की तुलना करें", "Tamil": "மற்றொரு பயிருடன் சந்தை விலையை ஒப்பிடுங்கள்", "Kannada": "ಇನ್ನೊಂದು ಬೆಳೆಯೊಂದಿಗೆ ಮಾರುಕಟ್ಟೆ ಬೆಲೆಯನ್ನು ಹೋಲಿಸಿ"},
    "Higher market price:": {"Telugu": "ఎక్కువ మార్కెట్ ధర:", "Hindi": "अधिक बाज़ार मूल्य:", "Tamil": "அதிக சந்தை விலை:", "Kannada": "ಹೆಚ್ಚಿನ ಮಾರುಕಟ್ಟೆ ಬೆಲೆ:"},
    "Not available": {"Telugu": "అందుబాటులో లేదు", "Hindi": "उपलब्ध नहीं", "Tamil": "கிடைக்கவில்லை", "Kannada": "ಲಭ್ಯವಿಲ್ಲ"},
    "This recommendation is based on the trained Random Forest model and simple SIH rule-based advisory layers.": {"Telugu": "ఈ సిఫార్సు ట్రెయిన్ చేసిన రాండమ్ ఫారెస్ట్ మోడల్ మరియు సరళమైన SIH రూల్-బేస్డ్ లాజిక్ ఆధారంగా రూపొందించబడింది.", "Hindi": "यह सिफारिश प्रशिक्षित रैंडम फॉरेस्ट मॉडल और सरल SIH नियम-आधारित परतों पर आधारित है।", "Tamil": "இந்த பரிந்துரை பயிற்சி செய்யப்பட்ட ராண்டம் ஃபாரஸ்ட் மாடல் மற்றும் எளிய SIH விதி அடிப்படையிலான அடுக்குகள் மீது அமைந்தது.", "Kannada": "ಈ ಶಿಫಾರಸು ತರಬೇತಿ ನೀಡಿದ ರ್ಯಾಂಡಮ್ ಫಾರೆಸ್ಟ್ ಮಾದರಿ ಮತ್ತು ಸರಳ SIH ನಿಯಮ ಆಧಾರಿತ ಪದರಗಳನ್ನು ಆಧರಿಸಿದೆ."},
    "High temperature alert: Provide irrigation or mulching to reduce crop stress.": {"Telugu": "అధిక ఉష్ణోగ్రత హెచ్చరిక: పంట ఒత్తిడిని తగ్గించేందుకు నీరు లేదా మల్చింగ్ చేయండి.", "Hindi": "उच्च तापमान चेतावनी: फसल तनाव कम करने के लिए सिंचाई या मल्चिंग करें।", "Tamil": "அதிக வெப்பநிலை எச்சரிக்கை: பயிர் அழுத்தத்தை குறைக்க நீர்ப்பாய்ச்சி அல்லது மழைமூடி செய்யவும்.", "Kannada": "ಹೆಚ್ಚಿನ ತಾಪಮಾನ ಎಚ್ಚರಿಕೆ: ಬೆಳೆ ಒತ್ತಡವನ್ನು ಕಡಿಮೆ ಮಾಡಲು ನೀರಾವರಿ ಅಥವಾ ಮಲ್ಚಿಂಗ್ ಮಾಡಿ."},
    "High humidity alert: Watch for fungal disease and improve field ventilation.": {"Telugu": "అధిక తేమ హెచ్చరిక: ఫంగస్ వ్యాధులను గమనించి గాలి ప్రసరణ మెరుగుపరచండి.", "Hindi": "उच्च आर्द्रता चेतावनी: फफूंद रोगों पर ध्यान दें और खेत में वेंटिलेशन सुधारें।", "Tamil": "அதிக ஈரப்பதம் எச்சரிக்கை: பூஞ்சை நோய்களை கவனித்து காற்றோட்டத்தை மேம்படுத்தவும்.", "Kannada": "ಹೆಚ್ಚಿನ ಆದ್ರತೆ ಎಚ್ಚರಿಕೆ: ಶಿಲೀಂಧ್ರ ರೋಗಗಳನ್ನು ಗಮನಿಸಿ ಹೊಲದ ಗಾಳಿಚಲನವಲನವನ್ನು ಸುಧಾರಿಸಿ."},
    "Rain alert: Avoid spraying just before rainfall and check field drainage.": {"Telugu": "వర్ష హెచ్చరిక: వర్షం ముందు స్ప్రే చేయకుండా ఉండండి మరియు డ్రైనేజ్‌ను తనిఖీ చేయండి.", "Hindi": "बारिश चेतावनी: बारिश से पहले छिड़काव न करें और खेत की निकासी जांचें।", "Tamil": "மழை எச்சரிக்கை: மழைக்கு முன் தெளிப்பு செய்ய வேண்டாம் மற்றும் வடிகாலையை சரிபார்க்கவும்.", "Kannada": "ಮಳೆಯ ಎಚ್ಚರಿಕೆ: ಮಳೆಯ ಮೊದಲು ಸಿಂಪಡಿಸಬೇಡಿ ಮತ್ತು ಹೊಲದ ನೀರು ಹಾದಿಯನ್ನು ಪರಿಶೀಲಿಸಿ."},
    "Clear Sky": {"Telugu": "స్పష్టమైన ఆకాశం", "Hindi": "साफ़ आसमान", "Tamil": "தெளிந்த வானம்", "Kannada": "ಸ್ವಚ್ಛ ಆಕಾಶ"},
    "Quick Mode": {"Telugu": "త్వరిత విధానం", "Hindi": "क्विक मोड", "Tamil": "விரைவு முறை", "Kannada": "ಕ್ವಿಕ್ ಮೋಡ್"},
    "Advanced Mode": {"Telugu": "అడ్వాన్స్‌డ్ విధానం", "Hindi": "एडवांस मोड", "Tamil": "மேம்பட்ட முறை", "Kannada": "ಅಡ್ವಾನ್ಸ್ಡ್ ಮೋಡ್"},
    "Input Mode": {"Telugu": "ఇన్‌పుట్ విధానం", "Hindi": "इनपुट मोड", "Tamil": "உள்ளீட்டு முறை", "Kannada": "ಇನ್‌ಪುಟ್ ಮೋಡ್"},
    "Quick Mode uses suggested NPK values based on soil type.": {"Telugu": "త్వరిత విధానం నేల రకాన్ని ఆధారంగా సూచించిన NPK విలువలను వాడుతుంది.", "Hindi": "क्विक मोड मिट्टी के प्रकार के आधार पर सुझाए गए NPK मानों का उपयोग करता है।", "Tamil": "விரைவு முறை மண் வகையை அடிப்படையாகக் கொண்டு பரிந்துரைக்கப்பட்ட NPK மதிப்புகளை பயன்படுத்துகிறது.", "Kannada": "ಕ್ವಿಕ್ ಮೋಡ್ ಮಣ್ಣಿನ ಪ್ರಕಾರದ ಆಧಾರದ ಮೇಲೆ ಸೂಚಿಸಿದ NPK ಮೌಲ್ಯಗಳನ್ನು ಬಳಸುತ್ತದೆ."},
    "Tip: If unsure, follow the first recommendation.": {"Telugu": "సూచన: సందేహం ఉంటే మొదటి సిఫార్సును అనుసరించండి.", "Hindi": "सुझाव: यदि संदेह हो तो पहली सिफारिश अपनाएँ।", "Tamil": "குறிப்பு: உறுதி இல்லையெனில் முதல் பரிந்துரையைப் பின்பற்றுங்கள்.", "Kannada": "ಸೂಚನೆ: ಅನುಮಾನ ಇದ್ದರೆ ಮೊದಲ ಶಿಫಾರಸನ್ನು ಅನುಸರಿಸಿ."},
    "Summary": {"Telugu": "సారాంశం", "Hindi": "सारांश", "Tamil": "சுருக்கம்", "Kannada": "ಸಾರಾಂಶ"},
    "Panchagavya": {"Telugu": "పంచగవ్య", "Hindi": "पंचगव्य", "Tamil": "பஞ்சகவ்யம்", "Kannada": "ಪಂಚಗವ್ಯ"},
    "Vermicompost": {"Telugu": "వెర్మీకంపోస్ట్", "Hindi": "वर्मी कम्पोस्ट", "Tamil": "வெர்மிகம்போஸ்ட்", "Kannada": "ವರ್ಮಿಕಂಪೋಸ್ಟ್"},
    "litres": {"Telugu": "లీటర్లు", "Hindi": "लीटर", "Tamil": "லிட்டர்", "Kannada": "ಲೀಟರ್"},
    "kg": {"Telugu": "కిలో", "Hindi": "किलो", "Tamil": "கிலோ", "Kannada": "ಕಿಲೋ"},
    "Kharif": {"Telugu": "ఖరీఫ్", "Hindi": "खरीफ", "Tamil": "கரீஃப்", "Kannada": "ಖರೀಫ್"},
    "Rabi": {"Telugu": "రబీ", "Hindi": "रबी", "Tamil": "ரபி", "Kannada": "ರಬಿ"},
    "Summer": {"Telugu": "వేసవి", "Hindi": "गर्मी", "Tamil": "கோடை", "Kannada": "ಬೇಸಿಗೆ"},
    "Black": {"Telugu": "నల్ల నేల", "Hindi": "काली मिट्टी", "Tamil": "கருப்பு மண்", "Kannada": "ಕರಿ ಮಣ್ಣು"},
    "Red": {"Telugu": "ఎర్ర నేల", "Hindi": "लाल मिट्टी", "Tamil": "சிவப்பு மண்", "Kannada": "ಕೆಂಪು ಮಣ್ಣು"},
    "Alluvial": {"Telugu": "అల్లువియల్ నేల", "Hindi": "जलोढ़ मिट्टी", "Tamil": "அல்லுவியல் மண்", "Kannada": "ಅಲ್ಲುವಿಯಲ್ ಮಣ್ಣು"},
}

TRANSLATIONS = {lang: {} for lang in ["Telugu", "Hindi", "Tamil", "Kannada"]}
for english_text, language_values in BASE_UI_TRANSLATIONS.items():
    for language_name, translated_text in language_values.items():
        TRANSLATIONS[language_name][english_text] = translated_text

CROP_TRANSLATIONS = {
    "Telugu": {"Rice": "వరి", "Maize": "మొక్కజొన్న", "Chickpea": "సెనగ", "Kidneybeans": "రాజ్మా", "Pigeonpeas": "కందులు", "Mothbeans": "మోత్ బీన్స్", "Mungbean": "పెసర", "Blackgram": "మినుములు", "Lentil": "మసూర్", "Pomegranate": "దానిమ్మ", "Banana": "అరటి", "Mango": "మామిడి", "Grapes": "ద్రాక్ష", "Watermelon": "పుచ్చకాయ", "Muskmelon": "ఖర్బూజా", "Apple": "సేపు", "Orange": "నారింజ", "Papaya": "బొప్పాయి", "Coconut": "కొబ్బరి", "Cotton": "పత్తి", "Jute": "జూట్", "Coffee": "కాఫీ", "Urea (High Nitrogen)": "యూరియా (అధిక నత్రజని)", "DAP (Diammonium Phosphate - High Phosphorus)": "డిఏపీ (అధిక ఫాస్ఫరస్)", "MOP (Muriate of Potash - High Potassium)": "ఎంఓపీ (అధిక పొటాషియం)", "NPK 19:19:19 (Balanced)": "ఎన్‌పికే 19:19:19 (సమతుల్యం)", "Soil fertility is good. Use organic compost.": "నేల సారవంతంగా ఉంది. సేంద్రియ కంపోస్ట్ వాడండి."},
    "Hindi": {"Rice": "धान", "Maize": "मक्का", "Chickpea": "चना", "Kidneybeans": "राजमा", "Pigeonpeas": "अरहर", "Mothbeans": "मौठ", "Mungbean": "मूंग", "Blackgram": "उड़द", "Lentil": "मसूर", "Pomegranate": "अनार", "Banana": "केला", "Mango": "आम", "Grapes": "अंगूर", "Watermelon": "तरबूज", "Muskmelon": "खरबूजा", "Apple": "सेब", "Orange": "संतरा", "Papaya": "पपीता", "Coconut": "नारियल", "Cotton": "कपास", "Jute": "जूट", "Coffee": "कॉफी"},
    "Tamil": {"Rice": "நெல்", "Maize": "மக்காச்சோளம்", "Chickpea": "கொண்டைக்கடலை", "Kidneybeans": "ராஜ்மா", "Pigeonpeas": "துவரம்", "Mothbeans": "மொத் பீன்", "Mungbean": "பாசிப்பயறு", "Blackgram": "உளுந்து", "Lentil": "மசூர் பருப்பு", "Pomegranate": "மாதுளை", "Banana": "வாழை", "Mango": "மாம்பழம்", "Grapes": "திராட்சை", "Watermelon": "தர்பூசணி", "Muskmelon": "முலாம்பழம்", "Apple": "ஆப்பிள்", "Orange": "ஆரஞ்சு", "Papaya": "பப்பாளி", "Coconut": "தேங்காய்", "Cotton": "பருத்தி", "Jute": "ஜூட்", "Coffee": "காப்பி"},
    "Kannada": {"Rice": "ಅಕ್ಕಿ", "Maize": "ಮೆಕ್ಕೆಜೋಳ", "Chickpea": "ಕಡಲೆ", "Kidneybeans": "ರಾಜ್ಮಾ", "Pigeonpeas": "ತೊಗರಿ", "Mothbeans": "ಮೋತ್ ಬೀನ್", "Mungbean": "ಹೆಸರು", "Blackgram": "ಉದ್ದು", "Lentil": "ಮಸೂರು", "Pomegranate": "ದಾಳಿಂಬೆ", "Banana": "ಬಾಳೆ", "Mango": "ಮಾವು", "Grapes": "ದ್ರಾಕ್ಷಿ", "Watermelon": "ಕಲ್ಲಂಗಡಿ", "Muskmelon": "ಖರ್ಬೂಜಾ", "Apple": "ಸೇಬು", "Orange": "ಕಿತ್ತಳೆ", "Papaya": "ಪಪ್ಪಾಯಿ", "Coconut": "ತೆಂಗು", "Cotton": "ಹತ್ತಿ", "Jute": "ಜ್ಯೂಟ್", "Coffee": "ಕಾಫಿ"},
}


def translate_text(text, language):
    if language == "English":
        return text
    return TRANSLATIONS.get(language, {}).get(text, CROP_TRANSLATIONS.get(language, {}).get(text, text))


def get_crop_display_name(crop_name, language):
    if language == "English":
        return crop_name
    return CROP_TRANSLATIONS.get(language, {}).get(crop_name, crop_name)


def get_fertilizer_recommendation(n, p, k):
    if n < 50:
        return "Urea (High Nitrogen)"
    if p < 50:
        return "DAP (Diammonium Phosphate - High Phosphorus)"
    if k < 50:
        return "MOP (Muriate of Potash - High Potassium)"
    if n < 80 and p < 80 and k < 80:
        return "NPK 19:19:19 (Balanced)"
    return "Soil fertility is good. Use organic compost."


def fetch_weather_data(city_name, api_key):
    if not api_key:
        return {
            "temperature": 28.5,
            "humidity": 65.0,
            "weather": "Clear Sky",
            "rain_expected": False,
            "mocked": True,
        }

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_name, "appid": api_key, "units": "metric"}

    try:
        response = requests.get(base_url, params=params, timeout=10)
        data = response.json()

        if response.status_code == 200:
            weather_text = data["weather"][0]["description"].title()
            return {
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "weather": weather_text,
                "rain_expected": "rain" in weather_text.lower() or "drizzle" in weather_text.lower(),
                "mocked": False,
            }
        return {"error": data.get("message", "Could not fetch weather.")}
    except Exception as exc:
        return {"error": str(exc)}


def get_weather_alerts(weather_data):
    if not weather_data or "error" in weather_data:
        return []

    alerts = []
    if weather_data.get("temperature", 0) > 35:
        alerts.append("High temperature alert: Provide irrigation or mulching to reduce crop stress.")
    if weather_data.get("humidity", 0) > 85:
        alerts.append("High humidity alert: Watch for fungal disease and improve field ventilation.")
    if weather_data.get("rain_expected"):
        alerts.append("Rain alert: Avoid spraying just before rainfall and check field drainage.")
    return alerts


def mock_disease_detection(image):
    return "No disease detected. Plant looks healthy! (Placeholder Feature)"


def get_crop_specific_advice(crop_name):
    return CROP_GUIDE.get(crop_name, DEFAULT_CROP_GUIDE)


def get_organic_farming_plan(crop_name, land_acres):
    crop_guide = get_crop_specific_advice(crop_name)
    land_acres = max(land_acres, 0)

    return {
        "watering": crop_guide["watering"],
        "crop_advice": crop_guide["crop_advice"],
        "panchagavya_total_litres": round(crop_guide["panchagavya_litre_per_acre"] * land_acres, 2),
        "vermicompost_total_kg": round(crop_guide["vermicompost_kg_per_acre"] * land_acres, 2),
        "booster_components": crop_guide["booster_components"],
        "application_schedule": {
            "panchagavya": "Spray once every 12-15 days during active growth.",
            "vermicompost": "Apply once as basal dose and again after 30-35 days for long-duration crops.",
        },
    }


def get_state_specific_advice(state):
    return REGION_SPECIFIC_TIPS.get(state, "Follow local agricultural department guidance for irrigation timing and input planning.")


def get_suitability_feedback(crop_name, season, soil_type):
    rules = SOIL_SEASON_RULES.get(crop_name)
    if not rules:
        return {
            "season_fit": "Moderate fit",
            "soil_fit": "Moderate fit",
            "summary": "No detailed rule is stored for this crop, so general agronomy guidance is used.",
        }

    season_fit = "Good fit" if season in rules["seasons"] else "Check suitability"
    soil_fit = "Good fit" if soil_type in rules["soils"] else "Check suitability"

    if season_fit == "Good fit" and soil_fit == "Good fit":
        summary = f"{crop_name} matches the selected season and soil type reasonably well."
    else:
        summary = f"{crop_name} is predicted by the model, but your selected season or soil may need extra field management."

    return {"season_fit": season_fit, "soil_fit": soil_fit, "summary": summary}


def get_crop_market_price(crop_name):
    return CROP_PRICES.get(crop_name)


def get_disease_advisory(crop_name):
    return DISEASE_LIBRARY.get(crop_name, DEFAULT_DISEASES)


def explain_crop_choice(crop_name, n, p, k, temp, humidity, ph, season, soil_type, state):
    reasons = []

    if n >= 80:
        reasons.append("Nitrogen is strong, which supports leafy and vigorous crop growth.")
    elif n < 40:
        reasons.append("Nitrogen is relatively low, so crops that manage with moderate nitrogen are safer.")

    if p >= 60:
        reasons.append("Phosphorus is adequate for root development and early plant establishment.")
    else:
        reasons.append("Phosphorus is on the lower side, so fertilizer support may be useful.")

    if k >= 60:
        reasons.append("Potassium level can help plant strength and stress tolerance.")
    else:
        reasons.append("Potassium is limited, so fruiting and stress management need attention.")

    if 20 <= temp <= 32:
        reasons.append("Temperature is in a generally favorable range for many field crops.")
    elif temp > 35:
        reasons.append("Temperature is high, so heat tolerance and irrigation become important.")
    else:
        reasons.append("Cooler temperature may favor rabi-style crop conditions.")

    if 5.5 <= ph <= 7.5:
        reasons.append("Soil pH is near the productive range for most crops.")
    else:
        reasons.append("Soil pH is outside the common optimum range, so nutrient uptake may reduce.")

    reasons.append(f"The model predicted {crop_name} from your NPK, temperature, humidity, and pH values.")
    reasons.append(f"Selected context: {season} season, {soil_type} soil, and {state} conditions.")
    return reasons
