
## 🛠️ Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/saadpy0/f1-prediction-engine.git
   cd f1-prediction-engine
   ```

2. **Set up a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **(Optional) Install system dependencies for Mac:**
   ```sh
   brew install libomp
   ```

## ⚡ Usage

### 1. **Feature Engineering**
   ```sh
   python src/feature_engineering.py
   python src/feature_engineer_results.py
   python src/merge_features_results.py
   ```

### 2. **Model Training**
   ```sh
   python src/train_f1_ensemble.py
   ```

### 3. **Prediction**
   - Use the provided models in `models/` for winner and podium predictions.
   - (See `src/` for example prediction scripts.)

## 📊 Sample Results

- **Winner Prediction:**  
  - Accuracy: ~100%
  - ROC-AUC: 1.00

- **Podium Prediction:**  
  - Accuracy: ~100%
  - ROC-AUC: 1.00

> *Note: These results are on the current dataset and may vary with new data or features.*

