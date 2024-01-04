"""
Churn Library Module for the churn prediction model project,
    including functions for importing data, performing EDA,
    feature engineering, and training models.
Author: Hossameldein Elfayoumi
Creation Date: 04/01/2023
"""

# library doc string
import os
from sklearn.metrics import plot_roc_curve, classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set()

# import libraries


os.environ['QT_QPA_PLATFORM'] = 'offscreen'


def import_data(pth):
    '''
    Import data from a CSV file into a pandas DataFrame.
    Parameters:
        pth (str): A string representing the file path to the CSV file.
    Returns:
        DataFrame: A pandas DataFrame containing the data from the CSV file.
    '''

    print(f"Importing data from {pth}")
    imported_df = pd.read_csv(pth)
    print(f"Successfully imported data from {pth}")
    print(f"Dataframe head: {imported_df.head()}")
    return imported_df


def perform_eda(data_frame, eda_images_directory='./images/eda'):
    '''
    Perform exploratory data analysis (EDA) on the given DataFrame and save the resulting figures.
    This function generates histograms and a correlation heatmap,
     saving each figure in the images/eda directory.
    Parameters:
        data_frame (DataFrame): The pandas DataFrame on which to perform EDA.
        eda_images_directory (str): The directory where the EDA images will be saved.
    Returns:
        None: This function does not return any value.
    '''

    print("Start Exploratory Data Analysis")
    print(f"Performing EDA: Dataframe shape: {data_frame.shape}", )
    print(
        f"Performing EDA: Checking for null values {data_frame.isnull().sum()}")
    print(
        f"Performing EDA: View descriptive statistics {data_frame.describe()}")
    data_frame['Churn'] = data_frame['Attrition_Flag'].apply(
        lambda val: 0 if val == "Existing Customer" else 1)
    if not os.path.exists(eda_images_directory):
        os.makedirs(eda_images_directory)
    print(f"All plots saved in {eda_images_directory}")
    print("Performing EDA: Plot histogram of Churn")
    plt.figure(figsize=(20, 10))
    data_frame['Churn'].hist()
    plt.savefig(os.path.join(eda_images_directory, 'churn_distribution.png'))
    plt.close()
    print("Performing EDA: Plot histogram of Customer Age")
    plt.figure(figsize=(20, 10))
    data_frame['Customer_Age'].hist()
    plt.savefig(
        os.path.join(
            eda_images_directory,
            'customer_age_distribution.png'))
    plt.close()
    print("Performing EDA: Plot histogram of Martial Status")
    plt.figure(figsize=(20, 10))
    # pylint: disable=no-member
    colors = plt.cm.tab20.colors
    data_frame.Marital_Status.value_counts(
        'normalize').plot(kind='bar', color=colors)
    plt.savefig(
        os.path.join(
            eda_images_directory,
            'martial_status_distribution.png'))
    plt.close()
    print("Performing EDA: Plot histogram of Total Transaction")
    plt.figure(figsize=(20, 10))
    sns.histplot(data_frame['Total_Trans_Ct'], stat='density', kde=True)
    plt.savefig(
        os.path.join(
            eda_images_directory,
            'total_transaction_distribution.png'))
    plt.close()
    print("Performing EDA: Plot heatmap of correlation matrix")
    plt.figure(figsize=(20, 15))
    sns.heatmap(
        data_frame.select_dtypes(
            include=[
                np.number]).corr(),
        annot=False,
        cmap='Dark2_r',
        linewidths=2)
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.savefig(os.path.join(eda_images_directory, 'heatmap.png'))
    plt.close()


def perform_feature_engineering(data_frame, response):
    '''
    Perform feature engineering on the given DataFrame and
    split the data into training and testing sets.
    Parameters:
        data_frame (DataFrame): The pandas DataFrame to be processed.
        response (str): The name of the response column.
    Returns:
        tuple: A tuple containing four elements (X_train, X_test, y_train, y_test)
         which are the split
        training and testing sets for features and response variable.
    '''

    print("Start Feature Engineering")
    print(
        f"Feature Engineering: Choosing {response} as response variable")
    y_axis = data_frame[response]
    category_list = [
        'Gender',
        'Education_Level',
        'Marital_Status',
        'Income_Category',
        'Card_Category']
    print("Feature Engineering: encode categorical variables")
    data_frame = encoder_helper(data_frame, category_list, response)
    keep_cols = [
        'Customer_Age',
        'Dependent_count',
        'Months_on_book',
        'Total_Relationship_Count',
        'Months_Inactive_12_mon',
        'Contacts_Count_12_mon',
        'Credit_Limit',
        'Total_Revolving_Bal',
        'Avg_Open_To_Buy',
        'Total_Amt_Chng_Q4_Q1',
        'Total_Trans_Amt',
        'Total_Trans_Ct',
        'Total_Ct_Chng_Q4_Q1',
        'Avg_Utilization_Ratio',
        'Gender_Churn',
        'Education_Level_Churn',
        'Marital_Status_Churn',
        'Income_Category_Churn',
        'Card_Category_Churn']
    x_axis_features = pd.DataFrame()
    x_axis_features[keep_cols] = data_frame[keep_cols]
    return train_test_split(
        x_axis_features,
        y_axis,
        test_size=0.3,
        random_state=42)


