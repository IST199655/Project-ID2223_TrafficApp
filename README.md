# Serverless Traffic Prediction Machine Learning System

<iframe
  src="https://huggingface.co/spaces/Heit39/Stockholm_Traffic"
  width="100%"
  height="500"
  frameborder="0"
></iframe>

## Overview  
This project leverages **Hopsworks** as the data management platform and **XGBoost** as the machine learning model to predict traffic conditions. The target variable for prediction is the **relative speed**, defined as:  

The system is designed for a location in **Stockholm**, near Odenplan, with the following coordinates:  **59.34318, 18.05141**.  

The hugging face space with the UI is available [here](https://huggingface.co/spaces/Heit39/Stockholm_Traffic)

## Key Features  
- **Data Preprocessing**: Includes cleaning and preparing traffic data for efficient analysis.  
- **Serverless Machine Learning**: Implements serverless architecture to streamline deployment and scalability of ML workflows.  
- **Model Training**: Uses the XGBoost algorithm for robust and accurate predictions.  
- **Performance Optimization**: Fine-tuning the model with grid search to improve accuracy and reduce overfitting.  
- **Real-world Application**: Designed to provide actionable insights for traffic management and optimization with an UI

  

## File Organization  
The repository is structured as follows:  

```plaintext
Project-ID2223_TrafficApp/  
├── notebooks/  
│   ├── Startup.ipynb  # Jupyter notebook to 
│   ├── Update_hourly.ipynb     # Jupyter notebook to update features stores (called by a github action every hour)  
│   ├── Training.ipynb     # Jupyter notebook for model training to update model registry(called by a github action every week)
│   ├── Inference.ipynb     # Jupyter notebook for model inference (called by a github action every hour)