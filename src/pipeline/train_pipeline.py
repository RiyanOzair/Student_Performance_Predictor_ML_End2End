import sys 
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, model_evaluation
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

class TrainPipeline:
    def __init__(self):
        pass

    def initiate_training_pipeline(self):
        try:
            # Load the training data
            train_data_path = os.path.join('artifacts', 'train.csv')
            train_df = pd.read_csv(train_data_path)

            # Split the data into features and target variable
            X = train_df.drop(columns=['target'], axis=1)
            y = train_df['target']

            # Split the data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Define the models to be evaluated
            models = {
                'RandomForest': RandomForestClassifier(),
                'LogisticRegression': LogisticRegression(),
                'SVC': SVC()
            }

            # Evaluate the models and get the best model
            best_model_name, best_model = model_evaluation(X_train, y_train, X_test, y_test, models, params={
                'RandomForest': {},
                'LogisticRegression': {},
                'SVC': {}
            })

            # Save the best model to disk
            save_object(file_path=os.path.join('artifacts', 'model.pkl'), obj=best_model)

        except Exception as e:
            logging.error(f"Error occurred during training pipeline: {e}")
            raise CustomException(e, sys)
        