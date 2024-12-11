# -*- coding: utf-8 -*-
"""model2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GpvAVK5OqrokBXDoNkYoiVM0LiMnTWUj
"""



from google.colab import drive
drive.mount('/content/drive')

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

class MyLogisticRegression:
    def __init__(self, dataset_path, perform_test=True):
        self.training_set = None
        self.test_set = None
        self.model_logistic = None
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.label_encoder = None  # Declare label_encoder as an instance attribute
        self.perform_test = perform_test
        self.dataset_path = dataset_path
        self.read_csv()

    def read_csv(self):
        """
        Reads the dataset and preprocesses it.
        """
        data = pd.read_csv(self.dataset_path)
        X = data.drop('Weather Type', axis=1)
        y = data['Weather Type']

        # Preprocess data
        X = pd.get_dummies(X, columns=['Cloud Cover', 'Season', 'Location'], drop_first=True)
        self.label_encoder = LabelEncoder()  # Assign the label encoder instance to the class attribute
        y_encoded = self.label_encoder.fit_transform(y)
        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(X)

        # Split into training and test sets
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X_scaled, y_encoded, test_size=0.5, random_state=42)

    def model_fit_logistic(self):
        """
        Initialize self.model_logistic and call the fit function.
        """
        self.model_logistic = LogisticRegression()
        self.model_logistic.fit(self.X_train, self.y_train)

    def model_predict_logistic(self):
        """
        Calculate and return the accuracy, precision, recall, f1, support of the model.
        """
        self.model_fit_logistic()
        predictions = self.model_logistic.predict(self.X_test)

        # Calculate metrics
        accuracy = accuracy_score(self.y_test, predictions)
        precision, recall, f1, support = precision_recall_fscore_support(self.y_test, predictions, average=None)

        # Get label mappings
        label_mapping = {i: label for i, label in enumerate(self.label_encoder.classes_)}

        # Attach class labels to precision, recall, etc.
        metrics = {
            "Accuracy": accuracy,
            "Metrics": []
        }
        for i, class_label in label_mapping.items():
            metrics["Metrics"].append({
                "Class": class_label,
                "Precision": precision[i],
                "Recall": recall[i],
                "F1 Score": f1[i],
                "Support": support[i]
            })
        return metrics

if __name__ == '__main__':
    # Define the dataset path
    dataset_path = "/content/drive/My Drive/Cs482/Assignments/Final/weather_classification_data.csv"

    # Instantiate the MyLogisticRegression class
    logistic_model = MyLogisticRegression(dataset_path)

    # Predict and evaluate
    metrics = logistic_model.model_predict_logistic()
    precision_avg=0
    recall_avg=0
    f1_avg=0
    # Output results and calculate averages
    print(f"Accuracy: {metrics['Accuracy']}")
    for metric in metrics["Metrics"]:
        print(f"Class: {metric['Class']}")
        print(f"  Precision: {metric['Precision']}")
        print(f"  Recall: {metric['Recall']}")
        print(f"  F1 Score: {metric['F1 Score']}")
        print(f"  Support: {metric['Support']}")

        # Sum precision, recall, and F1 scores for averaging
        precision_avg += metric['Precision']
        recall_avg += metric['Recall']
        f1_avg += metric['F1 Score']

    # Calculate macro averages
    num_classes = len(metrics["Metrics"])
    precision_avg = precision_avg / num_classes
    recall_avg = recall_avg / num_classes
    f1_avg = f1_avg / num_classes

    # Print averages
    print("\nAverages:")
    print(f"  Average Precision: {precision_avg}")
    print(f"  Average Recall: {recall_avg}")
    print(f"  Average F1 Score: {f1_avg}")