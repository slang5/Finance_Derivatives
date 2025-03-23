import numpy as np

#Values
Accuracy = 6
StepTime = 1/365

#Goal : Generate path of underlying asset with everything expressed in percentage and time in proportion of year

def Random(size:int=1, Precision:int=Accuracy) ->np.array: #Generate random number following a normal distribution
    return np.round(np.random.normal(0,1,size),Precision)

def BS_AssetVariation(div:float=0, rf:float=0, volatility:float=0, dt:float=StepTime, alea:float=0) ->np.array: #Generate the variation of the asset
    drift = rf - div
    output = np.exp((drift - 0.5 * volatility**2) * dt + volatility * (dt**0.5) * alea)
    output = np.cumprod(output)
    return np.insert(output,0,1)

def BS_Path_Asset(S0:float=100, div:float=0, rf:float=0, volatility:float=0, rnd:np.array="", dt:float=StepTime, Precision:int=Accuracy) ->np.array: #Generate the path of the asset
    #dt is the periodicity of the observation
    Variation = BS_AssetVariation(div,rf,volatility,dt,rnd) * np.array(S0)
    return np.round(Variation,Precision)

def BS_Path_Asset_Perf(S0:float=100, div:float=0, rf:float=0, volatility:float=0, rnd:np.array="", dt:float=StepTime, Precision:int=Accuracy) ->np.array: #Generate the path of the asset described as performance from initial value 
    #dt is the periodicity of the observation
    Path = BS_Path_Asset(S0,div,rf,volatility,rnd,dt,Precision) - np.array(S0)
    Path = Path / np.array(S0)
    return np.round(Path,Precision)

def CholeskyCorrelated_Variation(CovMatrix:np.array, T:iter=1, dt:float=StepTime, Precision:int=Accuracy) ->np.array: #Generate the correlated variation of the asset
    
    if np.linalg.eigvals(CovMatrix).min() < 0:
        print("CholeskyCorrelated_Variation : The matrix is not positive definite")
        return None
    else:
        nb_iteration = int(T/dt)
        nb_assets = len(CovMatrix)
        L = np.linalg.cholesky(CovMatrix)
        Z = np.random.normal(0,1,(nb_iteration,nb_assets))
        Rdn = np.dot(Z,np.transpose(L))
        return np.round(Rdn,Precision) 

def WorstOf_Path(Assets_path:np.array, Precision:int=Accuracy) ->np.array: #Generate the worst path from the paths of the assets
    return np.round(np.min(Assets_path,axis=1),Precision)

def BestOf_Path(Assets_path:np.array, Precision:int=Accuracy) ->np.array: #Generate the best path from the paths of the assets
    return np.round(np.max(Assets_path,axis=1),Precision)