def encoder_helper(data_frame, category_lst, response):
    '''
    Transform categorical columns in the DataFrame into new columns representing the proportion of
    churn for each category. This is used for encoding categorical features.
    Parameters:
        data_frame (DataFrame): The pandas DataFrame to be processed.
        category_lst (list): A list of strings representing the names of the categorical columns.
        response (str): The name of the response column to calculate the proportions against.
    Returns:
        DataFrame: The modified pandas DataFrame with new columns for each categorical feature
        representing the proportion of churn.
    '''

    print("Feature Engineering: Encode categorical variables")
    mappings = {category: data_frame.groupby(category)[response].mean()
                for category in category_lst}

    for category in category_lst:
        print(f"Feature Engineering: Encode {category}")
        new_column_name = f'{category}_{response}'
        data_frame[new_column_name] = data_frame[category].map(
            mappings[category])
    return data_frame


def classification_report_image(y_train,
                                y_test,
                                y_train_preds_lr,
                                y_train_preds_rf,
                                y_test_preds_lr,
                                y_test_preds_rf,
                                results_images_directory):
    '''
    Generate and save classification report images for training and
    testing results of logistic regression
    and random forest models.
    Parameters:
        y_train (array): Array of training response values.
        y_test (array): Array of testing response values.
        y_train_preds_lr (array): Predictions from logistic regression on the training set.
        y_train_preds_rf (array): Predictions from random forest on the training set.
        y_test_preds_lr (array): Predictions from logistic regression on the testing set.
        y_test_preds_rf (array): Predictions from random forest on the testing set.
        results_images_directory (str): Path to the directory where result images will be saved.
    Returns:
        None: This function does not return any value but saves images to the specified directory.
    '''

    print("Start Classification Report")
    print("Classification Report: Random Forest")
    plt.figure(figsize=(10, 5))  # Adjusted figure size
    plt.text(0.01, 1.25, str('Random Forest Train'), {
        'fontsize': 10}, fontproperties='monospace')
    plt.text(
        0.01, 0.05, str(
            classification_report(
                y_test, y_test_preds_rf)), {
            'fontsize': 10}, fontproperties='monospace')
    plt.text(0.01, 0.6, str('Random Forest Test'), {
        'fontsize': 10}, fontproperties='monospace')
    plt.text(
        0.01, 0.7, str(
            classification_report(
                y_train, y_train_preds_rf)), {
            'fontsize': 10}, fontproperties='monospace')
    plt.axis('off')
    plt.savefig(results_images_directory + '/rf_results.png')
    plt.close()
    print(
        f"Classification Report: Report Image Saved in {results_images_directory}" +
        "/rf_results.png ")

    print("Classification Report: Logistic Regression")
    plt.figure(figsize=(10, 5))
    plt.text(0.01, 1.25, str('Logistic Regression Train'),
             {'fontsize': 10}, fontproperties='monospace')
    plt.text(
        0.01, 0.05, str(
            classification_report(
                y_train, y_train_preds_lr)), {
            'fontsize': 10}, fontproperties='monospace')
    plt.text(0.01, 0.6, str('Logistic Regression Test'), {
        'fontsize': 10}, fontproperties='monospace')
    plt.text(
        0.01, 0.7, str(
            classification_report(
                y_test, y_test_preds_lr)), {
            'fontsize': 10}, fontproperties='monospace')
    plt.axis('off')
    plt.savefig(results_images_directory + '/logistic_results.png')
    plt.close()
    print(
        f"Classification Report: Report Image Saved in {results_images_directory}" +
        "/logistic_results.png ")


