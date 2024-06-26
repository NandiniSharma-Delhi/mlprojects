import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import(

    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object,evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Split trainign and test input data")
            x_train,y_train,x_test,y_test =(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1],
            )
            models={
                "Random Forest":RandomForestRegressor(),
                "Decision Tree":DecisionTreeRegressor(),
                "Gradient Boosting":GradientBoostingRegressor(),
                "Linear Regression":LinearRegression(),
                "K-Neighbours Classifier":KNeighborsRegressor(),
                "XGBClassifier":XGBRegressor(),
                "Catboosting Classifier":CatBoostRegressor(verbose=False),
                "Adaboost Classifier":AdaBoostRegressor(),

            }
            model_report:dict = evaluate_models(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models = models)
            best_model_name=list(model_report.keys())[0]
            best_model_score = model_report[best_model_name]
            for i in model_report:
                if(model_report[i]>best_model_score):
                    best_model_score=model_report[i]
                    best_model_name=i

            best_model = models[best_model_name]
            if best_model_score<0.6:
                raise CustomException("No best model found")
            logging.info("Best model found on both training and test dataset")
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
            predicted = best_model.predict(x_test)
            r2_square = r2_score(y_test,predicted)
            return r2_square

        except Exception as e:
            raise CustomException(e,sys)



