"""
Test functions for churn_library.py script
Author: Hossameldein Elfayoumi
Creation Date: 04/01/2023
"""

import tempfile
import logging
import os

from churn_library import (import_data, perform_feature_engineering,
                           perform_eda, encoder_helper, train_models)

logging.basicConfig(
    filename="./churn_tests.log",
    filemode='a',
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)


def test_import():
    '''
    test data import - this example is completed for you to assist with the other test functions
    '''
    try:
        data_frame = import_data("./data/bank_data.csv")
        logging.info("Testing import_data: SUCCESS")
    except FileNotFoundError as err:
        logging.error("Testing import_eda: The file wasn't found")
        raise err

    try:
        assert data_frame.shape[0] > 0
        assert data_frame.shape[1] > 0
    except AssertionError as err:
        logging.error(
            "Testing import_data: The file doesn't appear to have rows and columns")
        raise err


# def test_eda():
#     '''
#     test perform eda function
#     '''
#     data_frame = import_data("./data/bank_data.csv")
#     try:
#         perform_eda(data_frame)
#         eda_images_directory = './images/eda'
#         assert os.path.exists(
#             eda_images_directory), "EDA images directory not created"
#         files = [
#             "churn_distribution.png",
#             "customer_age_distribution.png",
#             "martial_status_distribution.png",
#             "total_transaction_distribution.png",
#             "heatmap.png"]
#         for file in files:
#             assert os.path.isfile(
#                 os.path.join(
#                     eda_images_directory, file)), f"{file} not created"
#         logging.info("Testing perform_eda: SUCCESS")
#     except Exception as error:
#         logging.error("Testing perform_eda: Error occurred: %s", str(error))
#         raise error


def test_eda():
    '''
    test perform eda function
    '''
    with tempfile.TemporaryDirectory() as temp_dir:
        data_frame = import_data("./data/bank_data.csv")
        try:
            perform_eda(data_frame, eda_images_directory=temp_dir)
            files = [
                "churn_distribution.png",
                "customer_age_distribution.png",
                "martial_status_distribution.png",
                "total_transaction_distribution.png",
                "heatmap.png"]
            for file in files:
                assert os.path.isfile(
                    os.path.join(
                        temp_dir, file)), f"{file} not created"
            logging.info("Testing perform_eda: SUCCESS")
        except Exception as error:
            logging.error(
                "Testing perform_eda: Error occurred: %s",
                str(error))
            raise error


def test_encoder_helper():
    '''
    test encoder helper
    '''
    data_frame = import_data("./data/bank_data.csv")
    data_frame['Churn'] = data_frame['Attrition_Flag'].apply(
        lambda val: 0 if val == "Existing Customer" else 1)
    category_lst = [
        'Gender',
        'Education_Level',
        'Marital_Status',
        'Income_Category',
        'Card_Category']
    try:
        df_encoded = encoder_helper(data_frame, category_lst, 'Churn')
        for category in category_lst:
            assert f'{category}_Churn' in df_encoded.columns, f"{category}_Churn column not created"
        logging.info("Testing encoder_helper: SUCCESS")
    except AssertionError as error:
        logging.error("Testing encoder_helper: Error occurred: %s", str(error))
        raise error


def test_perform_feature_engineering():
    '''
    test perform_feature_engineering
    '''
    data_frame = import_data("./data/bank_data.csv")
    data_frame['Churn'] = data_frame['Attrition_Flag'].apply(
        lambda val: 0 if val == "Existing Customer" else 1)
    try:
        x_train, x_test, y_train, y_test = perform_feature_engineering(
            data_frame, 'Churn')
        assert x_train.shape[0] > 0 and x_test.shape[0] > 0, "Empty train or test set"
        assert y_train.shape[0] > 0 and y_test.shape[0] > 0, "Empty train or test target set"
        logging.info("Testing perform_feature_engineering: SUCCESS")
    except AssertionError as error:
        logging.error(
            "Testing perform_feature_engineering: Error occurred: %s",
            str(error))
        raise error


def test_train_models():
    '''
    test train_models with a smaller subset of data
    '''
    with tempfile.TemporaryDirectory() as temp_dir:
        data_frame = import_data("./data/bank_data.csv")
        data_frame['Churn'] = data_frame['Attrition_Flag'].apply(
            lambda val: 0 if val == "Existing Customer" else 1)

        df_sample = data_frame.sample(frac=0.1, random_state=42)
        x_train, x_test, y_train, y_test = perform_feature_engineering(
            df_sample, 'Churn')

        try:
            train_models(
                x_train,
                x_test,
                y_train,
                y_test,
                models_directory=temp_dir,
                results_images_directory=temp_dir)
            files = ["rfc_model.pkl", "logistic_model.pkl"]
            for file in files:
                assert os.path.isfile(
                    os.path.join(
                        temp_dir, file)), f"{file} not created"
            logging.info("Testing train_models: SUCCESS")
        except Exception as error:
            logging.error(
                "Testing train_models: Error occurred: %s",
                str(error))
            raise error


if __name__ == "__main__":
    # Test import_data function
    logging.info("Starting script execution.")

    test_import()

    # Test perform_eda function
    test_eda()

    # Test encoder_helper function
    test_encoder_helper()

    # Test perform_feature_engineering function
    test_perform_feature_engineering()

    # Test train_models function
    test_train_models()

    logging.info("All tests completed.")
