=======================================================
Pneumonia Detection from Chest X-rays
Master's Final Project — DATA 6250 Machine Learning
Wentworth Institute of Technology
Student: Pavan Kalyan
=======================================================

OVERVIEW
--------
This project builds a medical image classification system
that detects pneumonia from chest X-ray images using both
classical machine learning and deep learning approaches.

RESULTS SUMMARY
---------------
Model               Accuracy    AUC-ROC
-----------         --------    -------
Decision Tree       82.37%      N/A
Random Forest       82.05%      0.9499
ResNet50 CNN        91.67%      0.9627

Best model: ResNet50 fine-tuned with transfer learning
Pneumonia recall: 97% (catches 97% of all pneumonia cases)

DATASET
-------
Name    : Chest X-Ray Images (Pneumonia)
Source  : https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia
License : CC BY 4.0
Size    : 5,216 training images, 624 test images
Classes : NORMAL (1,342) vs PNEUMONIA (3,876)

NOTE: Dataset is not included due to size (2.3GB).
Download from Kaggle link above and place in:
data/raw/chest_xray/chest_xray/

PROJECT STRUCTURE
-----------------
ML Project/
├── app/
│   └── app.py              (Streamlit web app)
├── data/
│   ├── raw/                (downloaded dataset goes here)
│   └── processed/
├── models/
│   ├── config.json         (dataset + training config)
│   ├── best_resnet50.pth   (best CNN model weights)
│   ├── baseline_cnn.pth    (scratch CNN weights)
│   ├── random_forest.pkl   (tuned Random Forest)
│   └── results.json        (all model results)
├── notebooks/
│   ├── eda.ipynb              (Exploratory Analysis)
│   ├── preprocessing.ipynb    (Data Pipeline)
│   ├── baseline_cnn.ipynb     (Scratch CNN)
│   ├── transfer_learning.ipynb(ResNet50)
│   ├── evaluation.ipynb       (Metrics + Grad-CAM)
│   └── classical_ml.ipynb     (RF + GridSearchCV)
├── src/
│   └── __init__.py
└── README.txt

HOW TO RUN
----------
1. Clone or download this project

2. Create and activate virtual environment:
   python3 -m venv venv
   source venv/bin/activate        (Mac/Linux)
   venv\Scripts\activate           (Windows)

3. Install dependencies:
   pip install torch torchvision numpy pandas matplotlib
   pip install seaborn opencv-python Pillow scikit-learn
   pip install streamlit kaggle grad-cam tqdm jupyter joblib

4. Download dataset:
   kaggle datasets download -d paultimothymooney/chest-xray-pneumonia
   unzip chest-xray-pneumonia.zip -d data/raw/

5. Run notebooks in order:
   jupyter notebook
   Then open notebooks/ and run 1 through 6 in order

6. Run Streamlit app:
   cd app
   ../venv/bin/streamlit run app.py

METHODS USED
------------
- Exploratory Data Analysis (EDA)
- Data augmentation (flip, rotate, color jitter)
- PyTorch DataLoaders with class weighting
- Simple CNN from scratch (baseline)
- Transfer learning with ResNet50 (ImageNet pretrained)
- Fine-tuning (unfreezing layer4)
- Decision Tree classifier
- Random Forest with GridSearchCV tuning (36 fits, 3-fold CV)
- Grad-CAM explainability heatmaps
- Streamlit deployment

METRICS REPORTED
----------------
- Accuracy, Precision, Recall, F1-score
- AUC-ROC curve
- Confusion matrix
- Grad-CAM visual explanations

AI TOOL DISCLOSURE
------------------
This project was developed with assistance from Claude (Anthropic)
for code guidance, debugging, and structure suggestions.
All code has been reviewed, understood, and validated by the student.
Final implementation, analysis, and conclusions are the student's own work.

RANDOM SEEDS
------------
All classical ML models use random_state=42 for reproducibility.
PyTorch training uses deterministic MPS backend on Apple Silicon.

REFERENCES
----------
- Dataset: Kermany et al. (2018), Cell journal
- ResNet50: He et al. (2016), Deep Residual Learning
- Grad-CAM: Selvaraju et al. (2017)
- PyTorch: https://pytorch.org
- Streamlit: https://streamlit.io