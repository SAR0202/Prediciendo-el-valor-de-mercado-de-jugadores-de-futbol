import pandas as pd
import numpy as np

def competencias_int(df_games,id_copa,diccio_jerarquia,year_of_interest_int):
    df_games = df_games.copy()
    df_games = df_games[(df_games["round"].str.contains("Final|Group")&(df_games["season"]>=year_of_interest_int))]
    #Estandarizo Rondas
    df_games["round"] = np.where(df_games["round"].isin(["Quarter-Finals 1st leg", "Quarter-Finals 2nd leg", "Quarter-Finals"]),"Cuartos-Final", df_games["round"])
    df_games["round"] = np.where(df_games["round"].isin(["Semi-Finals 1st Leg", "Semi-Finals 2nd Leg", "Semi-Finals"]),"Semi-Final", df_games["round"])
    df_games["round"] = np.where(df_games["round"].isin(["Group A", "Group B", "Group C", "Group D", "Group E", "Group F", "Group G", "Group H", "Group Stage"]),"Fase-Grupos", df_games["round"])

    jerarquia_rondas=diccio_jerarquia

    df_copa = df_games[(df_games["competition_id"] == id_copa)&(df_games["season"] >= year_of_interest_int)].copy()
    df_copa["jerarquia_rondas"] = df_copa["round"].map(jerarquia_rondas)

    df_copa_idaway=df_copa[["away_club_id","round","season","jerarquia_rondas"]].rename(columns={"away_club_id":"club_id"})
    df_copa_idhome=df_copa[["home_club_id","round","season","jerarquia_rondas"]].rename(columns={"home_club_id":"club_id"})
    df_conca=pd.concat([df_copa_idaway, df_copa_idhome], ignore_index=True)

    df_final=df_conca.groupby(["club_id","season"])["jerarquia_rondas"].max().reset_index()
    df_final = df_final.rename(columns={"jerarquia_rondas": f"jerarquia_rondas_{id_copa}"})
    return df_final
def jugadores_clubs_primera(lista_paises,df_comp,df_clubes,df_jugadores,year_of_interest_int):


    df_comp_it = df_comp[(df_comp["country_name"].isin(lista_paises)) & (df_comp["type"] == "domestic_league")]
    id_comp = df_comp_it["competition_id"].tolist()

    df_clubes_1 = df_clubes[(df_clubes["domestic_competition_id"].isin(id_comp)) & (df_clubes["last_season"] >= year_of_interest_int)]
    lista_club_1 = df_clubes_1["name"].tolist()

    df_jugadores = df_jugadores[(df_jugadores["current_club_name"].isin(lista_club_1)) & (df_jugadores["last_season"] >= year_of_interest_int)].copy()

    return df_jugadores

def inf_acum(año):
    inflacion = [1.74118084746924, 1.87084961406325, 2.84327019799065, 3.18466272791609, 3.86856354936628,3.90803782779623,
             3.87365401861331, 3.45533218314714, 2.76486447339765, 2.65725273386971, 4.37282441582136,5.24097448273095,
             6.06300309718188, 8.02220995878935, 13.6493174728139, 12.7681985920515, 9.79734643716299,10.6439507951549,
             7.75523144587006, 9.05684784238687, 12.5785990487562, 13.3144055680071, 11.9784719523806,9.45954847235317,
             7.67380262247321, 5.39548620170352, 2.93357920442327, 3.28889821400134, 2.70081527508112,4.08905388153545,
             3.44831217961808, 4.04703259753466, 5.16378397662331, 4.5218241221731, 3.50262577413398,3.37384030440144,
             2.57299919930232, 2.00709087666531, 1.95711094996816, 1.66345995007715, 2.85303039287157,2.72449326646328,
             2.63323912175956, 2.38551385959886, 2.21620788926273, 2.47212179047864, 2.7200475052927,2.48231546689541,
             4.11407022033816, 0.437175412792704, 1.5205755786839, 3.28801427219793, 2.54154474108013,1.31023355618665,
             0.220195628198783, -0.085207229696361, 0.166009884375597, 1.37503641525343, 1.68923965804135,1.44123966942342, 0.186938139702113, 2.48650438120822, 8.4711764559089, 5.78431554960867,2.18497406958038]
    year = [i for i in range(1960, 2025)]
    indice = year.index(año)
    inflacion = inflacion[indice:]
    acum = 1
    for i in inflacion:
        i = i / 100
        acum = acum * (1 + i)
    acum_f = acum
    return (acum_f - 1)