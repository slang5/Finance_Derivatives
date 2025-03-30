import numpy as np

Accuracy = 6

def PayOff_Call(EndValue:float, Strike:float, rf:float, T:float, Precision:int=Accuracy)->float:
    if EndValue > Strike:
        return np.round(np.exp(-rf * T) * (EndValue - Strike),Precision)
    else:
        return 0.0
    
def PayOff_Put(EndValue:float, Strike:float, rf:float, T:float, Precision:int=Accuracy)->float:
    if EndValue < Strike:
        return np.round(np.exp(-rf * T) * (Strike - EndValue),Precision)
    else:
        return 0.0

def Pricing_CallPut(EndValue:np.array, Strike:float, rf:float, T:float,TypeOption:str="Call",Precision:int=Accuracy):
    if TypeOption == "Call":
        result = np.mean([PayOff_Call(i, Strike,rf,T) for i in EndValue])
    elif TypeOption == "Put":
        result = np.mean([PayOff_Put(i, Strike,rf,T) for i in EndValue])
    else:
        raise ValueError("TypeOption must be 'Call' or 'Put'")
    return result

def Pricing_DigitBull(EndValue:float, Strike:float, rf:float, T:float, Precision:int=Accuracy)->float:
    if EndValue >= Strike:
        return 1
    else:
        return 0.0

def Pricing_DigitBear(EndValue:float, Strike:float, rf:float, T:float, Precision:int=Accuracy)->float:
    if EndValue <= Strike:
        return 1
    else:
        return 0.0
    

def PayOff_Digit(EndValue:np.array, Strike:float,Gain:float, rf:float, T:float,TypeOption:str="Bull",Precision:int=Accuracy)->float:
    if TypeOption == "Bull":
        result = np.mean([Pricing_DigitBull(i, Strike,rf,T) for i in EndValue])*Gain
    elif TypeOption == "Bear":
        result = np.mean([Pricing_DigitBear(i, Strike,rf,T) for i in EndValue])*Gain
    else:
        raise ValueError("TypeOption must be 'Bull' or 'Bear'")
    return result
