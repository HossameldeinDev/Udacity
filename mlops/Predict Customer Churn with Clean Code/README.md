# Predict Customer Churn

This is the **Predict Customer Churn** project, part of the ML DevOps Engineer Nanodegree Program by Udacity.

## Project Description
In this project, we aim to identify potential churn customers for a banking institution. Using historical customer data, we apply machine learning models to predict which customers are more likely to churn. This enables proactive engagement with these customers to improve retention. Our project encapsulates the entire ML pipeline, including data preprocessing, exploratory data analysis, feature engineering, model training, evaluation, and saving the results.

## Files and Data Description
- `churn_library.py`: Main script containing functions for data import, preprocessing, exploratory data analysis (EDA), feature engineering, model training, and evaluation.
- `churn_script_logging_and_tests.py`: Contains unit tests for functions in `churn_library.py` and logs the outcomes of these tests.
- `data/`: Directory containing the dataset `bank_data.csv` used for analysis.
- `models/`: Directory where trained model objects are saved as `.pkl` files.
- `images/eda/`: Directory where exploratory data analysis plots are saved.
- `images/results/`: Directory where model evaluation and results plots are stored.
- `README.md`: This file, providing an overview and instructions for the project.

## Running Files
To run this project, follow these steps:

1. Ensure that all the necessary libraries are installed by running `python -m pip install -r requirements_py3.6.txt`.
2. Run `python churn_library.py` to perform the data analysis and modeling process. This will create EDA plots, train models, and save the results and model objects in their respective directories.
3. To test the functions and log the outcomes, run `python churn_script_logging_and_tests.py`. This will generate logs in `churn_tests.log`, documenting the success or failure of each test.

When you run `churn_library.py`, it will:
- Import and preprocess the data.
- Conduct exploratory data analysis, saving various plots in the `images/eda` directory.
- Perform feature engineering.
- Train logistic regression and random forest models, and save them in the `models` directory.
- Generate evaluation metrics and save the results in the `images/results` directory.

Running `churn_script_logging_and_tests.py` will:
- Perform unit tests for each function in `churn_library.py`.
- Log the test results to `churn_tests.log`, providing a detailed report of the testing process.
