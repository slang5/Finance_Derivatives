import numpy as np

#Values
Accuracy = 6
StepTime = 1/365

#Goal : Generate path of underlying asset with everything expressed in percentage and time in proportion of year
#good but not enough for Monte Carlo simulation

def Random(size:int=1, Precision:int=Accuracy) ->np.array: #Generate random number following a normal distribution
    return np.round(np.random.normal(0,1,size),Precision)

def BS_AssetVariation(div:float=0, rf:float=0, volatility:float=0, dt:float=StepTime, alea:float=0) ->np.array: #Generate the variation of the asset
    drift = rf - div
    output = np.exp((drift - 0.5 * volatility**2) * dt + volatility * np.sqrt(dt) * alea)
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

def CholeskyCorrelated_Variation(CovMatrix:np.array, T:int=1, dt:float=StepTime, Precision:int=Accuracy) ->np.array: #Generate the correlated variation of the asset
    
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

def Correlated_PathsPerf(SpotMatrix:np.array, DriftMatrix:np.array, VolatilityMatrix:np.array, CorrelationMatrix: np.array, T:int=1, dt:float=StepTime, Precision:int=Accuracy)-> np.array:
    #TypePath = "Worst" or "Best"
    #SpotMatrix : [S0, Si-1, Si, ...] (Si is the initial value of the asset i)
    #DriftMatrix : [rf - dividend] (ofr each asset)
    #VolatilityMatrix : [volatility0, volatilityi, ...] (volatilityi is the volatility of the asset i)
    
    #sanitary check
    if not (len(SpotMatrix) == len(DriftMatrix) and len(SpotMatrix) == len(VolatilityMatrix) and len(SpotMatrix) == np.shape(CorrelationMatrix)[0] and dt <= T):
        print("Path_WorstBestOf : The length of the matrices is not the same")
        return None
    else:
        nb_assets = len(SpotMatrix)
        CorrelatedPaths = CholeskyCorrelated_Variation(CorrelationMatrix, T, dt, Precision)
        PathsMatrix = [BS_Path_Asset_Perf(SpotMatrix[i],0,DriftMatrix[i],VolatilityMatrix[i],CorrelatedPaths[:,i],dt,Precision) for i in range(nb_assets)]
        PathsMatrix = np.transpose(PathsMatrix)
        return np.round(PathsMatrix,Precision)
    
def Correlated_PathsAbs(SpotMatrix:np.array, DriftMatrix:np.array, VolatilityMatrix:np.array, CorrelationMatrix: np.array, T:int=1, dt:float=StepTime, Precision:int=Accuracy)-> np.array:
    #TypePath = "Worst" or "Best"
    #SpotMatrix : [S0, Si-1, Si, ...] (Si is the initial value of the asset i)
    #DriftMatrix : [rf - dividend] (ofr each asset)
    #VolatilityMatrix : [volatility0, volatilityi, ...] (volatilityi is the volatility of the asset i)
    
    #sanitary check
    if not (len(SpotMatrix) == len(DriftMatrix) and len(SpotMatrix) == len(VolatilityMatrix) and len(SpotMatrix) == np.shape(CorrelationMatrix)[0] and dt <= T):
        print("Path_WorstBestOf : The length of the matrices is not the same")
        return None
    else:
        nb_assets = len(SpotMatrix)
        CorrelatedPaths = CholeskyCorrelated_Variation(CorrelationMatrix, T, dt, Precision)
        PathsMatrix = [BS_Path_Asset(SpotMatrix[i],0,DriftMatrix[i],VolatilityMatrix[i],CorrelatedPaths[:,i],dt,Precision) for i in range(nb_assets)]
        PathsMatrix = np.transpose(PathsMatrix)
        return np.round(PathsMatrix,Precision)

def Path_WorstBestOf(TypePath:str ,PathsMatrix:np.array, Precision:int=Accuracy) -> np.array:
    #TypePath = "Worst" or "Best"
    if TypePath == "Worst":
        return WorstOf_Path(PathsMatrix,Precision)
    elif TypePath == "Best":
        return BestOf_Path(PathsMatrix,Precision)
    else:
        print("Path_WorstBestOf : TypePath must be 'Worst' or 'Best'")
        return None
    
def Path_Average(WeightMatrix:np.array, PathsMatrix:np.array, Precision:int=Accuracy) -> np.array:
    #WeightMatrix : [w0, wi-1, wi, ...] (wi is the weight of the asset i)
    #PathsMatrix : [Path0, Pathi-1, Pathi, ...] (Pathi is the path of the asset i)
    if len(WeightMatrix) != np.shape(PathsMatrix)[1]:
        print("Path_Average : matrices are not the same size")
        return None
    else:
        AveragePath = np.sum(WeightMatrix * PathsMatrix, axis=1)
        return np.round(AveragePath,Precision)
    
def Path_EndValues(PathsMatrix:np.array) -> np.array:
    shape = PathsMatrix.shape[0]-1
    if shape >=0:
        return PathsMatrix[shape]
    else:
        raise ValueError("Error: array is too small")
