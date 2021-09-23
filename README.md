# Capstone Azure ML Engineer Udacity Nanodegree

In this project, I created two classification models to predict the whether a patient is likely to have a stroke or not. 

The first classification model uses Azure AutoML to test various classifications models and selects the best one based on overall Accuracy. The second classification model uses logistic regression via sklearn and Hyperdrive to test various combinations of hyperparameters, - `C` (Inverse of regularization strength) and `max_iter` (Maximum number of iterations taken to converge), in an attempt to find the optimal model. Once the best AutoML model was found, it was deployed as a webservice and test patient data was sent to the deployed model to generate a response prediction, i.e. True or False.  

## Project Set Up and Installation
The following steps were used to create the project in AzureML.

1. Load the external dataset into AzureML
2. Use the Python SDK to create a compute instance.
3. Configure and submit an AutoML run using the SDK.
4. Once the Azure AutoML run is finished, find, save and register the best model with the Azure ML service.
5. Using the SDK, configure the deployment settings and the inference entry script (scoring.py) that is used to pass input to the deployed web endpoint.
6. Test the deployed model endpoint using a python file (endpoint.py) as well as a JSON request sent to the endpoint through the SDK.
7. Delete the compute cluster and the deployed endpoint service

## Dataset

### Overview
The dataset contains characteristics of 5,110 patients who ultimately did, or did not, suffer a stroke. The patient data points include the following attributes:

1) id: unique identifier
2) gender: "Male", "Female" or "Other"

3) age: age of the patient
4) hypertension: 0 if the patient doesn't have hypertension, 1 if the patient has hypertension

5) heart_disease: 0 if the patient doesn't have any heart diseases, 1 if the patient has a heart disease

6) ever_married: "No" or "Yes"

7) work_type: "children", "Govt_jov", "Never_worked", "Private" or "Self-employed"

8) Residence_type: "Rural" or "Urban"

9) avg_glucose_level: average glucose level in blood

10) bmi: body mass index
11) smoking_status: "formerly smoked", "never smoked", "smokes" or "Unknown"*

12) stroke: 1 if the patient had a stroke or 0 if not

