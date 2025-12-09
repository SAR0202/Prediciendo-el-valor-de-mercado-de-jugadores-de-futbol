  # Prediciendo-el-valor-de-mercado-de-jugadores-de-f-tbol-Predicting-football-players-market-value
#ADECUAR A LOS NUEVOS CAMBIOS

En este proyecto usé las bases de datos disponibles en www.kaggle.com/datasets/davidcariboo/player-scores con datos de Transfermarkt.Me propongo entrenar 2 modelos,uno Random Forest y otro XGB, que predigan el valor de mercado de jugadores de futbol de las 5 mayores ligas de Europa(Premier league, Serie A, LaLiga, Bundesliga, Ligue 1) en el periodo 2018-2024 para luego comparar métricas.
  
Dado que el periodo de tiempo elegido abarca varios años decidí que la variable objetivo sea el valor real del jugador durante la última temporada que jugó en su respectiva liga (los precios los actualizo a partir de los datos de inflación de la zona euro, publicados por el Banco Mundial).

Resumen:
      
    -Trabajando los datos:
        -Integré los datos de 5 database en un solo dataframe.
        -No eliminé outliers, empeoraba la performance.
        -Eliminé datos faltantes que podrian romper el modelo.
        -Creé nuevos atributos(efectividad,jugador ofensivo,arquero).
        -Definí variable objetivo(valor real) y variables independientes.
          -Definí variables categoricas y númericas a utilizar.
        -Particioné el data set en train y test.
    -Transformación de la informacino relevante
        -Binarización de variables categoricas y uso de Simple Imputer para faltantes(estrategia constante)
    -Random Forest:
        -Definición del modelo a usar(RF)
        -Búsqueda de hiperparametros con Randomized grid search(100 iteraciones)
        -Gráfico de importancia de atributos
    -XGB:
        -Definición del modelo a usar
        -Búsqueda de hiperparametros con Randomized search(100 iteraciones)
        -Gráfico de importancia de atributos

    -Metricas aproximadas de cada modelo:
               |    RF       | XGB
    -------------------------------------------
    MAE        | ~ 1.400.000 |  ~1.596.506,819|
    ------------------------------------------
    RMSE       | ~ 4.000.000 |  ~3.951.283,289|
    ------------------------------------------
    R2         |    ~ 0.82   |   ~0.8740      |
    ------------------------------------------
    R2_ajustado|    ~0.81    |   ~0.8725      |
    ------------------------------------------
    MAE/MEDIA  |     ~32%    |    0.3322      |
    ------------------------------------------
  Proceso completo:

Para empezar, el proyecto esta compuesto por 5 archivos:
    
    -tratamiento_de_datos.ipynb (1)
    -division_y_preproceso.py (2)
    -funciones_varias.py (3)
    -Modelo_RF (4)
    -Modelo_XGB (5)

En el primer archivo extraigo toda la información necesaria de los 5 datasets que se utilizaron(competitions,clubs,players,game_events,game_lineups) y creo nuevos atributos entre los que esta la variable objetivo, el "valor_real" de mercado de cada jugador. Uso valor real para actualizar por inflación el valor de mercado de cada jugador y tener un valor comparable en cada momento(recordar que el dataset tiene datos del 2018 hasta el 2024). Una vez terminado con eso paso a una breve seccion de estadistica descriptiva del dataset que incluye los siguientes graficos:
      
-------Grafico 1,distribucion del valor real de los jugadores: En este gráfico se puede observar que la mayoria de observaciones se ubican en el lado izquierdo del grafico,marcando.....

-------Gráfico 2,Distribución de posiciones:se puede observar que la posicion con mas jugadores es la de Defensor Central, seguida por.... 

-------Gráfico 3,matriz de correlaciones: este último grafico permite ver las correlaciones entre variables numericas del dataset, se puede ver que la mayor correlacion de

Este archivo tambien contiene el calculo de rangos intercuartilicos para la eliminación de outliers, aunque no se lleva a cabo porque luego de varios intentos note que sacar outliers empeoraba la predicción(posiblemente por la poca cantidad de datos que tiene el dataset final, alrededor de 7000 observaciones).Luego se eliminan columnas que no se van a utilizar y se deshechan observaciones con NaN que empeoraban el modelo o imposibilitaban la predicción. Lo último que hace el archivo 1 es descargar el DataFrame final a un archivo csv para poder usarlo en el entrenamiento de los modelos.

El archivo division_y_preproceso contiene una funcion homónima que toma como argumento la dirección(path) del archivo csv descargado por el archivo 1. Esta funcion define la variable objetivo, las columnas categóricas y numericas y su tratamiento(OHE y SimpleImputer) y también particiona el dataset en train y test. La función devuelve los dataframes de X_train,X_test,y_train,y_test y el preprocesamiento de las columnas (para poner directamente en el pipeline)


  Empecé por extraer toda la información necesaria de las 5 bases de datos y unirla en un solo DataFrame..Luego de correr el modelo observe que el quitar outliers respecto al precio con rango intercuatílico empeoraba la predicción por lo que opté por dejar cualquier outlier que haya en el dataset. Una vez que todos los datasets estuvieron unidos en un solo dataframe creé algunos atributos que mejoraron marginalmente las predicciones y definí variables categoricas y numéricas que pasarán por el preproceso. Luego particioné el dataframe en train y test y definí las variables dependientes y la variable objetivo(valor real del pase). Después establecí el preproceso de la información que iría al pipeline con OneHotEncoder para las variables binarias y un Simple Imputer que llenará valores faltantes con cero.
  
  El modelo predictivo RF que uso es simple, utilizo un randomized grid search con 100 iteraciones para la búsqueda de hiperparametros buscando minimizar el error medio absoluto(MAE) porque es la métrica que uso como referencia en este caso.Uso los hiperpárametros mas comúnes con valores conservadores que buscan evitar el overfitting del modelo. Luego hago el .fit() del modelo, predigo sobre la porción de test e informo MAE,RMSE,R2,R2 ajustado y la relación MAE/MEDIA. 


  Las librerias que usé fueron Pandas, Numpy y scikit-learn


Posibles mejoras:

Se podria usar un modelo de stacking con los dos modelos usados y un modelo LASSO como metamodelo,además, se podria usaar la libreria optuna para la búsqueda de hiperparametros óptimos.
