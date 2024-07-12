import pandas as pd
import numpy as np
from scipy.stats import norm
import random
import statistics
import pathlib
import matplotlib.pyplot as plt

# Import data
scenario_base_inputs = pd.read_excel (io = r'Data_inputs.xlsx', 
header = None, sheet_name="Baseline", usecols= "B:IY", nrows = 101, skiprows = 4)

scenario_strategy_inputs = pd.read_excel (io = r'Data_inputs.xlsx', 
header = None, sheet_name="Strategy", usecols= "B:IY", nrows = 101, skiprows = 4)

scenario_strategy_inputs.iloc[90:101]

# Define strategy options
lever_list = {
     'BASE': [],
     'ELE': [136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159], # Electricity decarbonization
     'EEI': [110,135], # Thermal and electrical energy efficiency improvements
     'FUE': [111,112,113,114,115], # Low-carbon fuel utilization
     'CLI': [121,122,123,124,125,126,127], # Clinker-to-cement ratio reductions
     'TRA': [226,228,230,231,233], # Low-carbon transportation
     'CHE': [160,161,162,163,164,165], # Lower-carbon cement chemistries
     'CCUcur': [185], # Concrete curing with CO2
     'CCUmin': [189,193,196,199,203], # Mineralization to aggregates
     'ME': [108,205], # Material-efficienct design
     'FYI': [221], # Fabrication yield improvement
     'MIU': [22,23,24,25,26,27,28,29,30,31,32], # More intensive use
     'LTE': [45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65], # Lifetime extension
     'REU': [223], # Component reuse
     'REC': [224], # Downcycling
     'SPR': [236], # Demolition waste stockpiling
    }

# Run the model
lever_list_story = {
    'BASE':lever_list['BASE'],
    'ELE': lever_list['BASE']+lever_list['ELE'],
    'EEI': lever_list['BASE']+lever_list['ELE']+lever_list['EEI'],
    'FUE': lever_list['BASE']+lever_list['ELE']+lever_list['EEI']+lever_list['FUE'],
    'CLI': lever_list['BASE']+lever_list['ELE']+lever_list['EEI']+lever_list['FUE']+lever_list['CLI'],
    'TRA': lever_list['BASE']+lever_list['ELE']+lever_list['EEI']+lever_list['FUE']+lever_list['CLI']+lever_list['TRA'],
    'CHE': lever_list['BASE']+lever_list['ELE']+lever_list['EEI']+lever_list['FUE']+lever_list['CLI']+lever_list['TRA']\
    +lever_list['CHE'],
    'CCUcur': lever_list['BASE']+lever_list['ELE']+lever_list['EEI']+lever_list['FUE']+lever_list['CLI']+lever_list['TRA']\
    +lever_list['CHE']+lever_list['CCUcur'],
    'CCUmin': lever_list['BASE']+lever_list['ELE']+lever_list['EEI']+lever_list['FUE']+lever_list['CLI']+lever_list['TRA']\
    +lever_list['CHE']+lever_list['CCUcur']+lever_list['CCUmin'],
    'ME': lever_list['BASE']+lever_list['ELE']+lever_list['EEI']+lever_list['FUE']+lever_list['CLI']+lever_list['TRA']\
    +lever_list['CHE']+lever_list['CCUcur']+lever_list['CCUmin']+lever_list['ME'],
    'FYI': lever_list['BASE']+lever_list['ELE']+lever_list['EEI']+lever_list['FUE']+lever_list['CLI']+lever_list['TRA']\
    +lever_list['CHE']+lever_list['CCUcur']+lever_list['CCUmin']+lever_list['ME']+lever_list['FYI'],
    'MIU': lever_list['BASE']+lever_list['ELE']+lever_list['EEI']+lever_list['FUE']+lever_list['CLI']+lever_list['TRA']\
    +lever_list['CHE']+lever_list['CCUcur']+lever_list['CCUmin']+lever_list['ME']+lever_list['FYI']+lever_list['MIU'],
    'LTE': lever_list['BASE']+lever_list['ELE']+lever_list['EEI']+lever_list['FUE']+lever_list['CLI']+lever_list['TRA']\
    +lever_list['CHE']+lever_list['CCUcur']+lever_list['CCUmin']+lever_list['ME']+lever_list['FYI']+lever_list['MIU']\
    +lever_list['LTE'],
    'SPR': lever_list['BASE']+lever_list['ELE']+lever_list['EEI']+lever_list['FUE']+lever_list['CLI']+lever_list['TRA']\
    +lever_list['CHE']+lever_list['CCUcur']+lever_list['CCUmin']+lever_list['ME']+lever_list['FYI']+lever_list['MIU']\
    +lever_list['LTE']+lever_list['REC']+lever_list['REU']+lever_list['SPR']
        }
data_inputs = scenario_base_inputs.copy()
scenario_inputs = scenario_strategy_inputs.copy()
    
print("levers include " + str(lever_list_story.keys()))