def feature_importance_plot(model, x_data, output_pth):
    '''
    Create and save a plot of feature importances from a given model.
    Parameters:
        model (model object): A trained model object that contains
         the attribute 'feature_importances_'.
        x_data (DataFrame): The pandas DataFrame of features used in the model.
        output_pth (str): Path to the directory where the feature importance plot will be saved.
    Returns:
        None: This function does not return any value but saves a plot to the specified directory.
    '''

    print("Start Feature Importance Plot")
    # Adjust the size of the plot and the layout
    plt.figure(figsize=(20, 10))

    # Calculate feature importances
    importances = model.best_estimator_.feature_importances_
    # Sort feature importances in descending order
    indices = np.argsort(importances)[::-1]

    # Rearrange feature names so they match the sorted feature importances
    names = [x_data.columns[i] for i in indices]

    # Create plot title
    plt.title("Feature Importance")
    plt.ylabel('Importance')

    # Add bars
    plt.bar(range(x_data.shape[1]), importances[indices])

    # Add feature names as x-axis labels
    plt.xticks(range(x_data.shape[1]), names, rotation=90)

    # Adjust layout
    # Automatically adjust subplot params to give specified padding.
    plt.tight_layout()

    # Save the plot
    if not os.path.exists(output_pth):
        os.makedirs(output_pth)
    print(
        f"Feature Importance Plot: Saved in {output_pth}" +
        "/feature_importance.png")
    plt.savefig(os.path.join(output_pth, "feature_importance.png"))
    plt.close()


def train_models(x_train, x_test, y_train, y_test, models_directory='./models',
                 results_images_directory='./images/results'):
    '''
    Train models, save the model results (as images and scores), and store the model objects.
    This function handles training for both logistic regression and random forest models.
    Parameters:
        x_train (DataFrame): The training data set for features.
        x_test (DataFrame): The testing data set for features.
        y_train (array): The training data set for the response variable.
        y_test (array): The testing data set for the response variable.
        models_directory (str): Path to the directory where models will be saved.
        results_images_directory (str): Path to the directory where result images will be saved.
    Returns:
        None: This function does not return any value but saves
         model results and the models themselves.
    '''
    print("Start Training Models")
    rfc = RandomForestClassifier(random_state=42)
    lrc = LogisticRegression(solver='lbfgs', max_iter=3000)
    param_grid = {
        'n_estimators': [200, 500],
        'max_features': ['auto', 'sqrt'],
        'max_depth': [4, 5, 100],
        'criterion': ['gini', 'entropy']
    }
    print("Training Models: Random Forest")
    cv_rfc = GridSearchCV(estimator=rfc, param_grid=param_grid, cv=5)
    cv_rfc.fit(x_train, y_train)
    print("Training Models: Logistic Regression")
    lrc.fit(x_train, y_train)
    print("Compute Model Scores: Random Forest")
    y_train_preds_rf = cv_rfc.best_estimator_.predict(x_train)
    y_test_preds_rf = cv_rfc.best_estimator_.predict(x_test)
    print("Compute Model Scores: Logistic Regression")
    y_train_preds_lr = lrc.predict(x_train)
    y_test_preds_lr = lrc.predict(x_test)

    # scores
    print('random forest results')
    print('test results')
    print(classification_report(y_test, y_test_preds_rf))
    print('train results')
    print(classification_report(y_train, y_train_preds_rf))

    print('logistic regression results')
    print('test results')
    print(classification_report(y_test, y_test_preds_lr))
    print('train results')
    print(classification_report(y_train, y_train_preds_lr))
    if not os.path.exists(results_images_directory):
        os.makedirs(results_images_directory)
    print(
        f"Save classification report results plot in"
        f" {os.path.join(results_images_directory, 'roc_curve_result.png')}")
    lrc_plot = plot_roc_curve(lrc, x_test, y_test)
    plt.figure(figsize=(15, 8))
    current_axis = plt.gca()
    plot_roc_curve(
        cv_rfc.best_estimator_,
        x_test,
        y_test,
        ax=current_axis,
        alpha=0.8)
    lrc_plot.plot(ax=current_axis, alpha=0.8)
    plt.savefig(os.path.join(results_images_directory, "roc_curve_result.png"))
    plt.close()

    if not os.path.exists(models_directory):
        os.makedirs(models_directory)
    print("Save Models")
    print(
        f"Save Models: Random Forest in {os.path.join(models_directory, 'rfc_model.pkl')}")
    joblib.dump(
        cv_rfc.best_estimator_,
        os.path.join(
            models_directory,
            'rfc_model.pkl'))
    print(
        f"Save Models: Logistic Regression in"
        f" {os.path.join(models_directory, 'logistic_model.pkl')}")
    joblib.dump(lrc, os.path.join(models_directory, 'logistic_model.pkl'))
    classification_report_image(y_train,
                                y_test,
                                y_train_preds_lr,
                                y_train_preds_rf,
                                y_test_preds_lr,
                                y_test_preds_rf,
                                results_images_directory)
    feature_importance_plot(cv_rfc, x_train, results_images_directory)


if __name__ == "__main__":
    FILE_PATH = r"./data/bank_data.csv"
    df = import_data(pth=FILE_PATH)
    perform_eda(data_frame=df)
    X_train, X_test, Y_train, Y_test = perform_feature_engineering(
        data_frame=df, response='Churn')
    train_models(
        x_train=X_train,
        x_test=X_test,
        y_train=Y_train,
        y_test=Y_test)
    print("Train Completed")
