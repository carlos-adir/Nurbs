import numpy as np
from typing import Iterable, Any, Optional, Union, Tuple, Type
from compmec.nurbs.spaceu import VectorU 

def N(i: int, j: int, k: int, u: float, U: VectorU) -> float:
    """
    Returns the value of N_{ij}(u) in the interval [u_{k}, u_{k+1}]
    Remember that N_{i, j}(u) = 0   if  ( u not in [U[i], U[i+j+1]] )
    """
    
    n, p = U.n, U.p
    
    if k < i:
        return 0
    if j == 0:
        if i == k:
            return 1
        if i + 1 == n and k == n:
            return 1
        return 0
    if i + j < k:
        return 0

    if i+j > n+p:
        factor1 = 0
    elif U[i] == U[i+j]:
        factor1 = 0
    else:
        factor1 = (u-U[i])/(U[i+j]-U[i])

    if i+j+1 > n+p:
        factor2 = 0
    elif U[i+j+1] == U[i+1]:
        factor2 = 0
    else:
        factor2 = (U[i+j+1]-u)/(U[i+j+1]-U[i+1])

    result = factor1 * N(i, j-1, k, u, U) + factor2 * N(i+1, j-1, k, u, U)
    return result

def R(i: int, j: int, k: int, u: float, U: VectorU, w: Iterable[float]) -> float:
    """
    Returns the value of R_{ij}(u) in the interval [u_{k}, u_{k+1}]
    """
    Niju = N(i, j, k, u, U)
    if Niju == 0:
        return 0
    n = len(w)
    soma = 0
    for z in range(n):
        soma += w[z] * N(z, j, k, u, U)
    return w[i] * Niju / soma



class EvaluationClass(object):

    def __init__(self, U: Iterable[float], p: int, tup: Union[None, int, slice, Tuple]= None, A: Optional[np.ndarray]=None):
        self._U = VectorU(U)
        self._p = p
        self.__initialize_tup(tup)
        self.A = A

    def __initialize_tup(self, tup):
        if tup is None:
            self.i = None
            self.j = self.p
        elif isinstance(tup, tuple):
            if len(tup) > 2:
                raise IndexError("The dimension of N is maximum 2")
            self.i = tup[0]
            self.j = tup[1]
        else:
            self.i = tup
            self.j = self.p

    @property
    def i(self):
        return self._i
    
    @property
    def j(self):
        return self._j

    @property
    def p(self):
        return self._p

    @property
    def n(self):
        return self.U.n

    @property
    def U(self):
        return self._U

    @property
    def A(self):
        return self._A

    @i.setter
    def i(self, value: Union[None, int, slice]):
        if value is None:
            self._i = range(0, self.n, 1)
            return
        if isinstance(value, slice):
            start = 0 if value.start is None else value.start
            stop = self.U.n if value.stop is None else value.stop
            step = 1 if value.step is None else value.step
            self._i = range(start, stop, step)
            return
        if isinstance(value, range):
            self._i = value
            return
        try:
            value = int(value)
            if value > self.U.n:
                raise ValueError("The frist value must be <= n = %d" % self.U.n)
            self._i = range(value, value+1, 1)
            return
        except Exception as e:
            raise TypeError(f"Type {type(value)} is incorrect to set i")
        
    @j.setter
    def j(self, value: int):
        try:
            value = int(value)
            if value < 0:
                raise ValueError("The second value (%d) must be >= 0" % value)
            elif self.p < value:
                raise ValueError("The second value (%d) must be <= p = %d" % (value, self.p))
            self._j = value
            return
        except Exception as e:
            raise TypeError(f"Type {type(value)} is incorrect to set j")

    @p.setter
    def p(self, value: int):
        if value < 0:
            raise ValueError("p must be >= 0")
        self._p = int(value)

    @A.setter
    def A(self, value: np.ndarray):
        if value is None:
            self._A = np.eye(self.U.n)
        else:
            value = np.array(value)
            if value.ndim != 2 or value.shape[0] != self.U.n:
                raise ValueError("The given numpy array must be a square matrix")
            self._A = np.array(value)


    def __validate_evaluation_u(self, u: np.ndarray):
        U = self._U
        minU = np.min(U)
        maxU = np.max(U)
        if not np.all((minU <= u) * (u <= maxU)):
            raise Exception(f"All values of u must be inside the interval [{minU}, {maxU}]")
        if np.array(u).ndim > 1:
            raise ValueError("For the moment we can only evaluate scalars or 1D array")
        

    def __treat_input(self, u: Union[float, np.ndarray]) -> np.ndarray:
        try:
            len(u)
        except Exception as e:
            u = [u]
        return np.array(u)

    def compute_matrix(self, u: Union[float, np.ndarray]) -> np.ndarray:
        """
        In this function, u is a vector, while i is a range
        """
        u = self.__treat_input(u)
        r = np.zeros((self.n, len(u)))
        for w, uw in enumerate(u):
            k = self._U.spot(uw)
            for ind in self.i:
                r[ind, w] = self.f(ind, self.j, k, uw, self._U)
        return r
    
    def compute_all(self, u: np.ndarray) -> np.ndarray:
        return self.A @ self.compute_matrix(u)

    def __call__(self, u: Union[float, np.ndarray]) -> np.ndarray:
        self.__validate_evaluation_u(u)
        u = self.__treat_input(u)
        result = self.A @ self.compute_matrix(u)
        return result[self.i]


