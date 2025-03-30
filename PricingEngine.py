import numpy as np
import multiprocessing
import time

'''def monte_carlo_batch(n_simulations):
    """ Simule plusieurs trajectoires en batch """
    S0, r, sigma, T, N = 100, 0.05, 0.2, 1, 100
    dt = T / N
    Z = np.random.standard_normal((N, n_simulations))  # Génère les chocs aléatoires
    S = S0 * np.exp(np.cumsum((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z, axis=0))
    return np.mean(S[-1, :])  # Moyenne des prix finaux'''

'''if __name__ == "__main__":
    start_time = time.time()  # Démarre le chronomètre
    
    num_simulations = 5_000_000
    num_cores = multiprocessing.cpu_count()  # Nombre de cœurs disponibles
    batch_size = num_simulations // num_cores  # Divise en plusieurs groupes

    print(f"Nombre de cœurs disponibles : {num_cores}")
    print(f"Nombre total de simulations : {num_simulations}")
    print(f"Nombre de simulations par cœur : {batch_size}")

    with multiprocessing.Pool(processes=num_cores) as pool:
        results = pool.map(monte_carlo_batch, [batch_size] * num_cores)

    estimated_price = np.mean(results)  # Moyenne des prix simulés

    end_time = time.time()  # Arrête le chronomètre
    execution_time = end_time - start_time  # Calcule le temps écoulé

    print(f"Prix estimé : {estimated_price}")
    print(f"Temps total d'exécution : {execution_time:.2f} secondes")'''

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