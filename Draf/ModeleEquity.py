import numpy as np

def Correlation(rho:float=0, epsilon1:float=0, epsilon2:float=0, dt:float=1/365, type:str="") ->float:
    if type =="Cho":
        return rho * epsilon1 + ((1-rho**2)**0.5)*epsilon2
    elif type == "Bro":
        return rho * dt / epsilon1
    else:
        return None
    
def CorrelatedMatrix(rho:float=0, size:int=1) ->np.array:
    matrice_1 = [i for i in np.random.normal(0,1,size)]
    matrice_2 = [i for i in np.random.normal(0,1,size)]
    output = [[i,Correlation(rho,i,j,1/365,"Cho")] for i,j in zip(matrice_1,matrice_2)]
    
    return np.round(np.transpose(output),5)
    
def Alea(size:int=1) ->np.array:
    return np.round(np.random.normal(0,1,size),5)

def AssetVariation(drift:float=0, volatility:float=0, dt:float=1/365, alea:float=0) ->np.array:
    output = np.exp((drift - 0.5 * volatility**2) * dt + volatility * (dt**0.5) * alea)
    output = np.cumprod(output)
    return np.insert(output,0,1)

def Path_Asset(S0:float=100, drift:float=0, volatility:float=0, T:int=365, dt:float=1/365) ->np.array:
    rnd = np.random.normal(0,1,T)
    AssetVar = [AssetVariation(drift,volatility,dt,i) for i in rnd]
    return [S0 * i for i in np.cumprod(AssetVar).tolist()]

def Path_InFine_Asset(S0:float=100, drift:float=0, volatility:float=0, T:int=365, dt:float=1/365) ->np.array:
    AssetVar = AssetVariation(drift,volatility,T*dt,Alea(1))[-1:]
    return AssetVar * S0

def Path_2Assets_Correlated_with_initial(S0_1: float = 100, S0_2: float = 100, rho: float = 0, drift_1: float = 0, drift_2: float = 0, volatility_1: float = 0, volatility_2: float = 0, T: int = 365, dt: float = 1/365) -> np.array:
    Correl = CorrelatedMatrix(rho, T)
    AssetVar_1 = [AssetVariation(drift_1, volatility_1, dt, i) for i in [i for i, j in Correl]]
    AssetVar_2 = [AssetVariation(drift_2, volatility_2, dt, j) for i, j in Correl]
    path_1 = [S0_1] + [S0_1 * i for i in np.cumprod(AssetVar_1).tolist()]
    path_2 = [S0_2] + [S0_2 * j for j in np.cumprod(AssetVar_2).tolist()]
    return np.array(list(zip(path_1, path_2)))

def Paths_1and2_from_Path2AssetsCorrelated(Paths:np.array):
    return [Paths[:, 0],Paths[:, 1]]


