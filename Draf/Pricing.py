import numpy as np
import ModeleEquity as PathEquity

def SqrtMax(Spot, Strike, Call:bool):
    if Call:
        return np.maximum(Spot - Strike, 0)**0.5
    else:
        return np.maximum(Strike - Spot, 0)**0.5

def InfineValue(S0:float, drift:float, volatility:float, T:int, N:int) ->np.array:
    return [PathEquity.Path_InFine_Asset(S0, drift, volatility, T,1) for i in range(N)]

def MonteCarlo_VanillaOption(S0:float, Strike:float, div:float,rf:float , volatility:float, Call: bool,T:int, N:int):
    InFine = InfineValue(S0,rf-div,volatility,T,N)
    if Call:
        output = np.maximum(np.array(InFine) - Strike, 0)
    else:
        output = np.maximum(Strike - np.array(InFine), 0)
    return np.mean(output) * np.exp(-rf * T)

def MonteCarlo_LeveragePowercall(S0:float, Strike:float, div:float,rf:float , volatility:float, Call: bool,T:int, N:int, leverage:float) ->float:
    InFine = InfineValue(S0,rf-div,volatility,T,N)
    InFine = np.array(InFine)
    if Call:
        output = np.where(InFine > Strike, SqrtMax(InFine,Strike,Call), 0)
    else:
        output = np.where(InFine < Strike, SqrtMax(InFine,Strike,Call), 0)
    return np.mean(output*leverage) * np.exp(-rf * T)

def MonteCarlo_BarrierOption_KI(S0:float, Strike:float, div:float,rf:float , volatility:float, Call: bool,T:int, N:int, Barrier:float) ->float:
    InFine = InfineValue(S0,rf-div,volatility,T,N)
    InFine = np.array(InFine)
    if Call:
        output = np.where(InFine> Barrier, np.maximum(InFine - Strike, 0),0)

    else:
        output = np.where(InFine< Barrier, np.maximum(Strike - InFine, 0),0)

    return np.mean(output) * np.exp(-rf * T)

def MonteCarlo_BarrierOption_KO(S0:float, Strike:float, div:float,rf:float , volatility:float, Call: bool,T:int, N:int, Barrier:float) ->float:
    InFine = InfineValue(S0,rf-div,volatility,T,N)  
    InFine = np.array(InFine)
    if Call:
        output = np.where(InFine< Barrier, np.maximum(InFine - Strike, 0),0)

    else:
        output = np.where(InFine> Barrier, np.maximum(Strike - InFine, 0),0)

    return np.mean(output) * np.exp(-rf * T)

def MonteCarlo_Digit(S0:float, Strike:float, div:float,rf:float , volatility:float, Call: bool,T:int, N:int, levier:float) ->float:
    InFine = InfineValue(S0,rf-div,volatility,T,N)
    InFine = np.array(InFine)
    if Call:
        output = np.where(InFine > Strike, levier, 0)
    else:
        output = np.where(InFine < Strike, levier, 0)
    return np.mean(output) * np.exp(-rf * T)

