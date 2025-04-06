import numpy as np

def ApproxTimeComputing(TempsParAn:float, StepTime:float, N_Simulations:int, N_Assets:int)->float:
    """
    Approximate the time needed to compute the simulation in seconds.
    """
    if TempsParAn <= 0 or StepTime <= 0 or N_Simulations <= 0 or N_Assets <= 0:
        raise ValueError("Erreur : valeur nulle ou negative")
    
    return f"Approx : {(TempsParAn / StepTime) * N_Simulations * N_Assets * 36 / 328500000} sec for computation" #in seconds

class Simulation_Class:

    def __init__(self, N_Simulations: int, Precision:int, N_Assets: int, DriftMatrix:np.array, VolatilityMatrix:np.array, CorrelationMatrix:np.array, TempsParAn:float, StepTime:float):
        
        self.N_Simulations: int
        self.Precision: int
        self.N_Assets: int
        self.DriftMatrix: np.array
        self.VolatilityMatrix: np.array
        self.CorrelationMatrix: np.array
        self.TimeToMaurity: float
        self.dt: float
        self.RandomMatrix: np.array
        self.Steps: int

        if N_Assets == np.shape(DriftMatrix)[0] and N_Assets == np.shape(VolatilityMatrix)[0] and np.shape(CorrelationMatrix)[0] == np.shape(CorrelationMatrix)[1] and N_Assets == np.shape(CorrelationMatrix)[0] and  TempsParAn>=StepTime:
            self.N_Simulations = N_Simulations
            self.Precision = Precision
            self.N_Assets = N_Assets
            self.DriftMatrix = DriftMatrix
            self.VolatilityMatrix = VolatilityMatrix
            self.CorrelationMatrix = CorrelationMatrix
            self.TimeToMaurity = TempsParAn
            self.dt = StepTime
            self.Steps = int(self.TimeToMaurity / self.dt)
            self.RandomMatrix = None
            self.PathsMatrix = None
            print("__init__ : Done")
        else:
            raise ValueError("Erreur : problème de cohérence dans les inputs")
        
    def GenerateRandomMatrix(self):
        if not (self.TimeToMaurity <= 0 and self.dt <= 0 and self.Steps <= 0):
            self.RandomMatrix = np.random.normal(0,1,(self.N_Simulations,self.Steps,self.N_Assets)).astype(np.float32)
            print("GenerateRandomMatrix : Done")
        else:
            raise ValueError("Erreur : valeur nulle ou negative")
        
    def ComputeCorrel(self,Array:np.array)->np.array:
        if np.linalg.eigvals(self.CorrelationMatrix).min() < 0:
            print("Erreur : Matrice Correlation n'est pas positive definite")
            return None
        else:
            L = np.linalg.cholesky(self.CorrelationMatrix)
            Z = Array
            Rdn = np.dot(L,np.transpose(Z))
            return np.array(Rdn.T,dtype=np.float32)

    def ApplyCorrelation(self):
        if self.RandomMatrix is not None:
            self.RandomMatrix = [self.ComputeCorrel(self.RandomMatrix[i]) for i in range(0,self.RandomMatrix.shape[0])]
            print("ApplyCorrelation : Done")
        else:
            raise ValueError("Erreur : Matrice Random n'est pas definie")
        
    def ComputeVariation(self)->np.array:
        if self.RandomMatrix is not None:
            self.PathsMatrix = (np.cumprod(np.exp((self.DriftMatrix - 0.5 * self.VolatilityMatrix **2)*self.dt + self.VolatilityMatrix * np.sqrt(self.dt) * self.RandomMatrix).astype(np.float32),1)).astype(np.float32)
            self.PathsMatrix = np.insert(self.PathsMatrix,0,1,axis=1)
            print("ComputeVariation : Done")
        else:
            raise ValueError("Erreur : Matrice Random n'est pas definie")

    def EstimationComputation(self):
        return ApproxTimeComputing(self.TimeToMaurity, self.dt, self.N_Simulations, self.N_Assets)
    
    def BestOf(self, OnlyEnd:str = "Y")->np.array:
        if self.PathsMatrix is not None:
            if OnlyEnd == "Y":
                return np.max(self.PathsMatrix[:,self.Steps],axis=1).astype(np.float32)
            elif OnlyEnd == "N":
                return None #np.max(self.PathsMatrix,axis=1).astype(np.float32)
        else:
            raise ValueError("Erreur : Matrice Paths n'est pas definie")
        
    def WorstOf(self, OnlyEnd:str = "Y")->np.array:
        if self.PathsMatrix is not None:
            if OnlyEnd == "Y":
                return np.min(self.PathsMatrix[:,self.Steps],axis=1).astype(np.float32)
            elif OnlyEnd == "N":
                return None #np.min(self.PathsMatrix,axis=1).astype(np.float32)
        else:
            raise ValueError("Erreur : Matrice Paths n'est pas definie")
        
    def AverageOf(self, Weight:np.array, OnlyEnd:str = "Y")->np.array:
        if self.PathsMatrix is not None:
            if OnlyEnd == "Y":
                return np.sum(self.PathsMatrix[:,self.Steps] * Weight,axis=1).astype(np.float32)
            elif OnlyEnd == "N":
                return None

    def ComputeEuropeanVanillaOption(self, BasketMethod:str,Strike:float,leverage:float, rebate:float,rf:float, TypeOption:str="Call", Weight:np.array=None)->float:
        #rebate is not leveraged
        output: np.array
        if self.PathsMatrix is not None:
            if BasketMethod == "Best":
                output =  self.BestOf("Y")
            elif BasketMethod == "Worst":
                output = self.WorstOf("Y")
            elif BasketMethod == "Average":
                output = self.AverageOf(Weight, "Y")
            elif BasketMethod == "Spread": #spread based on Best - Worst
                output = self.BestOf("Y") - self.WorstOf("Y")
            else:
                raise ValueError("Erreur : BasketMethod non reconnu")
                return None
            
            if TypeOption == "Call":
                output = np.maximum(0,output - Strike) * leverage
                output = np.where(output == 0,rebate,output)
                return np.mean(output * np.exp(-rf * self.TimeToMaurity),0)
            elif TypeOption == "Put": 
                output = np.maximum(0,Strike - output) * leverage
                output = np.where(output == 0,rebate,output)
                return np.mean(output * np.exp(-rf * self.TimeToMaurity),0)
            else:
                raise ValueError("Erreur : OptionType non reconnu")
        else:
            raise ValueError("Erreur : Matrice Paths n'est pas definie")
        
    