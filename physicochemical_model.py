import pandas as pd
import numpy as np
from scipy.stats import norm

import random
import statistics
import pathlib

def cement_carbonation(
    year_len,index_year2020,
    Belite_share,Belite_alk_save,
    BYF_share,BYF_alk_save,
    CCSC_share,CCSC_alk_save,
    CSAB_share,CSAB_alk_save,
    Celite_share,Celite_alk_save,
    MOMS_share,MOMS_alk_save,
    CO2_curing_share,CO2_curing_coef,
    CO2_mine_EOL_share,CO2_mine_EOL_coef,
    clinker,Cement_demand,waste_saving,
    scenario_index,
    Life,
    Std,
    reuse_rate,recRate,burRate,store_t,
    filepath
):

    Chem_alk_reduction = Belite_share*Belite_alk_save + BYF_share*BYF_alk_save +\
    CCSC_share*CCSC_alk_save + CSAB_share*CSAB_alk_save +\
    Celite_share*Celite_alk_save + MOMS_share*MOMS_alk_save

    Curing_coef_increase = CO2_curing_share*CO2_curing_coef
    Mine_coef_increase   = CO2_mine_EOL_share*CO2_mine_EOL_coef

    Beta_ad_random = []
    Beta_CO2_random = []
    Beta_CC_random = []
    
    for i in range(0,1000):
        random.seed(a=i);Beta_ad_random.append(random.weibullvariate(alpha = 1.16, beta = 20))
        random.seed(a=i);Beta_CO2_random.append(random.weibullvariate(alpha = 1.18, beta = 25))
        random.seed(a=i);Beta_CC_random.append(random.weibullvariate(alpha = 1, beta = 6))
    
    Beta_ad = statistics.median(Beta_ad_random)
    Beta_CO2 = statistics.median(Beta_CO2_random)
    Beta_CC = statistics.median(Beta_CC_random)

    impact_factor = Beta_ad * Beta_CO2 * Beta_CC

    coefC15_random = []; coefC16_random = []; coefC23_random = []; coefC35_random = []
    coefC15B_random = []; coefC16B_random = []; coefC23B_random = []; coefC35B_random = []

    for i in range(0,1000):
        random.seed(a=i);coefC15_random.append(random.uniform(a = 15, b = 5))
        random.seed(a=i);coefC16_random.append(random.uniform(a = 9, b = 2.5))
        random.seed(a=i);coefC23_random.append(random.uniform(a = 6, b = 1.5))
        random.seed(a=i);coefC35_random.append(random.uniform(a = 3.5, b = 1))
        
        random.seed(a=i);coefC15B_random.append(random.uniform(a = 3, b = 2))
        random.seed(a=i);coefC16B_random.append(random.uniform(a = 1.5, b = 1))
        random.seed(a=i);coefC23B_random.append(random.uniform(a = 1, b = 0.75))
        random.seed(a=i);coefC35B_random.append(random.uniform(a = 0.75, b = 0.5))

    coefC15 = statistics.median(coefC15_random) * impact_factor * (1+Curing_coef_increase)
    coefC16 = statistics.median(coefC16_random) * impact_factor * (1+Curing_coef_increase)
    coefC23 = statistics.median(coefC23_random) * impact_factor * (1+Curing_coef_increase)
    coefC35 = statistics.median(coefC35_random) * impact_factor * (1+Curing_coef_increase)
    
    coefC15B = statistics.median(coefC15B_random) * impact_factor * (1+Mine_coef_increase)
    coefC16B = statistics.median(coefC16B_random) * impact_factor * (1+Mine_coef_increase)
    coefC23B = statistics.median(coefC23B_random) * impact_factor * (1+Mine_coef_increase)
    coefC35B = statistics.median(coefC35B_random) * impact_factor * (1+Mine_coef_increase)


    wallthick_random = []
    
    for i in range(0,1000):
        random.seed(a=i);wallthick_random.append(random.uniform(a = 610, b = 60)/2)
    
    wallthick = statistics.median(wallthick_random)

    caocontent = 0.658*(1-Chem_alk_reduction)

    convertconcrete_random = []

    for i in range(0,1000):
        random.seed(a=i);convertconcrete_random.append(random.weibullvariate(alpha = 0.86, beta = 25))

    convertconcrete = statistics.median(convertconcrete_random) * 0.784808140177683

    C15percentage_random = []; C16percentage_random = []
    C23percentage_random = []; C35percentage_random = []

    for i in range(0,1000):
        random.seed(a=i);C15percentage_random.append(0.793*random.weibullvariate(alpha = 0, beta = 12))
        random.seed(a=i);C16percentage_random.append(0.793*random.weibullvariate(alpha = 0.3548, beta = 12))
        random.seed(a=i);C23percentage_random.append(0.793*random.weibullvariate(alpha = 0.4134, beta = 16))
        random.seed(a=i);C35percentage_random.append(0.793*random.weibullvariate(alpha = 0.2713, beta = 12))

    C15percentage = statistics.median(C15percentage_random)
    C16percentage = statistics.median(C16percentage_random)
    C23percentage = statistics.median(C23percentage_random)
    C35percentage = statistics.median(C35percentage_random)

    RENpercentage_random = []
    MASpercentage_random = []
    MAIpercentage_random = []

    for i in range(0,1000):
        random.seed(a=i);RENpercentage_random.append(0.207*random.weibullvariate(alpha = 0.524, beta = 14))
        random.seed(a=i);MASpercentage_random.append(0.207*random.weibullvariate(alpha = 0.188, beta = 12))
        random.seed(a=i);MAIpercentage_random.append(0.207*random.weibullvariate(alpha = 0.332, beta = 10))

    RENpercentage = statistics.median(RENpercentage_random)
    MASpercentage = statistics.median(MASpercentage_random)
    MAIpercentage = statistics.median(MAIpercentage_random)

    RENthick_random = []
    MASthick_random = []
    MAIthick_random = []

    for i in range(0,1000):
        random.seed(a=i);RENthick_random.append(random.weibullvariate(alpha = 22, beta = 4))
        random.seed(a=i);MASthick_random.append(random.uniform(a = 610, b = 60)/2)
        random.seed(a=i);MAIthick_random.append(random.weibullvariate(alpha = 26.8, beta = 7))

    RENthick = statistics.median(RENthick_random)
    MASthick = statistics.median(MASthick_random)
    MAIthick = statistics.median(MAIthick_random)

    coefMortar_random = []

    for i in range(0,1000):
        random.seed(a=i);coefMortar_random.append(random.triangular(low = 6.1, high = 36.8, mode = 19.6))

    coefMortar = statistics.median(coefMortar_random) * (1+Curing_coef_increase)

    convertmortar_random = []

    for i in range(0,1000):
        random.seed(a=i);convertmortar_random.append(random.weibullvariate(alpha = 0.92, beta = 20))

    convertmortar = statistics.median(convertmortar_random) * 0.784808140177683

    radiusRec_random = []; radiusBur_random = []
    radiusRecA_random = []; radiusRecB_random = []
    radiusBurA_random = []; radiusBurB_random = []

    for i in range(0,1000):
        random.seed(a=i);radiusRec_random.append(
            random.uniform(a = 0.15, b= 0.37)*2.5+random.uniform(a = 0.12, b= 0.23)*3.75+
            random.uniform(a = 0.24, b= 0.46)*7.5+random.uniform(a = 0.16, b= 0.39)*15)

        random.seed(a=i);radiusBur_random.append((
            (random.uniform(a = 0.1, b= 0.247)*0.5+random.uniform(a = 0.203, b= 0.28)*2.75+
             random.uniform(a = 0.353, b= 0.513)*10+random.uniform(a = 0.107, b= 0.26)*20.75)*0.12757+
            (random.uniform(a = 0.122, b= 0.256)*5+random.uniform(a = 0.195, b= 0.354)*10+
             random.uniform(a = 0.106, b= 0.225)*20+random.uniform(a = 0.248, b= 0.484)*25)*0.86872+
            (random.uniform(a = 0.15, b= 0.37)*2.5+random.uniform(a = 0.12, b= 0.23)*3.75+
             random.uniform(a = 0.24, b= 0.46)*7.5+random.uniform(a = 0.16, b= 0.39)*15)*0)/
            (0.12757 + 0.86872 + 0))

        random.seed(a=i);radiusRecA_random.append(
            random.uniform(a = 0.15, b= 0.37)*2.5+random.uniform(a = 0.12, b= 0.23)*2.5+
            random.uniform(a = 0.24, b= 0.46)*5+random.uniform(a = 0.16, b= 0.39)*10)
        
        random.seed(a=i);radiusRecB_random.append(
            random.uniform(a = 0.15, b= 0.37)*2.5+random.uniform(a = 0.12, b= 0.23)*5+
            random.uniform(a = 0.24, b= 0.46)*10+random.uniform(a = 0.16, b= 0.39)*20)

        random.seed(a=i);radiusBurA_random.append((
            (random.uniform(a = 0.1, b= 0.247)*0.5+
            random.uniform(a = 0.203, b= 0.28)*0.5+
            random.uniform(a = 0.353, b= 0.513)*5+
            random.uniform(a = 0.107, b= 0.26)*15)*0.12757+

            (random.uniform(a = 0.122, b= 0.256)*5+
            random.uniform(a = 0.195, b= 0.354)*5+
            random.uniform(a = 0.106, b= 0.225)*15+
            random.uniform(a = 0.248, b= 0.484)*25)*0.86872+

            (random.uniform(a = 0.15, b= 0.37)*2.5+
            random.uniform(a = 0.12, b= 0.23)*2.5+
            random.uniform(a = 0.24, b= 0.46)*5+
            random.uniform(a = 0.16, b= 0.39)*10)*0)/
            (0.12757 + 0.86872 + 0))

        random.seed(a=i);radiusBurB_random.append((
            (random.uniform(a = 0.1, b= 0.247)*0.5+
            random.uniform(a = 0.203, b= 0.28)*5+
            random.uniform(a = 0.353, b= 0.513)*15+
            random.uniform(a = 0.107, b= 0.26)*26.5)*0.12757+

            (random.uniform(a = 0.122, b= 0.256)*5+
            random.uniform(a = 0.195, b= 0.354)*15+
            random.uniform(a = 0.106, b= 0.225)*25+
            random.uniform(a = 0.248, b= 0.484)*25)*0.86872+

            (random.uniform(a = 0.15, b= 0.37)*2.5+
            random.uniform(a = 0.12, b= 0.23)*5+
            random.uniform(a = 0.24, b= 0.46)*10+
            random.uniform(a = 0.16, b= 0.39)*20)*0)/
            (0.12757 + 0.86872 + 0))

    radiusRecA = statistics.median(radiusRecA_random)
    radiusRecB = statistics.median(radiusRecB_random)
    radiusBurA = statistics.median(radiusBurA_random)
    radiusBurB = statistics.median(radiusBurB_random)

    shellthickRec = radiusRecB-radiusRecA
    shellthickBur = radiusBurB-radiusBurA

    adjustC = caocontent*convertconcrete*clinker
    adjustM = caocontent*convertmortar*clinker

    waste_rate = 0.015
    CONpercentage = 0.793
    CKD_rate = 0.06
    CKD_lanfill = 0.2
    caocontent_CKD = 0.44*(1-Chem_alk_reduction)
    
    cem_app_individual = Cement_demand

    uptake_wasteConcrete = cem_app_individual * CONpercentage * waste_rate * (1-waste_saving) * adjustC
    uptake_wasteMortar = cem_app_individual * (1-CONpercentage) * waste_rate * (1-waste_saving) * adjustM

    uptake_wasteConcrete_Matrix = np.zeros((year_len,year_len))
    uptake_wasteMortar_Matrix = np.zeros((year_len,year_len))

    for k in range(0,year_len):
        for n in range(0,year_len-k):
            if n <= 4:
                uptake_wasteConcrete_Matrix[k,n+k] = uptake_wasteConcrete[k]/5
            if n <= 0:
                uptake_wasteMortar_Matrix[k,n+k] = uptake_wasteMortar[k]
                
    uptake_wasteConcrete = pd.DataFrame(uptake_wasteConcrete_Matrix).sum()
    uptake_wasteMortar = pd.DataFrame(uptake_wasteMortar_Matrix).sum()
    uptake_CKD = cem_app_individual*clinker*CKD_rate*CKD_lanfill*caocontent_CKD*0.784808140177683
    
    
    uptake_mortar_Ren_use_Matrix = np.zeros((year_len,year_len))
    uptake_mortar_Mas_use_Matrix = np.zeros((year_len,year_len))
    uptake_mortar_Mai_use_Matrix = np.zeros((year_len,year_len))

    uptake_concrete_C15_use_Matrix = np.zeros((year_len,year_len))
    uptake_concrete_C16_use_Matrix = np.zeros((year_len,year_len))
    uptake_concrete_C23_use_Matrix = np.zeros((year_len,year_len))
    uptake_concrete_C35_use_Matrix = np.zeros((year_len,year_len))

    uptake_mortar_demolish_Matrix = np.zeros((year_len,year_len))
    uptake_concrete_demolish_Matrix = np.zeros((year_len,year_len))

    for k in range(0,year_len):
        print("k="); print(k)
        
        Life_k = Life[k]
        Std_k = Std[k]

        uptake_concrete_C15_Rec_Matrix = np.zeros((year_len,year_len))
        uptake_concrete_C16_Rec_Matrix = np.zeros((year_len,year_len))
        uptake_concrete_C23_Rec_Matrix = np.zeros((year_len,year_len))
        uptake_concrete_C35_Rec_Matrix = np.zeros((year_len,year_len))

        uptake_concrete_C15_Bur_Matrix = np.zeros((year_len,year_len))
        uptake_concrete_C16_Bur_Matrix = np.zeros((year_len,year_len))
        uptake_concrete_C23_Bur_Matrix = np.zeros((year_len,year_len))
        uptake_concrete_C35_Bur_Matrix = np.zeros((year_len,year_len))

        uptake_mortar_Ren_Rec_Matrix = np.zeros((year_len,year_len))
        uptake_mortar_Mas_Rec_Matrix = np.zeros((year_len,year_len))
        uptake_mortar_Mai_Rec_Matrix = np.zeros((year_len,year_len))

        uptake_mortar_Ren_Bur_Matrix = np.zeros((year_len,year_len))
        uptake_mortar_Mas_Bur_Matrix = np.zeros((year_len,year_len))
        uptake_mortar_Mai_Bur_Matrix = np.zeros((year_len,year_len))

        reuse_rate_k = reuse_rate[k]
        burRate_k=burRate[k]

        if k >= index_year2020 or scenario_index == 'Base':
            st = 0
        else:
            st = index_year2020-k
        for n in range(st,year_len-k):
            CO2Ren = (np.sqrt(n+1)-np.sqrt(n)) * coefMortar[k]/RENthick * adjustM[k]
            CO2Mas = (np.sqrt(n+1)-np.sqrt(n)) * coefMortar[k]/MASthick * adjustM[k]
            CO2Mai = (np.sqrt(n+1)-np.sqrt(n)) * coefMortar[k]/MAIthick * adjustM[k]
            depth1Ren = np.sqrt(n)  *coefMortar[k]; depth1Mas = np.sqrt(n)  *coefMortar[k]; depth1Mai = np.sqrt(n)  *coefMortar[k]
            depth2Ren = np.sqrt(n+1)*coefMortar[k]; depth2Mas = np.sqrt(n+1)*coefMortar[k]; depth2Mai = np.sqrt(n+1)*coefMortar[k]

            if depth1Ren >= RENthick:
                CO2Ren = 0
            if depth1Mas >= MASthick:
                CO2Mas = 0
            if depth1Mai >= MAIthick:
                CO2Mai = 0

            if depth1Ren <= RENthick and depth2Ren >= RENthick:
                CO2Ren = (1-depth1Ren/RENthick) * adjustM[k]
            if depth1Mas <= MASthick and depth2Mas >= MASthick:
                CO2Mas = (1-depth1Mas/MASthick) * adjustM[k]
            if depth1Mai <= MAIthick and depth2Mai >= MAIthick:
                CO2Mai = (1-depth1Mai/MAIthick) * adjustM[k]
                

            reuse_fraction = (norm.cdf(n,Life_k,Std_k) - norm.cdf(n-1,Life_k,Std_k))*reuse_rate_k
            hiber_fraction = (norm.cdf(n,Life_k,Std_k) - norm.cdf(n-1,Life_k,Std_k))*(burRate_k*0.7)
            remain_fraction = reuse_fraction + hiber_fraction
                
            uptake_mortar_Ren_use_Matrix[k,n+k] = cem_app_individual[k]*RENpercentage*(1-norm.cdf(n,Life_k,Std_k))*(1+remain_fraction)*CO2Ren
            uptake_mortar_Mas_use_Matrix[k,n+k] = cem_app_individual[k]*MASpercentage*(1-norm.cdf(n,Life_k,Std_k))*(1+remain_fraction)*CO2Mas
            uptake_mortar_Mai_use_Matrix[k,n+k] = cem_app_individual[k]*MAIpercentage*(1-norm.cdf(n,Life_k,Std_k))*(1+remain_fraction)*CO2Mai

            CO2C15 = (np.sqrt(n+1)-np.sqrt(n)) * coefC15[k]/wallthick*adjustC[k]
            CO2C16 = (np.sqrt(n+1)-np.sqrt(n)) * coefC16[k]/wallthick*adjustC[k]
            CO2C23 = (np.sqrt(n+1)-np.sqrt(n)) * coefC23[k]/wallthick*adjustC[k]
            CO2C35 = (np.sqrt(n+1)-np.sqrt(n)) * coefC35[k]/wallthick*adjustC[k]
            depth1C15 = np.sqrt(n)  *coefC15[k]; depth1C16 = np.sqrt(n)  *coefC16[k]
            depth1C23 = np.sqrt(n)  *coefC23[k]; depth1C35 = np.sqrt(n)  *coefC35[k]
            depth2C15 = np.sqrt(n+1)*coefC15[k]; depth2C16 = np.sqrt(n+1)*coefC16[k]
            depth2C23 = np.sqrt(n+1)*coefC23[k]; depth2C35 = np.sqrt(n+1)*coefC35[k]

            if depth1C15 >= wallthick:
                CO2C15 = 0
            if depth1C16 >= wallthick:
                CO2C16 = 0
            if depth1C23 >= wallthick:
                CO2C23 = 0
            if depth1C35 >= wallthick:
                CO2C35 = 0

            if depth1C15 < wallthick and depth2C15 >= wallthick:
                CO2C15 = (1-depth1C15/wallthick) * adjustC[k]
            if depth1C16 < wallthick and depth2C16 >= wallthick:
                CO2C16 = (1-depth1C16/wallthick) * adjustC[k]
            if depth1C23 < wallthick and depth2C23 >= wallthick:
                CO2C23 = (1-depth1C23/wallthick) * adjustC[k]
            if depth1C35 < wallthick and depth2C35 >= wallthick:
                CO2C35 = (1-depth1C35/wallthick) * adjustC[k]

            uptake_concrete_C15_use_Matrix[k,k+n] = cem_app_individual[k]*C15percentage*(1-norm.cdf(n,Life_k,Std_k))*(1+remain_fraction)*CO2C15
            uptake_concrete_C16_use_Matrix[k,k+n] = cem_app_individual[k]*C16percentage*(1-norm.cdf(n,Life_k,Std_k))*(1+remain_fraction)*CO2C16
            uptake_concrete_C23_use_Matrix[k,k+n] = cem_app_individual[k]*C23percentage*(1-norm.cdf(n,Life_k,Std_k))*(1+remain_fraction)*CO2C23
            uptake_concrete_C35_use_Matrix[k,k+n] = cem_app_individual[k]*C35percentage*(1-norm.cdf(n,Life_k,Std_k))*(1+remain_fraction)*CO2C35

            demolish_rate = norm.cdf(n,Life_k,Std_k) - norm.cdf(n-1,Life_k,Std_k) - remain_fraction
            
            for t in range(0,year_len-k-n):
                if t == 0:
                    depth1RenRec = np.sqrt(n)*coefMortar[k]/RENthick*shellthickRec
                    depth1MasRec = np.sqrt(n)*coefMortar[k]/MASthick*shellthickRec
                    depth1MaiRec = np.sqrt(n)*coefMortar[k]/MAIthick*shellthickRec
                    
                    depth1RenBur = np.sqrt(n)*coefMortar[k]/RENthick*shellthickBur
                    depth1MasBur = np.sqrt(n)*coefMortar[k]/MASthick*shellthickBur
                    depth1MaiBur = np.sqrt(n)*coefMortar[k]/MAIthick*shellthickBur

                    depth1C15Rec = np.sqrt(n)*coefC15[k]/wallthick*shellthickRec
                    depth1C16Rec = np.sqrt(n)*coefC16[k]/wallthick*shellthickRec
                    depth1C23Rec = np.sqrt(n)*coefC23[k]/wallthick*shellthickRec
                    depth1C35Rec = np.sqrt(n)*coefC35[k]/wallthick*shellthickRec
        
                    depth1C15Bur = np.sqrt(n)*coefC15[k]/wallthick*shellthickBur
                    depth1C16Bur = np.sqrt(n)*coefC16[k]/wallthick*shellthickBur
                    depth1C23Bur = np.sqrt(n)*coefC23[k]/wallthick*shellthickBur
                    depth1C35Bur = np.sqrt(n)*coefC35[k]/wallthick*shellthickBur
                else:
                    depth1RenRec = np.sqrt(n)*coefMortar[k]/RENthick*shellthickRec+(np.sqrt(n+t-1)-np.sqrt(n))*coefMortar[k]
                    depth1MasRec = np.sqrt(n)*coefMortar[k]/MASthick*shellthickRec+(np.sqrt(n+t-1)-np.sqrt(n))*coefMortar[k]
                    depth1MaiRec = np.sqrt(n)*coefMortar[k]/MAIthick*shellthickRec+(np.sqrt(n+t-1)-np.sqrt(n))*coefMortar[k]
                    
                    depth1RenBur = np.sqrt(n)*coefMortar[k]/RENthick*shellthickBur+(np.sqrt(n+store_t[k])-np.sqrt(n))*coefMortar[k]+\
                    (np.sqrt(n+t)-np.sqrt(n+store_t[k]))*coefMortar[k]
                    depth1MasBur = np.sqrt(n)*coefMortar[k]/MASthick*shellthickBur+(np.sqrt(n+store_t[k])-np.sqrt(n))*coefMortar[k]+\
                    (np.sqrt(n+t)-np.sqrt(n+store_t[k]))*coefMortar[k]
                    depth1MaiBur = np.sqrt(n)*coefMortar[k]/MAIthick*shellthickBur+(np.sqrt(n+store_t[k])-np.sqrt(n))*coefMortar[k]+\
                    (np.sqrt(n+t)-np.sqrt(n+store_t[k]))*coefMortar[k]
                    
                    depth1C15Rec = np.sqrt(n)*coefC15[k]/wallthick*shellthickRec+(np.sqrt(n+t-1)-np.sqrt(n))*coefC15[k]
                    depth1C16Rec = np.sqrt(n)*coefC16[k]/wallthick*shellthickRec+(np.sqrt(n+t-1)-np.sqrt(n))*coefC16[k]
                    depth1C23Rec = np.sqrt(n)*coefC23[k]/wallthick*shellthickRec+(np.sqrt(n+t-1)-np.sqrt(n))*coefC23[k]
                    depth1C35Rec = np.sqrt(n)*coefC35[k]/wallthick*shellthickRec+(np.sqrt(n+t-1)-np.sqrt(n))*coefC35[k]
                    
                    depth1C15Bur = np.sqrt(n)*coefC15[k]/wallthick*shellthickBur+(np.sqrt(n+store_t[k])-np.sqrt(n))*coefC15[k]+\
                    (np.sqrt(n+t)-np.sqrt(n+store_t[k]))*coefC15B[k]
                    depth1C16Bur = np.sqrt(n)*coefC16[k]/wallthick*shellthickBur+(np.sqrt(n+store_t[k])-np.sqrt(n))*coefC16[k]+\
                    (np.sqrt(n+t)-np.sqrt(n+store_t[k]))*coefC16B[k]
                    depth1C23Bur = np.sqrt(n)*coefC23[k]/wallthick*shellthickBur+(np.sqrt(n+store_t[k])-np.sqrt(n))*coefC23[k]+\
                    (np.sqrt(n+t)-np.sqrt(n+store_t[k]))*coefC23B[k]
                    depth1C35Bur = np.sqrt(n)*coefC35[k]/wallthick*shellthickBur+(np.sqrt(n+store_t[k])-np.sqrt(n))*coefC35[k]+\
                    (np.sqrt(n+t)-np.sqrt(n+store_t[k]))*coefC35B[k] 

                depth2RenRec = np.sqrt(n)*coefMortar[k]/RENthick*shellthickRec+(np.sqrt(n+t+1)-np.sqrt(n))*coefMortar[k]
                depth2MasRec = np.sqrt(n)*coefMortar[k]/MASthick*shellthickRec+(np.sqrt(n+t+1)-np.sqrt(n))*coefMortar[k]
                depth2MaiRec = np.sqrt(n)*coefMortar[k]/MAIthick*shellthickRec+(np.sqrt(n+t+1)-np.sqrt(n))*coefMortar[k]

                depth2RenBur = np.sqrt(n)*coefMortar[k]/RENthick*shellthickBur+(np.sqrt(n+store_t[k])-np.sqrt(n))*coefMortar[k]+\
                (np.sqrt(n+t+1)-np.sqrt(n+store_t[k]))*coefMortar[k]
                depth2MasBur = np.sqrt(n)*coefMortar[k]/MASthick*shellthickBur+(np.sqrt(n+store_t[k])-np.sqrt(n))*coefMortar[k]+\
                (np.sqrt(n+t+1)-np.sqrt(n+store_t[k]))*coefMortar[k]
                depth2MaiBur = np.sqrt(n)*coefMortar[k]/MAIthick*shellthickBur+(np.sqrt(n+store_t[k])-np.sqrt(n))*coefMortar[k]+\
                (np.sqrt(n+t+1)-np.sqrt(n+store_t[k]))*coefMortar[k]

                depth2C15Rec = np.sqrt(n)*coefC15[k]/wallthick*shellthickRec+(np.sqrt(n+t+1)-np.sqrt(n))*coefC15[k]
                depth2C16Rec = np.sqrt(n)*coefC16[k]/wallthick*shellthickRec+(np.sqrt(n+t+1)-np.sqrt(n))*coefC16[k]
                depth2C23Rec = np.sqrt(n)*coefC23[k]/wallthick*shellthickRec+(np.sqrt(n+t+1)-np.sqrt(n))*coefC23[k]
                depth2C35Rec = np.sqrt(n)*coefC35[k]/wallthick*shellthickRec+(np.sqrt(n+t+1)-np.sqrt(n))*coefC35[k]

                depth2C15Bur = np.sqrt(n)*coefC15[k]/wallthick*shellthickBur+(np.sqrt(n+store_t[k])-np.sqrt(n))*coefC15[k]+\
                    (np.sqrt(n+t+1)-np.sqrt(n+store_t[k]))*coefC15B[k]
                depth2C16Bur = np.sqrt(n)*coefC16[k]/wallthick*shellthickBur+(np.sqrt(n+store_t[k])-np.sqrt(n))*coefC16[k]+\
                    (np.sqrt(n+t+1)-np.sqrt(n+store_t[k]))*coefC16B[k]
                depth2C23Bur = np.sqrt(n)*coefC23[k]/wallthick*shellthickBur+(np.sqrt(n+store_t[k])-np.sqrt(n))*coefC23[k]+\
                    (np.sqrt(n+t+1)-np.sqrt(n+store_t[k]))*coefC23B[k]
                depth2C35Bur = np.sqrt(n)*coefC35[k]/wallthick*shellthickBur+(np.sqrt(n+store_t[k])-np.sqrt(n))*coefC35[k]+\
                    (np.sqrt(n+t+1)-np.sqrt(n+store_t[k]))*coefC35B[k]

                CO2RenRec = ((radiusRecB-depth1RenRec)**3-(radiusRecB-depth2RenRec)**3)/(radiusRecB**3-radiusRecA**3)*adjustM[k]
                CO2MasRec = ((radiusRecB-depth1MasRec)**3-(radiusRecB-depth2MasRec)**3)/(radiusRecB**3-radiusRecA**3)*adjustM[k]
                CO2MaiRec = ((radiusRecB-depth1MaiRec)**3-(radiusRecB-depth2MaiRec)**3)/(radiusRecB**3-radiusRecA**3)*adjustM[k]
                CO2RenBur = ((radiusBurB-depth1RenBur)**3-(radiusBurB-depth2RenBur)**3)/(radiusBurB**3-radiusBurA**3)*adjustM[k]
                CO2MasBur = ((radiusBurB-depth1MasBur)**3-(radiusBurB-depth2MasBur)**3)/(radiusBurB**3-radiusBurA**3)*adjustM[k]
                CO2MaiBur = ((radiusBurB-depth1MaiBur)**3-(radiusBurB-depth2MaiBur)**3)/(radiusBurB**3-radiusBurA**3)*adjustM[k]

                CO2C15Rec = ((radiusRecB-depth1C15Rec)**3-(radiusRecB-depth2C15Rec)**3)/(radiusRecB**3-radiusRecA**3)*adjustC[k]
                CO2C16Rec = ((radiusRecB-depth1C16Rec)**3-(radiusRecB-depth2C16Rec)**3)/(radiusRecB**3-radiusRecA**3)*adjustC[k]
                CO2C23Rec = ((radiusRecB-depth1C23Rec)**3-(radiusRecB-depth2C23Rec)**3)/(radiusRecB**3-radiusRecA**3)*adjustC[k]
                CO2C35Rec = ((radiusRecB-depth1C35Rec)**3-(radiusRecB-depth2C35Rec)**3)/(radiusRecB**3-radiusRecA**3)*adjustC[k]
                CO2C15Bur = ((radiusBurB-depth1C15Bur)**3-(radiusBurB-depth2C15Bur)**3)/(radiusBurB**3-radiusBurA**3)*adjustC[k]
                CO2C16Bur = ((radiusBurB-depth1C16Bur)**3-(radiusBurB-depth2C16Bur)**3)/(radiusBurB**3-radiusBurA**3)*adjustC[k]
                CO2C23Bur = ((radiusBurB-depth1C23Bur)**3-(radiusBurB-depth2C23Bur)**3)/(radiusBurB**3-radiusBurA**3)*adjustC[k]
                CO2C35Bur = ((radiusBurB-depth1C35Bur)**3-(radiusBurB-depth2C35Bur)**3)/(radiusBurB**3-radiusBurA**3)*adjustC[k]

                if depth1RenRec >= shellthickRec:
                    CO2RenRec = 0
                if depth1MasRec >= shellthickRec:
                    CO2MasRec = 0
                if depth1MaiRec >= shellthickRec:
                    CO2MaiRec = 0
                if depth1RenBur >= shellthickBur:
                    CO2RenBur = 0
                if depth1MasBur >= shellthickBur:
                    CO2MasBur = 0
                if depth1MaiBur >= shellthickBur:
                    CO2MaiBur = 0
                
                if depth1RenRec < shellthickRec and depth2RenRec >= shellthickRec:
                    CO2RenRec = ((radiusRecB-depth1RenRec)**3-radiusRecA**3)/(radiusRecB**3-radiusRecA**3)*adjustM[k]
                if depth1MasRec < shellthickRec and depth2MasRec >= shellthickRec:
                    CO2MasRec = ((radiusRecB-depth1MasRec)**3-radiusRecA**3)/(radiusRecB**3-radiusRecA**3)*adjustM[k]
                if depth1MaiRec < shellthickRec and depth2MaiRec >= shellthickRec:
                    CO2MaiRec = ((radiusRecB-depth1MaiRec)**3-radiusRecA**3)/(radiusRecB**3-radiusRecA**3)*adjustM[k]
                if depth1RenBur < shellthickBur and depth2RenBur >= shellthickBur:
                    CO2RenBur = ((radiusBurB-depth1RenBur)**3-radiusBurA**3)/(radiusBurB**3-radiusBurA**3)*adjustM[k]
                if depth1MasBur < shellthickBur and depth2MasBur >= shellthickBur:
                    CO2MasBur = ((radiusBurB-depth1MasBur)**3-radiusBurA**3)/(radiusBurB**3-radiusBurA**3)*adjustM[k]
                if depth1MaiBur < shellthickBur and depth2MaiBur >= shellthickBur:
                    CO2MaiBur = ((radiusBurB-depth1MaiBur)**3-radiusBurA**3)/(radiusBurB**3-radiusBurA**3)*adjustM[k]

                if depth1C15Rec >= shellthickRec:
                    CO2C15Rec = 0
                if depth1C16Rec >= shellthickRec:
                    CO2C16Rec = 0
                if depth1C23Rec >= shellthickRec:
                    CO2C23Rec = 0
                if depth1C35Rec >= shellthickRec:
                    CO2C35Rec = 0
                if depth1C15Bur >= shellthickBur:
                    CO2C15Bur = 0
                if depth1C16Bur >= shellthickBur:
                    CO2C16Bur = 0
                if depth1C23Bur >= shellthickBur:
                    CO2C23Bur = 0
                if depth1C35Bur >= shellthickBur:
                    CO2C35Bur = 0

                if depth1C15Rec < shellthickRec and depth2C15Rec >= shellthickRec:
                    CO2C15Rec = ((radiusRecB-depth1C15Rec)**3-radiusRecA**3)/(radiusRecB**3-radiusRecA**3)*adjustC[k]
                if depth1C16Rec < shellthickRec and depth2C16Rec >= shellthickRec:
                    CO2C16Rec = ((radiusRecB-depth1C16Rec)**3-radiusRecA**3)/(radiusRecB**3-radiusRecA**3)*adjustC[k]
                if depth1C23Rec < shellthickRec and depth2C23Rec >= shellthickRec:
                    CO2C23Rec = ((radiusRecB-depth1C23Rec)**3-radiusRecA**3)/(radiusRecB**3-radiusRecA**3)*adjustC[k]
                if depth1C35Rec < shellthickRec and depth2C35Rec >= shellthickRec:
                    CO2C35Rec = ((radiusRecB-depth1C35Rec)**3-radiusRecA**3)/(radiusRecB**3-radiusRecA**3)*adjustC[k]
                if depth1C15Bur < shellthickBur and depth2C15Bur >= shellthickBur:
                    CO2C15Bur = ((radiusBurB-depth1C15Bur)**3-radiusBurA**3)/(radiusBurB**3-radiusBurA**3)*adjustC[k]
                if depth1C16Bur < shellthickBur and depth2C16Bur >= shellthickBur:
                    CO2C16Bur = ((radiusBurB-depth1C16Bur)**3-radiusBurA**3)/(radiusBurB**3-radiusBurA**3)*adjustC[k]
                if depth1C23Bur < shellthickBur and depth2C23Bur >= shellthickBur:
                    CO2C23Bur = ((radiusBurB-depth1C23Bur)**3-radiusBurA**3)/(radiusBurB**3-radiusBurA**3)*adjustC[k]
                if depth1C35Bur < shellthickBur and depth2C35Bur >= shellthickBur:
                    CO2C35Bur = ((radiusBurB-depth1C35Bur)**3-radiusBurA**3)/(radiusBurB**3-radiusBurA**3)*adjustC[k]
                
                
                uptake_mortar_Ren_Rec_Matrix[k+n,k+t+n] = cem_app_individual[k]*RENpercentage*demolish_rate*\
                (recRate[k]/(recRate[k]+burRate[k]))*CO2RenRec
                uptake_mortar_Mas_Rec_Matrix[k+n,k+t+n] = cem_app_individual[k]*MASpercentage*demolish_rate*\
                (recRate[k]/(recRate[k]+burRate[k]))*CO2MasRec
                uptake_mortar_Mai_Rec_Matrix[k+n,k+t+n] = cem_app_individual[k]*MAIpercentage*demolish_rate*\
                (recRate[k]/(recRate[k]+burRate[k]))*CO2MaiRec

                uptake_mortar_Ren_Bur_Matrix[k+n,k+t+n] = cem_app_individual[k]*RENpercentage*demolish_rate*\
                (burRate[k]/(recRate[k]+burRate[k]))*CO2RenBur
                uptake_mortar_Mas_Bur_Matrix[k+n,k+t+n] = cem_app_individual[k]*MASpercentage*demolish_rate*\
                (burRate[k]/(recRate[k]+burRate[k]))*CO2MasBur
                uptake_mortar_Mai_Bur_Matrix[k+n,k+t+n] = cem_app_individual[k]*MAIpercentage*demolish_rate*\
                (burRate[k]/(recRate[k]+burRate[k]))*CO2MaiBur

                uptake_concrete_C15_Rec_Matrix[k+n,k+t+n] = cem_app_individual[k]*C15percentage*demolish_rate*\
                (recRate[k]/(recRate[k]+burRate[k]))*CO2C15Rec
                uptake_concrete_C16_Rec_Matrix[k+n,k+t+n] = cem_app_individual[k]*C16percentage*demolish_rate*\
                (recRate[k]/(recRate[k]+burRate[k]))*CO2C16Rec
                uptake_concrete_C23_Rec_Matrix[k+n,k+t+n] = cem_app_individual[k]*C23percentage*demolish_rate*\
                (recRate[k]/(recRate[k]+burRate[k]))*CO2C23Rec
                uptake_concrete_C35_Rec_Matrix[k+n,k+t+n] = cem_app_individual[k]*C35percentage*demolish_rate*\
                (recRate[k]/(recRate[k]+burRate[k]))*CO2C35Rec
               
                uptake_concrete_C15_Bur_Matrix[k+n,k+t+n] = cem_app_individual[k]*C15percentage*demolish_rate*\
                (burRate[k]/(recRate[k]+burRate[k]))*CO2C15Bur
                uptake_concrete_C16_Bur_Matrix[k+n,k+t+n] = cem_app_individual[k]*C16percentage*demolish_rate*\
                (burRate[k]/(recRate[k]+burRate[k]))*CO2C16Bur
                uptake_concrete_C23_Bur_Matrix[k+n,k+t+n] = cem_app_individual[k]*C23percentage*demolish_rate*\
                (burRate[k]/(recRate[k]+burRate[k]))*CO2C23Bur
                uptake_concrete_C35_Bur_Matrix[k+n,k+t+n] = cem_app_individual[k]*C35percentage*demolish_rate*\
                (burRate[k]/(recRate[k]+burRate[k]))*CO2C35Bur

        uptake_concrete_demolish_Matrix[k,:] =\
            pd.Series(np.sum(
                uptake_concrete_C15_Rec_Matrix + uptake_concrete_C16_Rec_Matrix +\
                    uptake_concrete_C23_Rec_Matrix + uptake_concrete_C35_Rec_Matrix +\
                    uptake_concrete_C15_Bur_Matrix + uptake_concrete_C16_Bur_Matrix +\
                    uptake_concrete_C23_Bur_Matrix + uptake_concrete_C35_Bur_Matrix,
                    axis = 0)
                    )
        
        uptake_mortar_demolish_Matrix[k,:] =\
        pd.Series(np.sum(uptake_mortar_Ren_Rec_Matrix + uptake_mortar_Mas_Rec_Matrix + uptake_mortar_Mai_Rec_Matrix +\
                         uptake_mortar_Ren_Bur_Matrix + uptake_mortar_Mas_Bur_Matrix + uptake_mortar_Mai_Bur_Matrix,axis = 0))

        
    uptake_concrete_demolish = pd.DataFrame(uptake_concrete_demolish_Matrix).sum()
    uptake_mortar_demolish   = pd.DataFrame(uptake_mortar_demolish_Matrix).sum()
    
    uptake_concrete_use_Matrix = (uptake_concrete_C15_use_Matrix + uptake_concrete_C16_use_Matrix + 
                                  uptake_concrete_C23_use_Matrix + uptake_concrete_C35_use_Matrix)
    uptake_mortar_use_Matrix   = (uptake_mortar_Ren_use_Matrix + uptake_mortar_Mas_use_Matrix + uptake_mortar_Mai_use_Matrix)  
    
    uptake_concrete_use = pd.DataFrame(uptake_concrete_use_Matrix).sum(axis=0)
    uptake_mortar_use   = pd.DataFrame(uptake_mortar_use_Matrix).sum(axis=0)
    
    uptake_total = (uptake_CKD + uptake_wasteConcrete + uptake_wasteMortar
                           + uptake_concrete_use + uptake_mortar_use
                           + uptake_concrete_demolish + uptake_mortar_demolish)
    
    uptake_list = pd.concat([uptake_CKD, uptake_wasteConcrete, 
                             uptake_wasteMortar, uptake_concrete_use, 
                             uptake_mortar_use, uptake_concrete_demolish, 
                             uptake_mortar_demolish],axis = 1, ignore_index = True)
    uptake_list.columns = ['CKD', 'Waste concrete','Waste mortar', 'In-use concrete','In-use mortar', 'EoL concrete','EoL mortar']
    
    #export data
    pd.DataFrame(uptake_total).to_excel(filepath + '/uptake_total_' + str(scenario_index) + '.xlsx')
    pd.DataFrame(uptake_list).to_excel(filepath + '/uptake_list_' + str(scenario_index) + '.xlsx')