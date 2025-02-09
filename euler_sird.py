import numpy as np

def euler_sird(params, CI, dt, T):
    """
    Résolution numérique du modèle SIRD par la méthode d'Euler
    
    Paramètres:
    params : liste [beta, gamma, micro] - paramètres du modèle
    CI : liste [S0, I0, R0, D0] - conditions initiales
    dt : float - pas de temps
    T : float - temps total de simulation
    
    Retourne:
    t : array - points temporels
    S : array - susceptibles
    I : array - infectés
    R : array - rétablis
    D : array - décédés
    """
    beta, gamma, micro = params
    S0, I0, R0, D0 = CI
    
    # Nombre de points temporels
    n = int(T/dt)
    
    # Initialisation des tableaux
    t = np.linspace(0, T, n)
    S = np.zeros(n)
    I = np.zeros(n)
    R = np.zeros(n)
    D = np.zeros(n)
    
    # Conditions initiales
    S[0] = S0
    I[0] = I0
    R[0] = R0
    D[0] = D0
    
    # Méthode d'Euler
    for j in range(n-1):
        S[j+1] = S[j] - dt*beta*S[j]*I[j]
        I[j+1] = I[j] + dt*(beta*S[j]*I[j] - gamma*I[j] - micro*I[j])
        R[j+1] = R[j] + dt*gamma*I[j]
        D[j+1] = D[j] + dt*micro*I[j]
    
    return t, S, I, R, D 