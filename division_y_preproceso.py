import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer


def division_y_preproceso(direccion_df_final):
    df_final = pd.read_csv(direccion_df_final)
    #variables a USAR
    X = df_final.drop("valor_real", axis=1)
    y = df_final["valor_real"]

    categoricas = X.select_dtypes(include=["object"]).columns.to_list()
    numericas = X.select_dtypes(include=["int64", "float64"]).columns.tolist()

    # DIVISION del dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=123)
    
    preproceso = ColumnTransformer(transformers=[
        ("cat", OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False), categoricas),
        ("num", SimpleImputer(strategy="constant", fill_value=0), numericas)  #
    ])

    return X_train, X_test, y_train, y_test, preproceso