The dataset can be downloaded from this [link](https://www.kaggle.com/fedesoriano/stroke-prediction-dataset?select=healthcare-dataset-stroke-data.csv) on Kaggle.

The author of the dataset is [fedesoriano](https://www.kaggle.com/fedesoriano)



### Task

The model will give a binary prediction whether a patient is likely to have a stroke or not, based on various demographic (gender, age, BMI) and behavioral attributes (type of employment, smoking status) of the patient.

### Access
The dataset was downloaded from Kaggle.com and uploaded to my AzureML workspace as a registered dataset.

![Dataset registered with Azure ML](https://github.com/icenine81/Capstone_udacity_ml_nanodegree/blob/513f7d051e5cf2ca0839f6d8a4f60891ddde3818/Screenshots/Dataset%20Registered.jpg)



## Automated ML
*TODO*: Give an overview of the `automl` settings and configuration you used for this experiment

These settings were used to configure the automl experiment.

![AutoML configuration settings](https://github.com/icenine81/Capstone_udacity_ml_nanodegree/blob/71feef72f0e2391c31bc260ac64775751696fd25/Screenshots/Automl%20Settings.jpg)

The primary metric used to evaluate the various automl models used was Accuracy.

The experiment was configured to run for a maximum of 30 minutes, with 4 models tested concurrently at any given time. 

The experiment was a classification task with the goal of predicting the value in column "stroke". Azure AutoML was used to automatically generate the various features as well as testing the dataset for imbalance, missing values, etc.

### Results
*TODO*: What are the results you got with your automated ML model? What were the parameters of the model? How could you have improved it?

*TODO* Remeber to provide screenshots of the `RunDetails` widget as well as a screenshot of the best model trained with it's parameters.

The best automl model was a Voting Ensemble with an accuracy score of 95.245% that consisted of 10 different models of varying weights with different parameters. The primary models used within the ensemble were XGBoostClassifiers, LightGBM and RandomForest models with various scaler wrappers. 

![AutoML Best Model Voting Ensemble](https://github.com/icenine81/Capstone_udacity_ml_nanodegree/blob/e66411afc5764c64b996ec07b85885f310873d29/Screenshots/AutoML%20Best%20Model%20VotingEnsemble.jpg)

![25 different models were attempted](https://github.com/icenine81/Capstone_udacity_ml_nanodegree/blob/35bb390d93579baf6bb72392e13ed9a9df27bb19/Screenshots/AutoML%20Best%20Model%20VotingEnsemble%20attemps.jpg)

![AutoML Best Model Voting Ensemble detailed submodels](https://github.com/icenine81/Capstone_udacity_ml_nanodegree/blob/35bb390d93579baf6bb72392e13ed9a9df27bb19/Screenshots/AutoML%20Best%20Model%20Voting%20Ensemble%20detailed%20submodels.jpg)

![Extensive list of parameters used within the various models that comprise the VotingEnsemble](https://github.com/icenine81/Capstone_udacity_ml_nanodegree/blob/3d7e49619e4754e4403e64f8abd81cb9490f053d/Screenshots/AutoML%20Best%20Model%20Voting%20Ensemble%20detailed%20submodels%202.jpg)

![AutoML RunDetails widget](https://github.com/icenine81/Capstone_udacity_ml_nanodegree/blob/35bb390d93579baf6bb72392e13ed9a9df27bb19/Screenshots/AutoML%20RunDetails%20Widget%20GUI.jpg)

The final model's accuracy could have been improved by allowing more training time to search for optimal weighted models. Additionally, the class imbalance issue could be addressed to improve the real-world accuracy of the model. 

![Azure data guardrails warning - class imbalance](https://github.com/icenine81/Capstone_udacity_ml_nanodegree/blob/35bb390d93579baf6bb72392e13ed9a9df27bb19/Screenshots/AutoML%20Best%20Model%20Data%20Guardrails.jpg)

In terms of the most important factors that predict whether or not a person will have a stroke, Age was found to be the most important factor, followed by Average Glucose Levels.

![Voting Ensemble feature importance explanation](https://github.com/icenine81/Capstone_udacity_ml_nanodegree/blob/35bb390d93579baf6bb72392e13ed9a9df27bb19/Screenshots/AutoML%20Best%20Model%20VotingEnsemble%20Explained.jpg)

This VotingEnsemble model was registered as a Model in Azure ML and eventually deployed. 

![VotingEnsemble model registered in Azure via SDK](https://github.com/icenine81/Capstone_udacity_ml_nanodegree/blob/149bc9c4bc7d5e3d935317bb5aef680a5fd8e6af/Screenshots/Best%20AutoML%20model%20registered%20and%20deployed.jpg)

![VotingEnsemble model appears as a registered model in Azure ML](https://github.com/icenine81/Capstone_udacity_ml_nanodegree/blob/149bc9c4bc7d5e3d935317bb5aef680a5fd8e6af/Screenshots/AutoML%20Model%20Deployed.jpg)

## Hyperparameter Tuning
Since this task involved binary classification, a Logistic Regression model from the sklearn library was chosen. This model is quick to train and tune and easy to explain while still providing a high level of prediction accuracy. 

Two hyperparameters were selected for tuning with Azure HyperDrive:

- C (inverse of regularization strength): This parameters determines the degree of regularization and helps to prevent the model from overfitting. Smaller values lead to stronger regularization. The values tried were 0.001,0.01,0.1,1.0,10.0 and 50.0. 
- Maximum iterations: It was set to choose from 10 and 25. This parameter defines the maximum number of iterations allowed for the algorithm's solver to converge on a solution.

The RandomParameterSampling method was used to search the hyperparameter grid space. A Bandit early stopping policy was also used to prevent compute resources from being wasted on unnecessary optimization attempts.  

![Hyperdrive parameters](https://github.com/icenine81/Capstone_udacity_ml_nanodegree/blob/569d71fa1ecbe9850c73a53984aad42584c9a342/Screenshots/Hyperdrive%20parameters.jpg)


### Results
The best hyperdrive model had an accuracy of 95.82% and used a C value of 50 (indicating little regularization) and a Max Iterations value of 25. The accuracy of the model could possibly have been improved by increasing the number of Max Iterations and allowing Hyperdrive to test more than 24 models. 

![Best hyperdrive model parameters](https://github.com/icenine81/Capstone_udacity_ml_nanodegree/blob/9201991d24a83a2102fc9ce2d3b3554349592f0a/Screenshots/Hyperdrive%20best%20model%20parameters.jpg)

![Hyperdrive RunDetails widget output 1](https://github.com/icenine81/Capstone_udacity_ml_nanodegree/blob/569d71fa1ecbe9850c73a53984aad42584c9a342/Screenshots/RunDetails%20Hyperdrive%201.jpg)

![Hyperdrive RunDetails widget output 2](https://github.com/icenine81/Capstone_udacity_ml_nanodegree/blob/569d71fa1ecbe9850c73a53984aad42584c9a342/Screenshots/RunDetails%20Hyperdrive%202.jpg)

![Hyperdrive experiment results overview](https://github.com/icenine81/Capstone_udacity_ml_nanodegree/blob/6cf10bb0260932101cbfe6461ad887a606999ce5/Screenshots/Hyperdrive%20experiment%20overview.jpg)

![Hyperdrive experiment child run details](https://github.com/icenine81/Capstone_udacity_ml_nanodegree/blob/6cf10bb0260932101cbfe6461ad887a606999ce5/Screenshots/Hyperdrive%20experiment%20childrun%20details.jpg)

## Model Deployment
The best model was deployed as a webservice with a REST endpoint. The REST endpoint for the model is:

http://1df50e91-db34-42db-ac68-8307731487f8.eastus2.azurecontainer.io/score 

![AutoML model deployed - healthy state](https://github.com/icenine81/Capstone_udacity_ml_nanodegree/blob/6cf10bb0260932101cbfe6461ad887a606999ce5/Screenshots/AutoML%20Model%20Deployed.jpg)

The model was deployed using the Python SDK via the following steps:

- Register the best model and provide a name to use in the deployed service.
- Create a Deployment Configuration and Inference Configuration ![Deployment Config](https://github.com/icenine81/Capstone_udacity_ml_nanodegree/blob/9e32e25fc5116b923ef73db4d1373a5a1858e636/Screenshots/Model%20deployment%20configuration.jpg)
- Deploy the model as a web service using ACI (Azure Container Instances)
- Send a REST call with JSON-formatted input data to the REST API's scoring URI. Authentication is enabled so the key has to be known in order to use the REST endpoint. 
- The deployed model service will respond with a prediction. ![Model response](https://github.com/icenine81/Capstone_udacity_ml_nanodegree/blob/9e32e25fc5116b923ef73db4d1373a5a1858e636/Screenshots/Response%20from%20Deployed%20Model.jpg)

A prediction can be generated by passing input as a JSON file to the endpoint. One way to do so is via the endpoint.py file. 

The JSON-formatted API request input data should have the following format:

"data": [

  {

   "gender": "Male",

   "age": 67,

   "hypertension": "False",

   "heart_disease": "True",

   "ever_married": "True",

   "work_type": "Private",

   "Residence_type": "Urban",

   "avg_glucose_level": 228.69,

   "bmi": 36.6,

   "smoking_status": "formerly smoked"

  }]



As a final cleanup step, the Python SDK was also used to delete the compute cluster and the deployed model (i.e. service) via these commands:





## Screen Recording
A screencast walk-through of the model and the deployed service endpoint can be found at this [link](https://youtu.be/Gm7Plnt2wcU)

In the screencast, you can see that the model has been registered with Azure ML and application insights enabled. Data is sent to the deployed model in two ways. First, by using the endpoint.py script and second by using the Notebook and Python SDK to pass the request to the endpoint. The model responds with Result: False False, indicating that the sample patients' (two of them) whose data was submitted are unlikely to suffer from a stroke.

## Standout Suggestions
Application insights were enabled for the deployed model. ![Application Insights enabled for deployed model](https://github.com/icenine81/Capstone_udacity_ml_nanodegree/blob/9e32e25fc5116b923ef73db4d1373a5a1858e636/Screenshots/Deployed%20Model%20Application%20Insights.jpg)

Swagger API enabled and tested ![Swagger API utilized](https://github.com/icenine81/Capstone_udacity_ml_nanodegree/blob/9e32e25fc5116b923ef73db4d1373a5a1858e636/Screenshots/Swagger%20on%20localhost.jpg)

