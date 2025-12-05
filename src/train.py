import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, f1_score, mean_squared_error, r2_score
import joblib
import mlflow
import mlflow.sklearn


def train(input_csv: str = 'data/cleaned.csv', models_dir: str = 'models'):
    df = pd.read_csv(input_csv)

    features = ['BHK', 'Size_in_SqFt', 'Price_per_SqFt', 'Age', 'Nearby_Schools', 'Nearby_Hospitals', 'PT_Score', 'Amenities_Count']

    # Ensure numeric columns
    for c in ['Nearby_Schools', 'Nearby_Hospitals']:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
        else:
            df[c] = 0

    X = df[features].fillna(0)
    y_clf = df['Good_Investment']
    y_reg = df['Future_Price_5Y']

    X_train, X_test, y_clf_train, y_clf_test, y_reg_train, y_reg_test = train_test_split(
        X, y_clf, y_reg, test_size=0.2, random_state=42
    )

    os.makedirs(models_dir, exist_ok=True)

    mlflow.set_experiment('realestate_training')
    with mlflow.start_run() as run:
        # Classifier
        clf = RandomForestClassifier(n_estimators=50, random_state=42)
        clf.fit(X_train, y_clf_train)
        preds = clf.predict(X_test)
        acc = accuracy_score(y_clf_test, preds)
        f1 = f1_score(y_clf_test, preds, zero_division=0)

        mlflow.log_param('clf', 'RandomForest')
        mlflow.log_metric('clf_accuracy', acc)
        mlflow.log_metric('clf_f1', f1)
        mlflow.sklearn.log_model(clf, 'classifier')

        joblib.dump(clf, os.path.join(models_dir, 'classifier.joblib'))

        # Regressor
        reg = RandomForestRegressor(n_estimators=50, random_state=42)
        reg.fit(X_train, y_reg_train)
        rpred = reg.predict(X_test)
        rmse = mean_squared_error(y_reg_test, rpred)
        rmse = rmse ** 0.5
        r2 = r2_score(y_reg_test, rpred)

        mlflow.log_param('reg', 'RandomForest')
        mlflow.log_metric('reg_rmse', rmse)
        mlflow.log_metric('reg_r2', r2)
        mlflow.sklearn.log_model(reg, 'regressor')

        joblib.dump(reg, os.path.join(models_dir, 'regressor.joblib'))

        print('Classifier acc:', acc, 'f1:', f1)
        print('Regressor rmse:', rmse, 'r2:', r2)
        print('Models saved to', models_dir)


if __name__ == '__main__':
    train()
