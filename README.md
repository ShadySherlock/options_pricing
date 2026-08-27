# Options Pricing Comparison Tool

📊 An interactive Streamlit application comparing **Black-Scholes** and **Monte Carlo** models for European call option pricing using real historical stock data.

## Overview

This project validates options pricing theory by comparing two fundamental pricing models against real market outcomes:

- **Black-Scholes**: Closed-form analytical solution
- **Monte Carlo**: Numerical simulation using Geometric Brownian Motion
- **Real Data**: Actual option payoffs from 6-month expired contracts

## Features

### 🎯 Core Functionality
- **5 Real Stock Options**: AAPL, MSFT, TSLA, NVDA, SPY (June-December 2024)
- **Interactive Parameters**: Adjust spot, strike, rate, volatility, and simulation count
- **Real-Time Calculations**: Instant price and accuracy updates
- **Greek Sensitivities**: Delta, Gamma, Vega, Theta, Rho

### 📈 Visualizations
1. **MC Distribution Chart** - Histogram of simulated final prices
2. **Price Comparison** - Bar chart of BS vs MC vs Actual
3. **Sensitivity Analysis** - Price curves across spot prices
4. **Convergence Analysis** - MC stability with increasing simulations
5. **Error Analysis** - Accuracy metrics vs actual payoff
6. **GBM Paths** - 300+ individual Monte Carlo trajectories

### 📊 Analytics
- Comprehensive statistical tables
- Model accuracy metrics
- Convergence analysis (1k → 100k simulations)
- Real outcome comparison

## Project Structure

```
options-pricing/
├── app.py              # Main Streamlit application
├── models.py           # Black-Scholes & Monte Carlo functions
├── config.py           # Stock options data & configuration
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## Installation

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/options-pricing.git
cd options-pricing
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

### Docker Setup (Optional)

```bash
docker build -t options-pricing .
docker run -p 8501:8501 options-pricing
```

## Streamlit Cloud Deployment

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Options pricing comparison tool"
git branch -M main
git remote add origin https://github.com/yourusername/options-pricing.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Click "New app"
3. Select your GitHub repository
4. Choose `app.py` as the main file
5. Click "Deploy"

✅ **Live in seconds!**

## Usage

### Selecting Stock Options
Choose from 5 pre-loaded options with real market data:
- **AAPL**: High volatility (24%), strong performance
- **MSFT**: Moderate volatility (18%), stable
- **TSLA**: High volatility (38%), explosive growth
- **NVDA**: High volatility (32%), strong momentum
- **SPY**: Low volatility (16%), market benchmark

### Adjusting Parameters
Use sidebar sliders to modify:
- **Spot Price**: Current stock price
- **Strike Price**: Option strike level
- **Risk-Free Rate**: Annual interest rate (0-10%)
- **Volatility**: Annual volatility (5-100%)
- **MC Simulations**: Path count (10k-500k)

### Interpreting Results

#### Metrics
- **Black-Scholes**: Theoretical price assuming lognormal distribution
- **Monte Carlo**: Numerical approximation via random path simulation
- **Actual Payoff**: Real option value at expiration

#### Greeks (Sensitivities)
- **Delta (Δ)**: Option price change per $1 spot move
- **Gamma (Γ)**: Delta's sensitivity to spot changes
- **Vega (ν)**: Volatility sensitivity (×1% change)
- **Theta (Θ)**: Daily time decay
- **Rho (ρ)**: Interest rate sensitivity

#### Convergence
- MC price stabilizes as simulations increase
- Fewer sims → noisy estimates
- More sims → closer to theoretical value (more time)

## Real Data Details

### Sample Options
All options expired 6 months after inception (Jun 1 → Dec 20, 2024):

| Stock | Spot (Inception) | Strike | Spot (Expiry) | Payoff | Return |
|-------|------------------|--------|---------------|--------|--------|
| AAPL  | $192.35          | $200   | $251.73       | $51.73 | +26.9% |
| MSFT  | $415.50          | $430   | $426.04       | $0.00  | +2.5%  |
| TSLA  | $187.50          | $200   | $262.68       | $62.68 | +39.8% |
| NVDA  | $120.85          | $130   | $140.76       | $10.76 | +16.5% |
| SPY   | $543.50          | $560   | $600.92       | $40.92 | +10.5% |

## Mathematical Background

### Black-Scholes Formula
```
C = S * N(d1) - K * e^(-rT) * N(d2)

where:
d1 = [ln(S/K) + (r + σ²/2)T] / (σ√T)
d2 = d1 - σ√T
N(x) = Cumulative standard normal CDF
```

### Monte Carlo (Geometric Brownian Motion)
```
S_T = S * exp((r - σ²/2)*T + σ*√T*Z)
Payoff = max(S_T - K, 0)
Price = e^(-rT) * mean(Payoffs)

where Z ~ N(0,1)
```

## Model Accuracy

Expected error ranges:
- **Black-Scholes**: 0-5% for normal volatility scenarios
- **Monte Carlo**: 0-2% with 100k+ simulations
- **Both models**: Converge to actual payoff with perfect parameters

Errors occur due to:
1. Volatility estimation uncertainty
2. Constant volatility assumption (vs. stochastic volatility)
3. No transaction costs or dividends
4. European-style exercise only

## Technology Stack

- **Streamlit**: Interactive web framework
- **Python 3.9+**: Core language
- **NumPy**: Fast numerical computation
- **Pandas**: Data manipulation
- **Plotly**: Interactive visualizations
- **SciPy**: Statistical distributions

## Performance

- **Black-Scholes**: < 1ms (analytical)
- **Monte Carlo (100k)**: 50-200ms (depends on params)
- **Chart generation**: 100-300ms

## Troubleshooting

### App runs slow
- Reduce MC simulations (start at 10k)
- Use smaller sensitivity analysis range
- Check internet connection

### Deployment fails
- Verify all files uploaded to GitHub
- Check `requirements.txt` is in root
- Ensure Python 3.9+ compatibility

### Calculations seem off
- Verify volatility input (as %)
- Check risk-free rate (5% = 0.05)
- Confirm time to expiry calculation


## Future Enhancements

- **Binomial Model**: Add binomial tree pricing
- **Stochastic Volatility**: SABR or Heston model
- **Machine Learning**: Price prediction models
- **Risk Management**: VaR, CVaR calculations
- **Backtesting**: Test models across historical data



**Live Demo**: [https://optionspricing-qn5yv4fdk7o4xhkwinevfc.streamlit.app/]


