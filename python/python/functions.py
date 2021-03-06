# -*- coding: utf-8 -*-
import numpy as np

"""
List of function used by the algorithm
"""

def sigmoide(t, args):
    """
    Sigmoide function

    Q(t;Qmax,ts, tau) = Qmax / (1+ exp((-t-ts)/tau))

    Parameters
    ----------
    t: int or float
        Time.
    args : List
        Arguments of the function.

    Returns
    -------
    Q(t;args).

    """
    Qmax, ts, tau = args
    return Qmax/(1+np.e**(-(t-ts)/tau))

def grad_sigmoide(t, args):
    """
    Sigmoide function

    dQ(t;Qmax,ts, tau)/dQmax = 1 / (1+ exp((-t-ts)/tau))

    dQ(t;Qmax,ts, tau)/dt* = - (1 / tau) * Qmax / (1+ exp(-(t-ts)/tau))^2

    dQ(t;Qmax,ts, tau)/dtau = (t-ts)/tau * Qmax / (1+ exp(-(t-ts)/tau))

    Parameters
    ----------
    t: int or float
        Time.
    args : List
        Arguments of the function.

    Returns
    -------
    grad Q(t;args).

    """
    Qmax, ts, tau = args

    dQdQmax = 1/(1+np.e**(-(t-ts)/tau)) 
    
    temp = -np.e**(-(t-ts)/tau) * Qmax/(1+np.e**(-(t-ts)/tau))**2

    dQdts = temp * (1/tau)

    dQdtau = (-(t-ts)/tau**2)*np.e**(-(t-ts)/tau) * Qmax/(1+np.e**(-(t-ts)/tau))**2 # ou ((t-ts)/tau) * Qmax/(1+np.e**(-(t-ts)/tau))**2

    return np.array([dQdQmax, dQdts, dQdtau]).transpose()


    # Qmax, tmid, tau = args
    
    # r = -(t-tmid)/tau
    # d_Qmax = 1/(1+np.e**(r))
    # d_tmid = (-Qmax/tau)*np.e**(r)/(1+np.e**(r)**2)
    # d_tau = (-Qmax/(tau**2))*(np.e**(r)*(t-tmid))/((1+np.e**(r))**2)
    
    # return np.array([d_Qmax, d_tmid, d_tau])

# criterion
def least_square(data,t_start, Dt, func, args): 
    """
    J(arg) = Dt || func(args) - data ||^2

    Parameters
    ----------
    Dt : float
        Time step.
    func : Function
        Function of modelisation.
    args : List
        Arguments of the function.

    Returns
    -------
    J(args).
    """
    
    T = np.arange(t_start, t_start+Dt*len(data), Dt)

    J = Dt * np.linalg.norm(data-func(t=T,args=args))**2
    
    # score = 0

    # for k, d in enumerate(data):
    #     score += Dt*(d-func(T[k],args))**2
        
    # J = score
    
    return J

def grad_least_square(data, t_start, Dt, func, grad_func, args):
    """
    
    grad J(arg) = 2*Dt || data - func(t,args)|| * grad func(t,args)

    """
    T = np.arange(t_start, t_start+Dt*len(data), Dt)
    grad_J = np.zeros(3)

    for k,t in enumerate(T):
        grad_J += 2*Dt*(data[k]-func(t,args))*grad_func(t,args)

    # grad_theta = np.zeros(3)

    # for x, y in enumerate(data):
    #     grad_theta += 2*Dt*grad_func(x, args)*(y-func(x, args)) # grad_func est ici le gradient de la courbe d'hubert

    # grad_J = grad_theta

    return -grad_J

def scale_matrix(t_start, t_end, grad_func, args):
    """
    Hess(func) ~= (J^t . J)^-1
    """
    jac = np.zeros((t_end-t_start,3))
    
    T = np.arange(t_start, t_end, 1)
    
    for k, t in enumerate(T):
        jac[k] = grad_func(t,args)
    
    B = 2*jac.transpose().dot(jac)
    
    return np.linalg.inv(B)

def noised_sigmoide(noise, Qmax=100, ts=30, tau=6, t_start=0, t_end=60):

    t = np.arange(t_start, t_end, 1)
    sig = sigmoide(t, (Qmax, ts, tau))

    noised_sig = [sig[0]]

    for k in range(len(sig)-1):
        rd = np.random.normal(noised_sig[k] + sig[k+1]-sig[k] ,noise*(sig[k+1]-sig[k])/5)

        clip_rd = np.clip(rd,noised_sig[k],np.inf)
        noised_sig.append(clip_rd)

    return noised_sig

