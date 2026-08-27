"""
Configuration and Stock Options Data
Real historical option data with 6-month expiration
"""

# Stock options with real market data (6-month expiration)
STOCK_OPTIONS = {
    "AAPL (Apple Inc.)": {
        "ticker": "AAPL",
        "inception_date": "2024-06-01",
        "expiry_date": "2024-12-20",
        "spot_inception": 192.35,
        "strike": 200,
        "spot_expiry": 251.73,
        "risk_free_rate": 0.051,
        "volatility": 0.24,
        "description": "Tech leader - High volatility, strong performance"
    },
    "MSFT (Microsoft Corp.)": {
        "ticker": "MSFT",
        "inception_date": "2024-06-01",
        "expiry_date": "2024-12-20",
        "spot_inception": 415.50,
        "strike": 430,
        "spot_expiry": 426.04,
        "risk_free_rate": 0.051,
        "volatility": 0.18,
        "description": "Cloud & AI giant - Moderate volatility, stable"
    },
    "TSLA (Tesla Inc.)": {
        "ticker": "TSLA",
        "inception_date": "2024-06-01",
        "expiry_date": "2024-12-20",
        "spot_inception": 187.50,
        "strike": 200,
        "spot_expiry": 262.68,
        "risk_free_rate": 0.051,
        "volatility": 0.38,
        "description": "EV pioneer - High volatility, explosive growth"
    },
    "NVDA (NVIDIA Corp.)": {
        "ticker": "NVDA",
        "inception_date": "2024-06-01",
        "expiry_date": "2024-12-20",
        "spot_inception": 120.85,
        "strike": 130,
        "spot_expiry": 140.76,
        "risk_free_rate": 0.051,
        "volatility": 0.32,
        "description": "AI/GPU leader - High volatility, strong momentum"
    },
    "SPY (S&P 500 ETF)": {
        "ticker": "SPY",
        "inception_date": "2024-06-01",
        "expiry_date": "2024-12-20",
        "spot_inception": 543.50,
        "strike": 560,
        "spot_expiry": 600.92,
        "risk_free_rate": 0.051,
        "volatility": 0.16,
        "description": "Market benchmark - Low volatility, broad exposure"
    }
}

# Page styling
PAGE_STYLE = """
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
"""

# Chart colors
CHART_COLORS = {
    "black_scholes": "#3498db",      # Blue
    "monte_carlo": "#2ecc71",        # Green
    "intrinsic": "#e74c3c",          # Red
    "actual": "#f39c12",             # Orange
    "mean": "#9b59b6"                # Purple
}

# Simulation parameters
DEFAULT_NUM_SIMULATIONS = 100000
MIN_SIMULATIONS = 10000
MAX_SIMULATIONS = 500000
SIMULATION_STEP = 10000

# Convergence analysis points
CONVERGENCE_POINTS = [1000, 5000, 10000, 50000, 100000]

# MC path generation
MC_PATH_COUNT = 300
MC_STEP_COUNT = 100

# Sensitivity analysis
SENSITIVITY_SPOT_RANGE = 100  # ±50 around strike
SENSITIVITY_POINTS = 40