for scenario_index in lever_list_story:
    print(lever_list_story[scenario_index])
    scenarios = lever_list_story[scenario_index]

    if len(scenarios)>0:
        print("Implementing Scenario" + str(scenarios))
        for i in range(0,len(scenarios)):
            data_inputs.iloc[:,scenarios[i]] = scenario_inputs.iloc[:,scenarios[i]]
    else:
        print("Implementing Base scenario")
        
    # building inputs (unit: 10,000 m2)
    new_m2_Res_W = data_inputs.iloc[0:71,0]
    new_m2_Res_SRC = data_inputs.iloc[0:71,1]
    new_m2_Res_RC = data_inputs.iloc[0:71,2]
    new_m2_Res_S = data_inputs.iloc[0:71,3]
    new_m2_Res_CB = data_inputs.iloc[0:71,4]
    new_m2_Res_Other = data_inputs.iloc[0:71,5]
    new_m2_Com_W = data_inputs.iloc[0:71,6]
    new_m2_Com_SRC = data_inputs.iloc[0:71,7]
    new_m2_Com_RC = data_inputs.iloc[0:71,8]
    new_m2_Com_S = data_inputs.iloc[0:71,9]
    new_m2_Com_CB = data_inputs.iloc[0:71,10]
    new_m2_Com_Other = data_inputs.iloc[0:71,11]
    
    #　infrastructure inputs (unit: million JPY)
    new_JPY_road = data_inputs.iloc[0:71,12]
    new_JPY_land = data_inputs.iloc[0:71,13]
    new_JPY_agri = data_inputs.iloc[0:71,14]
    new_JPY_indu = data_inputs.iloc[0:71,15]
    new_JPY_sewe = data_inputs.iloc[0:71,16]
    new_JPY_harb = data_inputs.iloc[0:71,17]
    new_JPY_rail = data_inputs.iloc[0:71,18]
    new_JPY_park = data_inputs.iloc[0:71,19]
    new_JPY_wast = data_inputs.iloc[0:71,20]
    
    # input dataframe
    new_m2_JPY_matrix = pd.concat([new_m2_Res_W, new_m2_Res_SRC, new_m2_Res_RC,\
                                   new_m2_Res_S, new_m2_Res_CB, new_m2_Res_Other,\
                                   new_m2_Com_W, new_m2_Com_SRC, new_m2_Com_RC,\
                                   new_m2_Com_S, new_m2_Com_CB, new_m2_Com_Other,\
                                   new_JPY_road, new_JPY_land, new_JPY_agri,\
                                   new_JPY_indu, new_JPY_sewe, new_JPY_harb,\
                                   new_JPY_rail, new_JPY_park, new_JPY_wast], axis = 1)
    
    # population
    pop = data_inputs.iloc[70:101,21]

    # building stock
    Use_m2_Res = data_inputs.iloc[70:101,22]*pop/10
    Use_m2_Com = data_inputs.iloc[70:101,23]*pop/10
    
    # building stock share
    Share_Res_W = data_inputs.iloc[70:101,33]
    Share_Res_SRC = data_inputs.iloc[70:101,34]
    Share_Res_RC = data_inputs.iloc[70:101,35]
    Share_Res_S = data_inputs.iloc[70:101,36]
    Share_Res_CB = data_inputs.iloc[70:101,37]
    Share_Res_Other = data_inputs.iloc[70:101,38]
    Share_Com_W = data_inputs.iloc[70:101,39]
    Share_Com_SRC = data_inputs.iloc[70:101,40]
    Share_Com_RC = data_inputs.iloc[70:101,41]
    Share_Com_S = data_inputs.iloc[70:101,42]
    Share_Com_CB = data_inputs.iloc[70:101,43]
    Share_Com_Other = data_inputs.iloc[70:101,44]
    
    # building stock
    Use_m2_Res_W = Use_m2_Res*Share_Res_W
    Use_m2_Res_SRC = Use_m2_Res*Share_Res_SRC
    Use_m2_Res_RC = Use_m2_Res*Share_Res_RC
    Use_m2_Res_S = Use_m2_Res*Share_Res_S
    Use_m2_Res_CB = Use_m2_Res*Share_Res_CB
    Use_m2_Res_Other = Use_m2_Res*Share_Res_Other
    Use_m2_Com_W = Use_m2_Com*Share_Com_W
    Use_m2_Com_SRC = Use_m2_Com*Share_Com_SRC
    Use_m2_Com_RC = Use_m2_Com*Share_Com_RC
    Use_m2_Com_S = Use_m2_Com*Share_Com_S
    Use_m2_Com_CB = Use_m2_Com*Share_Com_CB
    Use_m2_Com_Other = Use_m2_Com*Share_Com_Other
    
    # infrastructure stock
    Use_JPY_road = data_inputs.iloc[70:101,24]*pop
    Use_JPY_land = data_inputs.iloc[70:101,25]*pop
    Use_JPY_agri = data_inputs.iloc[70:101,26]*pop
    Use_JPY_indu = data_inputs.iloc[70:101,27]*pop
    Use_JPY_sewe = data_inputs.iloc[70:101,28]*pop
    Use_JPY_harb = data_inputs.iloc[70:101,29]*pop
    Use_JPY_rail = data_inputs.iloc[70:101,30]*pop
    Use_JPY_park = data_inputs.iloc[70:101,31]*pop
    Use_JPY_wast = data_inputs.iloc[70:101,32]*pop
    
    # stock dataframe
    Use_m2_JPY_matrix = pd.concat([Use_m2_Res_W, Use_m2_Res_SRC, Use_m2_Res_RC,\
                                   Use_m2_Res_S, Use_m2_Res_CB, Use_m2_Res_Other,\
                                   Use_m2_Com_W, Use_m2_Com_SRC, Use_m2_Com_RC,\
                                   Use_m2_Com_S, Use_m2_Com_CB, Use_m2_Com_Other,\
                                   Use_JPY_road, Use_JPY_land, Use_JPY_agri,\
                                   Use_JPY_indu, Use_JPY_sewe, Use_JPY_harb,\
                                   Use_JPY_rail, Use_JPY_park, Use_JPY_wast], axis = 1)
    
    # lifetime
    Life = data_inputs.iloc[:,45:66]
    Std = data_inputs.iloc[:,66:87]
    
    # concrete intensity
    int_Con_Res_W = data_inputs.iloc[:,87]*10
    int_Con_Res_SRC = data_inputs.iloc[:,88]*10
    int_Con_Res_RC = data_inputs.iloc[:,89]*10
    int_Con_Res_S = data_inputs.iloc[:,90]*10
    int_Con_Res_CB = data_inputs.iloc[:,91]*10
    int_Con_Res_Other = data_inputs.iloc[:,92]*10
    int_Con_Com_W = data_inputs.iloc[:,93]*10
    int_Con_Com_SRC = data_inputs.iloc[:,94]*10
    int_Con_Com_RC = data_inputs.iloc[:,95]*10
    int_Con_Com_S = data_inputs.iloc[:,96]*10
    int_Con_Com_CB = data_inputs.iloc[:,97]*10
    int_Con_Com_Other = data_inputs.iloc[:,98]*10
    int_Con_road = data_inputs.iloc[:,99]
    int_Con_land = data_inputs.iloc[:,100]
    int_Con_agri = data_inputs.iloc[:,101]
    int_Con_indu = data_inputs.iloc[:,102]
    int_Con_sewe = data_inputs.iloc[:,103]
    int_Con_harb = data_inputs.iloc[:,104]
    int_Con_rail = data_inputs.iloc[:,105]
    int_Con_park = data_inputs.iloc[:,106]
    int_Con_wast = data_inputs.iloc[:,107]
    
    # cement content
    cemen_content = data_inputs.iloc[:,108]
    
    # carbonate decomposition
    Pro_Em_factor = data_inputs.iloc[:,109]
    
    # thermal efficiency
    Them_eff = data_inputs.iloc[:,110]

    # fuel share
    Coal_share_cem = data_inputs.iloc[:,111]
    Coke_share_cem  = data_inputs.iloc[:,112]
    Oil_share_cem = data_inputs.iloc[:,113]
    WaFu_share_cem = data_inputs.iloc[:,114]
    NaGa_share_cem = data_inputs.iloc[:,115]

    # emission factor of fuel
    Coal_CO2_cem = data_inputs.iloc[:,116]
    Coke_CO2_cem  = data_inputs.iloc[:,117]
    Oil_CO2_cem = data_inputs.iloc[:,118]
    WaFu_CO2_cem = data_inputs.iloc[:,119]
    NaGa_CO2_cem = data_inputs.iloc[:,120]
    
    # cement ingredients
    clinker = data_inputs.iloc[:,121]
    Gyp_share = data_inputs.iloc[:,122]
    Lim_share = data_inputs.iloc[:,123]
    Poz_share = data_inputs.iloc[:,124]
    Sla_share = data_inputs.iloc[:,125]
    Fly_share = data_inputs.iloc[:,126]
    Cal_share = data_inputs.iloc[:,127]
    Ene_Cal   = data_inputs.iloc[:,128]
    
    # CCS
    CCS_Oxy_percent = data_inputs.iloc[:,129]
    CCS_Pos_percent = data_inputs.iloc[:,130]
    Eff_Oxy = data_inputs.iloc[:,131]
    Eff_Pos = data_inputs.iloc[:,132]
    Ene_Oxy = data_inputs.iloc[:,133]
    Ene_Pos = data_inputs.iloc[:,134]
    
    # electric efficiency
    Ele_eff = data_inputs.iloc[:,135]
        
    # electricity share
    Coal_share_ele = data_inputs.iloc[:,136]
    Oil_share_ele = data_inputs.iloc[:,137]
    Naga_share_ele = data_inputs.iloc[:,138]
    Hydr_share_ele = data_inputs.iloc[:,139]
    Geot_share_ele = data_inputs.iloc[:,140]
    Sol_share_ele = data_inputs.iloc[:,141]
    Wind_share_ele = data_inputs.iloc[:,142]
    Tide_share_ele = data_inputs.iloc[:,143]
    Nuc_share_ele = data_inputs.iloc[:,144]
    Bio_share_ele = data_inputs.iloc[:,145]
    Was_share_ele = data_inputs.iloc[:,146]
    SoTh_share_ele = data_inputs.iloc[:,147]
    
    # emission factor of electricity
    Coal_CO2_ele = data_inputs.iloc[:,148]
    Oil_CO2_ele = data_inputs.iloc[:,149]
    Naga_CO2_ele = data_inputs.iloc[:,150]
    Hydr_CO2_ele = data_inputs.iloc[:,151]
    Geot_CO2_ele = data_inputs.iloc[:,152]
    Sol_CO2_ele = data_inputs.iloc[:,153]
    Wind_CO2_ele = data_inputs.iloc[:,154]
    Tide_CO2_ele = data_inputs.iloc[:,155]
    Nuc_CO2_ele = data_inputs.iloc[:,156]
    Bio_CO2_ele = data_inputs.iloc[:,157]
    Was_CO2_ele = data_inputs.iloc[:,158]
    SoTh_CO2_ele = data_inputs.iloc[:,159]
    
    # share of low-carbon chemistries
    Belite_share = data_inputs.iloc[:,160]
    BYF_share = data_inputs.iloc[:,161]
    CCSC_share = data_inputs.iloc[:,162]
    CSAB_share = data_inputs.iloc[:,163]
    Celite_share = data_inputs.iloc[:,164]
    MOMS_share = data_inputs.iloc[:,165]

    # process emission savings of low-carbon chemistries
    Belite_pro_save = data_inputs.iloc[:,166]
    BYF_pro_save = data_inputs.iloc[:,167]
    CCSC_pro_save = data_inputs.iloc[:,168]
    CSAB_pro_save = data_inputs.iloc[:,169]
    Celite_pro_save = data_inputs.iloc[:,170]
    MOMS_pro_save = data_inputs.iloc[:,171]
    
    # thermal emission savings of low-carbon chemistries
    Belite_fue_save = data_inputs.iloc[:,172]
    BYF_fue_save = data_inputs.iloc[:,173]
    CCSC_fue_save = data_inputs.iloc[:,174]
    CSAB_fue_save = data_inputs.iloc[:,175]
    Celite_fue_save = data_inputs.iloc[:,176]
    MOMS_fue_save = data_inputs.iloc[:,177]

    # alkali reduction of low-carbon chemistries
    Belite_alk_save = data_inputs.iloc[:,178]
    BYF_alk_save = data_inputs.iloc[:,179]
    CCSC_alk_save = data_inputs.iloc[:,180]
    CSAB_alk_save = data_inputs.iloc[:,181]
    Celite_alk_save = data_inputs.iloc[:,182]
    MOMS_alk_save = data_inputs.iloc[:,183]
    
    # CCSC CO2 credit
    CCSC_CO2_credit = data_inputs.iloc[:,184]

    # CCU curing
    CO2_curing_share = data_inputs.iloc[:,185]
    CO2_curing_coef = data_inputs.iloc[:,186]
    CO2_curing_pen = data_inputs.iloc[:,187]
    CO2_curing_red = data_inputs.iloc[:,188]
    
    CO2_curing_sav = CO2_curing_share*CO2_curing_red
    CO2_curing_emi = CO2_curing_share*CO2_curing_pen

    # CCU mineralization
    CO2_mine_EOL_share = data_inputs.iloc[:,189]
    CO2_mine_EOL_coef = data_inputs.iloc[:,190]
    CO2_mine_EOL_pen = data_inputs.iloc[:,191]
    CO2_mine_EOL_red = data_inputs.iloc[:,192]

    CO2_mine_slag_share = data_inputs.iloc[:,193]
    CO2_mine_slag_upt = data_inputs.iloc[:,194]
    CO2_mine_slag_pen = data_inputs.iloc[:,195]
        
    CO2_mine_ash_share = data_inputs.iloc[:,196]
    CO2_mine_ash_upt = data_inputs.iloc[:,197]
    CO2_mine_ash_pen = data_inputs.iloc[:,198]

    CO2_mine_lime_share = data_inputs.iloc[:,199]
    CO2_mine_lime_upt = data_inputs.iloc[:,200]
    CO2_mine_lime_pen = data_inputs.iloc[:,201]

    CO2_mine_red_share = data_inputs.iloc[:,202]
    CO2_mine_red_upt = data_inputs.iloc[:,203]
    CO2_mine_red_pen = data_inputs.iloc[:,204]  

    CO2_mine_EOL_sav = CO2_mine_EOL_share*CO2_mine_EOL_red
    CO2_mine_EOL_emi = CO2_mine_EOL_share*CO2_mine_EOL_pen
    CO2_mine_slag_sto = CO2_mine_slag_share*CO2_mine_slag_upt
    CO2_mine_slag_emi = CO2_mine_slag_share*CO2_mine_slag_pen
    CO2_mine_ash_sto = CO2_mine_ash_share*CO2_mine_ash_upt
    CO2_mine_ash_emi = CO2_mine_ash_share*CO2_mine_ash_pen
    CO2_mine_lime_sto = CO2_mine_lime_share*CO2_mine_lime_upt
    CO2_mine_lime_emi = CO2_mine_lime_share*CO2_mine_lime_pen
    CO2_mine_red_sto = CO2_mine_red_share*CO2_mine_red_upt
    CO2_mine_red_emi = CO2_mine_red_share*CO2_mine_red_pen
    
    # material-efficient design
    Leaner_rate = data_inputs.iloc[:,205]
    Leaner_con_reduction = data_inputs.iloc[:,206]
    Leaner_con_saving = Leaner_rate*Leaner_con_reduction

    # material substitution
    Mat_sub_rate = data_inputs.iloc[:,207]
    Timber_to_cem_res = data_inputs.iloc[:,208]
    Timber_to_cem_nonr = data_inputs.iloc[:,209]
    CO2_tim_pen = data_inputs.iloc[:,210]
    CO2_tim_sto = data_inputs.iloc[:,211]
    EoL_tim_land = data_inputs.iloc[:,212]
    EoL_tim_inci = data_inputs.iloc[:,213]
    EoL_tim_recy = data_inputs.iloc[:,214]
    Land_tim_deg = data_inputs.iloc[:,215]
    Land_tim_per = data_inputs.iloc[:,216]
    Deg_tim_CO2 = data_inputs.iloc[:,217]
    Deg_tim_CH4 = data_inputs.iloc[:,218]
    CH4_to_CO2 = data_inputs.iloc[:,219]
    CH4_recover = data_inputs.iloc[:,220]
    
    # end-of-life options
    EoL = data_inputs.iloc[:,221:226]
    waste_saving = EoL.iloc[:,0]*EoL.iloc[:,1]
    recRate = EoL.iloc[:,2]
    reuseRate = EoL.iloc[:,3]*EoL.iloc[:,4]
        
    # emission factor
    CO2_tran_cem = data_inputs.iloc[:,226]
    CO2_prod_agg = data_inputs.iloc[:,227]
    CO2_tran_agg = data_inputs.iloc[:,228]
    CO2_prod_rec = data_inputs.iloc[:,229]
    CO2_tran_rec = data_inputs.iloc[:,230]
    CO2_tran_bur = data_inputs.iloc[:,231]
    CO2_mix_con = data_inputs.iloc[:,232]
    CO2_tran_con = data_inputs.iloc[:,233]
    CO2_onsite_con = data_inputs.iloc[:,234]
    
    # waste stockpiling
    Dem_spread_time = data_inputs.iloc[:,235]
    Dem_spread_ratio = data_inputs.iloc[:,236]
    store_t = Dem_spread_time*Dem_spread_ratio+(1-Dem_spread_ratio)*0.2
    
    # concrete outflow
    dem_con_Res_W = data_inputs.iloc[0:71,237]
    dem_con_Res_SRC = data_inputs.iloc[0:71,238]
    dem_con_Res_RC = data_inputs.iloc[0:71,239]
    dem_con_Res_S = data_inputs.iloc[0:71,240]
    dem_con_Res_CB = data_inputs.iloc[0:71,241]
    dem_con_Res_Other = data_inputs.iloc[0:71,242]
    dem_con_Com_W = data_inputs.iloc[0:71,243]
    dem_con_Com_SRC = data_inputs.iloc[0:71,244]
    dem_con_Com_RC = data_inputs.iloc[0:71,245]
    dem_con_Com_S = data_inputs.iloc[0:71,246]
    dem_con_Com_CB = data_inputs.iloc[0:71,247]
    dem_con_Com_Other = data_inputs.iloc[0:71,248]
    dem_con_road = data_inputs.iloc[0:71,249]
    dem_con_land = data_inputs.iloc[0:71,250]
    dem_con_agri = data_inputs.iloc[0:71,251]
    dem_con_indu = data_inputs.iloc[0:71,252]
    dem_con_sewe = data_inputs.iloc[0:71,253]
    dem_con_harb = data_inputs.iloc[0:71,254]
    dem_con_rail = data_inputs.iloc[0:71,255]
    dem_con_park = data_inputs.iloc[0:71,256]
    dem_con_wast = data_inputs.iloc[0:71,257]
    
    # outflow dataframe
    dem_con_matrix = pd.concat([dem_con_Res_W, dem_con_Res_SRC, dem_con_Res_RC,\
                                dem_con_Res_S, dem_con_Res_CB, dem_con_Res_Other,\
                                dem_con_Com_W, dem_con_Com_SRC, dem_con_Com_RC,\
                                dem_con_Com_S, dem_con_Com_CB, dem_con_Com_Other,\
                                dem_con_road, dem_con_land, dem_con_agri,\
                                dem_con_indu, dem_con_sewe, dem_con_harb,\
                                dem_con_rail, dem_con_park, dem_con_wast], axis = 1)
    
    # concrete intensity datarfame
    int_Con_matrix = pd.concat([int_Con_Res_W*(1-Leaner_con_saving)*(1-waste_saving*0.015),\
                                int_Con_Res_SRC*(1-Leaner_con_saving)*(1-Mat_sub_rate)*(1-waste_saving*0.015),\
                                int_Con_Res_RC*(1-Leaner_con_saving)*(1-Mat_sub_rate)*(1-waste_saving*0.015),\
                                int_Con_Res_S*(1-Leaner_con_saving)*(1-Mat_sub_rate)*(1-waste_saving*0.015),\
                                int_Con_Res_CB*(1-Leaner_con_saving)*(1-Mat_sub_rate)*(1-waste_saving*0.015),\
                                int_Con_Res_Other*(1-Leaner_con_saving)*(1-Mat_sub_rate)*(1-waste_saving*0.015),\
                                int_Con_Com_W*(1-Leaner_con_saving)*(1-waste_saving*0.015),\
                                int_Con_Com_SRC*(1-Leaner_con_saving)*(1-Mat_sub_rate)*(1-waste_saving*0.015),\
                                int_Con_Com_RC*(1-Leaner_con_saving)*(1-Mat_sub_rate)*(1-waste_saving*0.015),\
                                int_Con_Com_S*(1-Leaner_con_saving)*(1-Mat_sub_rate)*(1-waste_saving*0.015),\
                                int_Con_Com_CB*(1-Leaner_con_saving)*(1-Mat_sub_rate)*(1-waste_saving*0.015),\
                                int_Con_Com_Other*(1-Leaner_con_saving)*(1-Mat_sub_rate)*(1-waste_saving*0.015),\
                                int_Con_road*(1-Leaner_con_saving)*(1-waste_saving*0.015),\
                                int_Con_land*(1-Leaner_con_saving)*(1-waste_saving*0.015),\
                                int_Con_agri*(1-Leaner_con_saving)*(1-waste_saving*0.015),\
                                int_Con_indu*(1-Leaner_con_saving)*(1-waste_saving*0.015),\
                                int_Con_sewe*(1-Leaner_con_saving)*(1-waste_saving*0.015),\
                                int_Con_harb*(1-Leaner_con_saving)*(1-waste_saving*0.015),\
                                int_Con_rail*(1-Leaner_con_saving)*(1-waste_saving*0.015),\
                                int_Con_park*(1-Leaner_con_saving)*(1-waste_saving*0.015),\
                                int_Con_wast*(1-Leaner_con_saving)*(1-waste_saving*0.015)], axis = 1)
    
    # timber intensity datarfame
    int_Tim_matrix = pd.concat([int_Con_Res_W*(1-Leaner_con_saving)*0,\
                                int_Con_Res_SRC*(1-Leaner_con_saving)*Mat_sub_rate*Timber_to_cem_res,\
                                int_Con_Res_RC*(1-Leaner_con_saving)*Mat_sub_rate*Timber_to_cem_res,\
                                int_Con_Res_S*(1-Leaner_con_saving)*Mat_sub_rate*Timber_to_cem_res,\
                                int_Con_Res_CB*(1-Leaner_con_saving)*Mat_sub_rate*Timber_to_cem_res,\
                                int_Con_Res_Other*(1-Leaner_con_saving)*Mat_sub_rate*Timber_to_cem_res,\
                                int_Con_Com_W*(1-Leaner_con_saving)*0,\
                                int_Con_Com_SRC*(1-Leaner_con_saving)*Mat_sub_rate*Timber_to_cem_res,\
                                int_Con_Com_RC*(1-Leaner_con_saving)*Mat_sub_rate*Timber_to_cem_res,\
                                int_Con_Com_S*(1-Leaner_con_saving)*Mat_sub_rate*Timber_to_cem_res,\
                                int_Con_Com_CB*(1-Leaner_con_saving)*Mat_sub_rate*Timber_to_cem_res,\
                                int_Con_Com_Other*(1-Leaner_con_saving)*Mat_sub_rate*Timber_to_cem_res,\
                                int_Con_road*(1-Leaner_con_saving)*0,\
                                int_Con_land*(1-Leaner_con_saving)*0,\
                                int_Con_agri*(1-Leaner_con_saving)*0,\
                                int_Con_indu*(1-Leaner_con_saving)*0,\
                                int_Con_sewe*(1-Leaner_con_saving)*0,\
                                int_Con_harb*(1-Leaner_con_saving)*0,\
                                int_Con_rail*(1-Leaner_con_saving)*0,\
                                int_Con_park*(1-Leaner_con_saving)*0,\
                                int_Con_wast*(1-Leaner_con_saving)*0],axis = 1)
    
    # cement intensity dataframe
    int_Cem_Res_W = int_Con_Res_W*cemen_content*(1-Leaner_con_saving)*(1-waste_saving*0.015)*(1-CO2_curing_sav-CO2_mine_EOL_sav)
    int_Cem_Res_SRC = int_Con_Res_SRC*cemen_content*(1-Leaner_con_saving)*(1-Mat_sub_rate)*(1-waste_saving*0.015)*(1-CO2_curing_sav-CO2_mine_EOL_sav)
    int_Cem_Res_RC = int_Con_Res_RC*cemen_content*(1-Leaner_con_saving)*(1-Mat_sub_rate)*(1-waste_saving*0.015)*(1-CO2_curing_sav-CO2_mine_EOL_sav)
    int_Cem_Res_S = int_Con_Res_S*cemen_content*(1-Leaner_con_saving)*(1-Mat_sub_rate)*(1-waste_saving*0.015)*(1-CO2_curing_sav-CO2_mine_EOL_sav)
    int_Cem_Res_CB = int_Con_Res_CB*cemen_content*(1-Leaner_con_saving)*(1-Mat_sub_rate)*(1-waste_saving*0.015)*(1-CO2_curing_sav-CO2_mine_EOL_sav)
    int_Cem_Res_Other = int_Con_Res_Other*cemen_content*(1-Leaner_con_saving)*(1-Mat_sub_rate)*(1-waste_saving*0.015)*(1-CO2_curing_sav-CO2_mine_EOL_sav)
    int_Cem_Com_W = int_Con_Com_W*cemen_content*(1-Leaner_con_saving)*(1-waste_saving*0.015)*(1-CO2_curing_sav-CO2_mine_EOL_sav)
    int_Cem_Com_SRC = int_Con_Com_SRC*cemen_content*(1-Leaner_con_saving)*(1-Mat_sub_rate)*(1-waste_saving*0.015)*(1-CO2_curing_sav-CO2_mine_EOL_sav)
    int_Cem_Com_RC = int_Con_Com_RC*cemen_content*(1-Leaner_con_saving)*(1-Mat_sub_rate)*(1-waste_saving*0.015)*(1-CO2_curing_sav-CO2_mine_EOL_sav)
    int_Cem_Com_S = int_Con_Com_S*cemen_content*(1-Leaner_con_saving)*(1-Mat_sub_rate)*(1-waste_saving*0.015)*(1-CO2_curing_sav-CO2_mine_EOL_sav)
    int_Cem_Com_CB = int_Con_Com_CB*cemen_content*(1-Leaner_con_saving)*(1-Mat_sub_rate)*(1-waste_saving*0.015)*(1-CO2_curing_sav-CO2_mine_EOL_sav)
    int_Cem_Com_Other = int_Con_Com_Other*cemen_content*(1-Leaner_con_saving)*(1-Mat_sub_rate)*(1-waste_saving*0.015)*(1-CO2_curing_sav-CO2_mine_EOL_sav)
    int_Cem_road = int_Con_road*cemen_content*(1-Leaner_con_saving)*(1-waste_saving*0.015)*(1-CO2_curing_sav-CO2_mine_EOL_sav)
    int_Cem_land = int_Con_land*cemen_content*(1-Leaner_con_saving)*(1-waste_saving*0.015)*(1-CO2_curing_sav-CO2_mine_EOL_sav)
    int_Cem_agri = int_Con_agri*cemen_content*(1-Leaner_con_saving)*(1-waste_saving*0.015)*(1-CO2_curing_sav-CO2_mine_EOL_sav)
    int_Cem_indu = int_Con_indu*cemen_content*(1-Leaner_con_saving)*(1-waste_saving*0.015)*(1-CO2_curing_sav-CO2_mine_EOL_sav)
    int_Cem_sewe = int_Con_sewe*cemen_content*(1-Leaner_con_saving)*(1-waste_saving*0.015)*(1-CO2_curing_sav-CO2_mine_EOL_sav)
    int_Cem_harb = int_Con_harb*cemen_content*(1-Leaner_con_saving)*(1-waste_saving*0.015)*(1-CO2_curing_sav-CO2_mine_EOL_sav)
    int_Cem_rail = int_Con_rail*cemen_content*(1-Leaner_con_saving)*(1-waste_saving*0.015)*(1-CO2_curing_sav-CO2_mine_EOL_sav)
    int_Cem_park = int_Con_park*cemen_content*(1-Leaner_con_saving)*(1-waste_saving*0.015)*(1-CO2_curing_sav-CO2_mine_EOL_sav)
    int_Cem_wast = int_Con_wast*cemen_content*(1-Leaner_con_saving)*(1-waste_saving*0.015)*(1-CO2_curing_sav-CO2_mine_EOL_sav)
    
    int_Cem_matrix = pd.concat([int_Cem_Res_W, int_Cem_Res_SRC, int_Cem_Res_RC,\
                                int_Cem_Res_S, int_Cem_Res_CB, int_Cem_Res_Other,\
                                int_Cem_Com_W, int_Cem_Com_SRC, int_Cem_Com_RC,\
                                int_Cem_Com_S, int_Cem_Com_CB, int_Cem_Com_Other,\
                                int_Cem_road, int_Cem_land, int_Cem_agri,\
                                int_Cem_indu, int_Cem_sewe, int_Cem_harb,\
                                int_Cem_rail, int_Cem_park, int_Cem_wast], axis = 1)
    
    # lifetime dataframe
    Life_matrix = pd.concat([Life.iloc[:,x] for x in range(0,21)], axis=1)
    sh=Life_matrix.shape
    Life_matrix.columns=range(sh[1])
    
    # standard deviation dataframe
    Std_matrix = pd.concat([Std.iloc[:,x] for x in range(0,21)], axis=1)
    sh=Std_matrix.shape
    Std_matrix.columns=range(sh[1])
    
    # end-of-life datarfame
    Rec_matrix = pd.concat([recRate for x in range(0,21)], axis = 1)
    sh=Rec_matrix.shape
    Rec_matrix.columns=range(sh[1])
    
    numlist=[0]*101
    reuseRate_infra=pd.Series(numlist)
    Reuse_matrix = pd.concat([reuseRate,reuseRate,reuseRate,reuseRate,reuseRate,reuseRate,\
                              reuseRate,reuseRate,reuseRate,reuseRate,reuseRate,reuseRate,\
                              reuseRate_infra,reuseRate_infra,reuseRate_infra,reuseRate_infra,\
                              reuseRate_infra,reuseRate_infra,reuseRate_infra,reuseRate_infra,reuseRate_infra], axis = 1)
    
    ##############################################################################
    #stock-driven model#
    ##############################################################################
    
    new_m2_JPY_extended_matrix = pd.DataFrame()
    con_app_matrix = pd.DataFrame()
    cem_app_matrix = pd.DataFrame()
    tim_con_matrix = pd.DataFrame()
    dem_tim_matrix = pd.DataFrame()
    
    for i in range(0, len(new_m2_JPY_matrix.columns)):
        new_m2_JPY_extended = new_m2_JPY_matrix.iloc[:,i]
        dem_con_extended = dem_con_matrix.iloc[:,i]
        year_complete = np.arange(1950,2021)
        demol_Con_extended = np.repeat(0,len(year_complete))
        demol_Cem_extended = np.repeat(0,len(year_complete))
        demol_Tim_extended = np.repeat(0,len(year_complete))
        reuse_Con_extended = np.repeat(0,len(year_complete))
        reuse_Cem_extended = np.repeat(0,len(year_complete))
        
        for k in range(2021,2051):
            Life_extended = Life_matrix.iloc[0:len(year_complete),i]
            Std_extended = Std_matrix.iloc[0:len(year_complete),i]
            Rec_extended = Rec_matrix.iloc[0:len(year_complete),i]
            Reuse_extended = Reuse_matrix.iloc[0:len(year_complete),i]
            int_Con = int_Con_matrix.iloc[0:len(year_complete),i]
            int_Cem = int_Cem_matrix.iloc[0:len(year_complete),i]
            int_Tim = int_Tim_matrix.iloc[0:len(year_complete),i]
                
            # demolished buildings and infrastructure
            demolish_m2_JPY_list = new_m2_JPY_extended*(norm.cdf(k-year_complete,Life_extended,Std_extended)-\
                                                        norm.cdf(k-1-year_complete,Life_extended,Std_extended))
            demolish_m2_JPY = sum(demolish_m2_JPY_list)

            # demolished concrete
            demolish_Con_list =(new_m2_JPY_extended*int_Con)*(norm.cdf(k-year_complete,Life_extended,Std_extended)-\
                                                              norm.cdf(k-1-year_complete,Life_extended,Std_extended))
            demolish_Con = sum(demolish_Con_list)
            demol_Con_extended= np.append(demol_Con_extended,demolish_Con)
                
            # demolished cement
            demolish_Cem_list =(new_m2_JPY_extended*int_Cem)*(norm.cdf(k-year_complete,Life_extended,Std_extended)-\
                                                              norm.cdf(k-1-year_complete,Life_extended,Std_extended))
            demolish_Cem = sum(demolish_Cem_list)
            demol_Cem_extended= np.append(demol_Cem_extended,demolish_Cem)
                
            # demolished timber
            demolish_Tim_list = (new_m2_JPY_extended*int_Tim)*(norm.cdf(k-year_complete,Life_extended,Std_extended)-\
                                                               norm.cdf(k-1-year_complete,Life_extended,Std_extended))
            demolish_Tim = sum(demolish_Tim_list)
            demol_Tim_extended = np.append(demol_Tim_extended,demolish_Tim)

            # newly constructed buildings and infrastructure
            new_m2_JPY = Use_m2_JPY_matrix.iloc[k-2020,i] - Use_m2_JPY_matrix.iloc[k-2021,i] + demolish_m2_JPY
            if new_m2_JPY < 0:
                new_m2_JPY = 0
            new_m2_JPY_extended = np.append(new_m2_JPY_extended, new_m2_JPY)
            
            # reused component
            reuse_Con_list = demolish_Con_list*Reuse_extended
            reuse_Cem_list = demolish_Cem_list*Reuse_extended
            reuse_Con = sum(reuse_Con_list)
            reuse_Cem = sum(reuse_Cem_list)
            if new_m2_JPY == 0:
                reuse_Con = 0
                reuse_Cem = 0
            reuse_Con_extended= np.append(reuse_Con_extended,reuse_Con)
            reuse_Cem_extended= np.append(reuse_Cem_extended,reuse_Cem)
            
            year_complete = np.append(year_complete,k)
            
        # newly constructed buildings and infrastructure
        new_m2_JPY_extended_matrix = pd.concat([new_m2_JPY_extended_matrix, pd.Series(new_m2_JPY_extended)],axis = 1, ignore_index = True)        
               
        # concrete consumption
        con_app = new_m2_JPY_extended*int_Con_matrix.iloc[:,i]-reuse_Con_extended
        con_app_matrix = pd.concat([con_app_matrix, pd.Series(con_app)], axis = 1, ignore_index = True)

        # cement consumption
        cem_app = new_m2_JPY_extended*int_Cem_matrix.iloc[:,i]-reuse_Cem_extended
        cem_app_matrix = pd.concat([cem_app_matrix, pd.Series(cem_app)], axis = 1, ignore_index = True)

        # timber consumption
        tim_con = new_m2_JPY_extended*int_Tim_matrix.iloc[:,i]
        tim_con_matrix = pd.concat([tim_con_matrix, pd.Series(tim_con)], axis = 1, ignore_index = True)            
            
        # demolished concrete
        dem_con = demol_Con_extended - reuse_Con_extended
        dem_con_matrix = pd.concat([dem_con_matrix, pd.Series(dem_con)], axis = 1, ignore_index = True)
        
        # demolished timber
        dem_tim = demol_Tim_extended
        dem_tim_matrix = pd.concat([dem_tim_matrix, pd.Series(dem_tim)], axis = 1, ignore_index = True)
        
    dem_con_matrix_merge=pd.concat([dem_con_matrix.fillna(0)[x]+dem_con_matrix[y] for x,y in zip(range(0,21),range(21,42))], axis = 1)
    
    Concrete_demand = np.sum(con_app_matrix, axis=1)
    Cement_demand = np.sum(cem_app_matrix, axis=1)
    Timber_demand = np.sum(tim_con_matrix, axis=1)
    Concrete_demolish = np.sum(dem_con_matrix_merge, axis=1)
    Timber_demolish = np.sum(dem_tim_matrix, axis=1)
    
    Concrete_demand_share = con_app_matrix.div(Concrete_demand, axis=0)
    Concrete_demolish_share = dem_con_matrix_merge.div(Concrete_demolish, axis=0)
        
    Life_average_matrix = Concrete_demand_share*Life_matrix
    Life_average = Life_average_matrix.sum(axis=1)
    Std_average_matrix = Concrete_demand_share*Std_matrix
    Std_average = Std_average_matrix.sum(axis=1)
    Rec_average_matrix = Concrete_demolish_share*Rec_matrix
    Rec_average = Rec_average_matrix.sum(axis=1)
    Reuse_average_matrix = Concrete_demolish_share*Reuse_matrix
    Reuse_average = Reuse_average_matrix.sum(axis=1)
    burRate = 1-Rec_average-Reuse_average
    
    Recycled_aggregate = Concrete_demolish*Rec_average
    Virgin_aggregate = 0.90770*(Concrete_demand-Cement_demand)-Recycled_aggregate-\
    (Concrete_demolish*CO2_mine_EOL_share)-(Concrete_demand*(CO2_mine_slag_share+CO2_mine_ash_share+\
                                                             CO2_mine_lime_share+CO2_mine_red_share))
    Water_demand = 0.09230*(Concrete_demand-Cement_demand)
    
    filepath = 'Result'
    pd.DataFrame(Concrete_demand).to_excel(filepath + '/concrete_demand_' + str(scenario_index) + '.xlsx')
    pd.DataFrame(Cement_demand).to_excel(filepath + '/cement_demand_' + str(scenario_index) + '.xlsx')
    pd.DataFrame(Concrete_demolish).to_excel(filepath + '/concrete_demolish_' + str(scenario_index) + '.xlsx')
    pd.DataFrame(Virgin_aggregate).to_excel(filepath + '/virgin_aggregate_' + str(scenario_index) + '.xlsx')
    pd.DataFrame(Water_demand).to_excel(filepath + '/water_demand_' + str(scenario_index) + '.xlsx')
    pd.DataFrame(con_app_matrix).to_excel(filepath + '/concrete_demand_matrix_' + str(scenario_index) + '.xlsx')
    pd.DataFrame(cem_app_matrix).to_excel(filepath + '/cement_demand_matrix_' + str(scenario_index) + '.xlsx')
    pd.DataFrame(dem_con_matrix_merge).to_excel(filepath + '/concrete_demolish_matrix_' + str(scenario_index) + '.xlsx')
    
    import emissions_model

    emissions_model.emissions_calculate(
    year_len = 101,
    index_year2020 = 0,
    index_year2050 = 101,
    Belite_share = Belite_share,
    Belite_fue_save = Belite_fue_save,
    Belite_pro_save = Belite_pro_save,
    BYF_share = BYF_share,
    BYF_fue_save = BYF_fue_save,
    BYF_pro_save = BYF_pro_save,
    CCSC_share = CCSC_share,
    CCSC_fue_save = CCSC_fue_save,
    CCSC_pro_save = CCSC_pro_save,
    CCSC_CO2_credit = CCSC_CO2_credit,
    CSAB_share = CSAB_share,
    CSAB_fue_save = CSAB_fue_save,
    CSAB_pro_save = CSAB_pro_save,
    Celite_share = Celite_share,
    Celite_fue_save = Celite_fue_save,
    Celite_pro_save = Celite_pro_save,
    MOMS_share = MOMS_share,
    MOMS_fue_save = MOMS_fue_save,
    MOMS_pro_save = MOMS_pro_save,
    Pro_Em_factor = Pro_Em_factor,
    Them_eff = Them_eff,
    Coal_share_cem = Coal_share_cem,
    Coal_CO2_cem = Coal_CO2_cem,
    Coke_share_cem = Coke_share_cem,
    Coke_CO2_cem = Coke_CO2_cem,
    Oil_share_cem = Oil_share_cem,
    Oil_CO2_cem = Oil_CO2_cem,
    WaFu_share_cem = WaFu_share_cem,
    WaFu_CO2_cem = WaFu_CO2_cem,
    NaGa_share_cem = NaGa_share_cem,
    NaGa_CO2_cem = NaGa_CO2_cem,
    Ele_eff = Ele_eff,
    Coal_share_ele = Coal_share_ele,
    Coal_CO2_ele = Coal_CO2_ele,
    Oil_share_ele = Oil_share_ele,
    Oil_CO2_ele = Oil_CO2_ele,
    Naga_share_ele = Naga_share_ele,
    Naga_CO2_ele = Naga_CO2_ele,
    Hydr_share_ele = Hydr_share_ele,
    Hydr_CO2_ele = Hydr_CO2_ele,
    Geot_share_ele = Geot_share_ele,
    Geot_CO2_ele = Geot_CO2_ele,
    Sol_share_ele = Sol_share_ele,
    Sol_CO2_ele = Sol_CO2_ele,
    Wind_share_ele = Wind_share_ele,
    Wind_CO2_ele = Wind_CO2_ele,
    Tide_share_ele = Tide_share_ele,
    Tide_CO2_ele = Tide_CO2_ele,
    Nuc_share_ele = Nuc_share_ele,
    Nuc_CO2_ele = Nuc_CO2_ele,
    Bio_share_ele = Bio_share_ele,
    Bio_CO2_ele = Bio_CO2_ele,
    Was_share_ele = Was_share_ele,
    Was_CO2_ele = Was_CO2_ele,
    SoTh_share_ele = SoTh_share_ele,
    SoTh_CO2_ele = SoTh_CO2_ele,
    clinker = clinker,
    Cal_share = Cal_share,
    Ene_Cal = Ene_Cal,
    CCS_Oxy_percent = CCS_Oxy_percent,
    Eff_Oxy = Eff_Oxy,
    Ene_Oxy = Ene_Oxy,
    CCS_Pos_percent = CCS_Pos_percent,
    Eff_Pos = Eff_Pos,
    Ene_Pos = Ene_Pos,
    Cement_demand = Cement_demand,
    CO2_tran_cem = CO2_tran_cem,
    Concrete_demand = Concrete_demand,
    Virgin_aggregate = Virgin_aggregate,
    Recycled_aggregate = Recycled_aggregate,
    CO2_prod_agg = CO2_prod_agg,
    CO2_tran_agg = CO2_tran_agg,
    Concrete_demolish = Concrete_demolish,
    recRate = Rec_average,
    CO2_prod_rec = CO2_prod_rec,
    CO2_tran_rec = CO2_tran_rec,
    burRate = burRate,
    CO2_tran_bur = CO2_tran_bur,
    CO2_mix_con = CO2_mix_con,
    CO2_tran_con = CO2_tran_con,
    CO2_onsite_con = CO2_onsite_con,
    CO2_curing_emi = CO2_curing_emi,
    CO2_mine_EOL_emi = CO2_mine_EOL_emi,
    CO2_mine_slag_emi = CO2_mine_slag_emi,
    CO2_mine_slag_sto = CO2_mine_slag_sto,
    CO2_mine_ash_emi = CO2_mine_ash_emi,
    CO2_mine_ash_sto = CO2_mine_ash_sto,
    CO2_mine_lime_emi = CO2_mine_lime_emi,
    CO2_mine_lime_sto = CO2_mine_lime_sto,
    CO2_mine_red_emi = CO2_mine_red_emi,
    CO2_mine_red_sto = CO2_mine_red_sto,
    Timber_demand = Timber_demand,
    CO2_tim_pen = CO2_tim_pen,
    CO2_tim_sto = CO2_tim_sto,
    Timber_demolish = Timber_demolish,
    EoL_tim_land = EoL_tim_land,
    Land_tim_deg = Land_tim_deg,
    Deg_tim_CH4 = Deg_tim_CH4,
    Deg_tim_CO2 = Deg_tim_CO2,
    CH4_to_CO2 = CH4_to_CO2,
    CH4_recover = CH4_recover,
    EoL_tim_inci = EoL_tim_inci,
    scenario_index = scenario_index,
    filepath = filepath
    )
    
    import physicochemical_model

    physicochemical_model.cement_carbonation(
    year_len = 101,
    index_year2020 = 0,
    Belite_share = Belite_share,
    Belite_alk_save = Belite_alk_save,
    BYF_share = BYF_share,
    BYF_alk_save = BYF_alk_save,
    CCSC_share = CCSC_share,
    CCSC_alk_save = CCSC_alk_save,
    CSAB_share = CSAB_share,
    CSAB_alk_save = CSAB_alk_save,
    Celite_share = Celite_share,
    Celite_alk_save = Celite_alk_save,
    MOMS_share = MOMS_share,
    MOMS_alk_save = MOMS_alk_save,
    CO2_curing_share = CO2_curing_share,
    CO2_curing_coef = CO2_curing_coef,
    CO2_mine_EOL_share = CO2_mine_EOL_share,
    CO2_mine_EOL_coef = CO2_mine_EOL_coef,
    clinker = clinker,
    Cement_demand = Cement_demand,
    waste_saving = waste_saving,
    scenario_index = scenario_index,
    Life = Life_average,
    Std = Std_average,
    reuse_rate = Reuse_average,
    recRate = Rec_average,
    burRate = burRate,
    store_t = store_t,
    filepath = filepath
    )