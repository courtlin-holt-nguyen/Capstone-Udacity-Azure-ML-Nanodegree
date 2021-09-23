from sklearn.linear_model import LogisticRegression
import argparse
import os
import numpy as np
from sklearn.metrics import mean_squared_error
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from azureml.core.run import Run
from azureml.data.dataset_factory import TabularDatasetFactory

# TODO: Create TabularDataset using TabularDatasetFactory
# Data is located at:
# "https://automlsamplenotebookdata.blob.core.windows.net/automl-sample-notebook-data/bankmarketing_train.csv"

from azureml.core.dataset import Dataset
from azureml.core import Workspace, Experiment


run = Run.get_context(allow_offline=True)
ws = run.experiment.workspace #req'd for authentication for accessing local storage ie. blobstore

# ws = Workspace.get(name="udacity-courtlin",subscription_id="bd6c48f0-b2f5-4fd8-b4de-3351b13cbee8", resource_group="udacity-nano-degree")


ds = Dataset.get_by_name(ws, name='healthcare-dataset-stroke-data')

# url_paths = [
#     "https://automlsamplenotebookdata.blob.core.windows.net/automl-sample-notebook-data/bankmarketing_train.csv"
#             ]

# ds = TabularDatasetFactory.from_delimited_files(path=url_paths)


def clean_data(data):
    # Dict for cleaning data
    # months = {"jan":1, "feb":2, "mar":3, "apr":4, "may":5, "jun":6, "jul":7, "aug":8, "sep":9, "oct":10, "nov":11, "dec":12}
    # weekdays = {"mon":1, "tue":2, "wed":3, "thu":4, "fri":5, "sat":6, "sun":7}

    # Clean and one hot encode data
    x_df = data.to_pandas_dataframe().dropna()
    
    gender = pd.get_dummies(x_df.gender, prefix="gender")
    x_df.drop("gender", inplace=True, axis=1)
    x_df = x_df.join(gender)
    
    work_type = pd.get_dummies(x_df.work_type, prefix="work_type")
    x_df.drop("work_type", inplace=True, axis=1)
    x_df = x_df.join(work_type)
    # x_df["marital"] = x_df.marital.apply(lambda s: 1 if s == "married" else 0)
    # x_df["default"] = x_df.default.apply(lambda s: 1 if s == "yes" else 0)
    # x_df["housing"] = x_df.housing.apply(lambda s: 1 if s == "yes" else 0)
    # x_df["loan"] = x_df.loan.apply(lambda s: 1 if s == "yes" else 0)
    
    Residence_type = pd.get_dummies(x_df.Residence_type, prefix="Residence_type")
    x_df.drop("Residence_type", inplace=True, axis=1)
    x_df = x_df.join(Residence_type)

    smoking_status = pd.get_dummies(x_df.smoking_status, prefix="smoking_status")
    x_df.drop("smoking_status", inplace=True, axis=1)
    x_df = x_df.join(smoking_status)
    # x_df["month"] = x_df.month.map(months)
    # x_df["day_of_week"] = x_df.day_of_week.map(weekdays)
    # x_df["poutcome"] = x_df.poutcome.apply(lambda s: 1 if s == "success" else 0)

    # y_df = x_df.pop("stroke").apply(lambda s: 1 if s == "yes" else 0)
    y_df = x_df.pop("stroke")

    return x_df, y_df

x, y = clean_data(ds)

# TODO: Split data into train and test sets.
# cleaned_data = x
# cleaned_data['y'] = y 
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=123)

# ds = x.join(y)


def main():
    # Add arguments to script
    parser = argparse.ArgumentParser()

    parser.add_argument('--C', type=float, default=1.0, help="Inverse of regularization strength. Smaller values cause stronger regularization")
    parser.add_argument('--max_iter', type=int, default=100, help="Maximum number of iterations to converge")

    args = parser.parse_args()

    run.log("Regularization Strength:", np.float(args.C))
    run.log("Max iterations:", np.int(args.max_iter))

    model = LogisticRegression(C=args.C, max_iter=args.max_iter).fit(x_train, y_train)

    accuracy = model.score(x_test, y_test)
    run.log("Accuracy", np.float(accuracy))
    
    os.makedirs('outputs', exist_ok=True)
    joblib.dump(value=model, filename='outputs/model.pkl')

if __name__ == '__main__':
    main()



