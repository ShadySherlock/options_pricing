"""
Options Pricing Models
Black-Scholes and Monte Carlo implementations
"""

import numpy as np
import streamlit as st
from scipy.stats import norm


@st.cache_data
def black_scholes_call(S, K, r, sigma, T):
    """
    Calculate European call option price using Black-Scholes formula
    
    Args:
        S: Current spot price
        K: Strike price
        r: Risk-free rate (annual)
        sigma: Volatility (annual, as decimal)
        T: Time to expiry (in years)
    
    Returns:
        Tuple: (call_price, delta, gamma, vega, theta)
    """
    if T <= 0 or sigma <= 0:
        return 0, 0, 0, 0, 0
    
    # Calculate d1 and d2
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # Black-Scholes formula for call option
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    
    # Calculate Greeks
    delta = norm.cdf(d1)
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T) / 100
    theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - 
             r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
    
    return call_price, delta, gamma, vega, theta


@st.cache_data
def monte_carlo_call(S, K, r, sigma, T, num_simulations=100000):
    """
    Calculate European call option price using Monte Carlo simulation
    
    Simulates price paths using Geometric Brownian Motion:
    S_T = S * exp((r - σ²/2)*T + σ*√T*Z)
    where Z ~ N(0,1)
    
    Args:
        S: Current spot price
        K: Strike price
        r: Risk-free rate (annual)
        sigma: Volatility (annual, as decimal)
        T: Time to expiry (in years)
        num_simulations: Number of Monte Carlo paths
    
    Returns:
        Tuple: (call_price, simulated_final_prices)
    """
    if T <= 0 or sigma <= 0:
        return 0, np.array([S])
    
    np.random.seed(42)
    
    # Generate random normal variables
    Z = np.random.standard_normal(num_simulations)
    
    # Simulate final spot prices using Geometric Brownian Motion
    S_T = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    
    # Calculate payoffs at expiry (max(S_T - K, 0))
    payoffs = np.maximum(S_T - K, 0)
    
    # Discount back to present and take average
    call_price = np.exp(-r * T) * np.mean(payoffs)
    
    return call_price, S_T


def generate_mc_paths(S, K, r, sigma, T, num_paths=300, num_steps=100):
    """
    Generate Monte Carlo price paths for visualization
    
    Args:
        S: Current spot price
        K: Strike price
        r: Risk-free rate
        sigma: Volatility
        T: Time to expiry
        num_paths: Number of paths to generate
        num_steps: Number of time steps per path
    
    Returns:
        Tuple: (times, paths, mean_path)
    """
    dt = T / num_steps
    times = np.linspace(0, T, num_steps)
    
    np.random.seed(42)
    Z = np.random.standard_normal((num_paths, num_steps - 1))
    
    paths = np.zeros((num_paths, num_steps))
    paths[:, 0] = S
    
    for i in range(1, num_steps):
        paths[:, i] = paths[:, i-1] * np.exp((r - 0.5 * sigma**2) * dt + 
                                              sigma * np.sqrt(dt) * Z[:, i-1])
    
    mean_path = np.mean(paths, axis=0)
    
    return times, paths, mean_path