class BaseFunction(object):

    def __init__(self, U: Iterable[float]):
        """
        We have that the object can be called like
        N = SplineBaseFunction(U)

        And so, to get the value of N_{i, j}(u) can be express like
        N[i, j](u)
        """
        if isinstance(U, VectorU):
            self._U = U
        else:
            self._U = VectorU(U)
        self._p = self._U.p

    @property
    def p(self) -> int:
        return self._p

    @property
    def n(self) -> int:
        return self._U.n

    @property
    def U(self) -> Tuple[float]:
        return tuple(self._U)

    @property
    def evaluationClass(self) -> type[EvaluationClass]:
        """
        This function must be overwritten.
        If it's spline, evalfunction = N
        If it's rational, evalfunction = R
        """
        raise NotImplementedError("This function must be overwritten")

    def createEvaluationInstance(self, tup: Tuple[slice, int]) -> EvaluationClass:
        return self.evaluationClass(self.U, self.p, tup)

    def __getitem__(self, tup: slice) -> EvaluationClass:
        return self.createEvaluationInstance(tup)

    def __call__(self, u: np.ndarray) -> np.ndarray:
        return self[:, self.p] (u)
        

class GeneralBaseFunction(BaseFunction):

    def __init__(self, U: Iterable[float]):
        super().__init__(U)
        self.A = np.eye(self.n)

    def createEvaluationInstance(self, tup: Tuple[slice, int]) -> EvaluationClass:
        return self.evaluationClass(self.U, self.p, tup, self.A)

    @property
    def A(self) -> np.ndarray:
        return self._A

    @property
    def p(self) -> int:
        return self._p

    @A.setter
    def A(self, value: np.ndarray) -> None:
        self._A = value

    @p.setter
    def p(self, value: int) -> None:
        if value < 0:
            raise ValueError("Cannot set p = ", value)
        self._p = int(value)

    def derivate(self):
        U = list(self.U)
        newinstance = self.__class__(U)
        newinstance.p = self.p - 1
        avals = np.zeros(self.n)
        for i in range(self.n):
            diff = self.U[i+self.p] - self.U[i]
            if diff != 0:
                avals[i] = self.p/diff
        newA = np.diag(avals)
        for i in range(self.n-1):
            newA[i, i+1] = -avals[i+1]
        newinstance.A = self.A @ newA
        return newinstance


class SplineBaseFunction(GeneralBaseFunction):

    def __doc__(self):
        """
        This function is recursively determined like

        N_{i, 0}(u) = { 1   if  U[i] <= u < U[i+1]
                      { 0   else

                          u - U[i]
        N_{i, j}(u) = --------------- * N_{i, j-1}(u)
                       U[i+j] - U[i]
                            U[i+j+1] - u
                      + ------------------- * N_{i+1, j-1}(u)
                         U[i+j+1] - U[i+1]

        As consequence, we have that

        N_{i, j}(u) = 0   if  ( u not in [U[i], U[i+j+1]] )

        """
    
    def __init__(self, U: Iterable[float]):
        super().__init__(U)

    @property
    def evaluationClass(self) -> type[EvaluationClass]:
        return SplineEvaluationClass

class RationalBaseFunction(GeneralBaseFunction):
    def __init__(self, U: Iterable[float]):
        super().__init__(U)
        self.w = np.ones(self.n)

    @property
    def evaluationClass(self) -> type[EvaluationClass]:
        return RationalEvaluationClass

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value: Iterable[float]):
        for v in value:
            v = float(v)
            if v < 0:
                raise ValueError("The weights must be positive")
        self._w = value
    


class SplineEvaluationClass(EvaluationClass):

    def __init__(self, U: Iterable[float], p: int, tup: Any, A: Optional[np.ndarray]=None):
        super().__init__(U, p, tup, A)
        
    @property
    def f(self):
        return N


class RationalEvaluationClass(EvaluationClass):
    def __init__(self, U: Iterable[float], w: Iterable[float], p: int, tup: Any, A: Optional[np.ndarray]=None):
        super().__init__(U, p, tup, A)
        self.w = w
        
    @property
    def f(self):
        raise NotImplementedError("TO DO")
        return R

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value: Iterable[float]):
        value = np.array(value)
        if value.ndim != 1:
            raise ValueError("to set the weights, it must be a vector")
        if len(value) != self.U.n:
            raise ValueError("The size of weights must be the same as number of functions")
        self._w = value

    