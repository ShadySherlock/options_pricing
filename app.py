import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import norm
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Options Pricing Comparison",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.main {
    background-color: #f8f9fa;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# BLACK-SCHOLES
# ============================================================

def black_scholes_call(S, K, r, sigma, T):

    if T <= 0:
        payoff = max(S - K, 0)
        return payoff, 1.0 if S > K else 0.0, 0.0, 0.0, 0.0

    d1 = (
        np.log(S / K)
        + (r + 0.5 * sigma ** 2) * T
    ) / (sigma * np.sqrt(T))

    d2 = d1 - sigma * np.sqrt(T)

    price = (
        S * norm.cdf(d1)
        - K * np.exp(-r * T) * norm.cdf(d2)
    )

    delta = norm.cdf(d1)

    gamma = (
        norm.pdf(d1)
        / (S * sigma * np.sqrt(T))
    )

    vega = (
        S * norm.pdf(d1) * np.sqrt(T)
        / 100
    )

    theta = (
        -S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
        - r * K * np.exp(-r * T) * norm.cdf(d2)
    ) / 365

    return price, delta, gamma, vega, theta


# ============================================================
# MONTE CARLO
# ============================================================

def monte_carlo_call(
    S,
    K,
    r,
    sigma,
    T,
    num_simulations=100000
):

    z = np.random.standard_normal(num_simulations)

    terminal_prices = S * np.exp(
        (r - 0.5 * sigma ** 2) * T
        + sigma * np.sqrt(T) * z
    )

    payoffs = np.maximum(terminal_prices - K, 0)

    price = np.exp(-r * T) * np.mean(payoffs)

    return price, terminal_prices


# ============================================================
# MONTE CARLO PATHS
# ============================================================

def generate_mc_paths(
    S,
    r,
    sigma,
    T,
    path_count=30,
    step_count=252
):

    dt = T / step_count

    z = np.random.standard_normal(
        (path_count, step_count)
    )

    increments = (
        (r - 0.5 * sigma ** 2) * dt
        + sigma * np.sqrt(dt) * z
    )

    paths = np.zeros(
        (path_count, step_count + 1)
    )

    paths[:, 0] = S

    paths[:, 1:] = S * np.exp(
        np.cumsum(increments, axis=1)
    )

    times = np.linspace(
        0,
        T,
        step_count + 1
    )

    mean_path = np.mean(paths, axis=0)

    return times, paths, mean_path


# ============================================================
# HEADER
# ============================================================

st.title(
    "📊 European Call Pricing Lab"
)

st.markdown("""
### Black-Scholes vs Monte Carlo

Compare two major option-pricing approaches using
interactive simulations, sensitivity analysis, Monte Carlo
convergence and statistical analysis.
""")


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Option Configuration")

st.sidebar.subheader("Underlying")

S = st.sidebar.number_input(
    "Spot Price ($)",
    min_value=1.0,
    max_value=100000.0,
    value=100.0,
    step=0.5
)

K = st.sidebar.number_input(
    "Strike Price ($)",
    min_value=1.0,
    max_value=100000.0,
    value=100.0,
    step=0.5
)

st.sidebar.subheader("Model Parameters")

r_percent = st.sidebar.slider(
    "Risk-Free Rate (%)",
    min_value=0.0,
    max_value=15.0,
    value=5.0,
    step=0.1
)

r = r_percent / 100

sigma_percent = st.sidebar.slider(
    "Volatility (%)",
    min_value=1.0,
    max_value=150.0,
    value=20.0,
    step=1.0
)

sigma = sigma_percent / 100

T = st.sidebar.slider(
    "Time to Expiry (Years)",
    min_value=0.05,
    max_value=5.0,
    value=1.0,
    step=0.05
)

st.sidebar.subheader("Monte Carlo")

num_sims = st.sidebar.slider(
    "Simulations",
    min_value=10000,
    max_value=500000,
    value=100000,
    step=10000
)

actual_spot = st.sidebar.number_input(
    "Actual Spot at Expiry ($)",
    min_value=0.0,
    max_value=100000.0,
    value=110.0,
    step=0.5
)


# ============================================================
# CALCULATIONS
# ============================================================

bs_price, delta, gamma, vega, theta = black_scholes_call(
    S,
    K,
    r,
    sigma,
    T
)

mc_price, simulated_prices = monte_carlo_call(
    S,
    K,
    r,
    sigma,
    T,
    num_sims
)

actual_payoff = max(
    actual_spot - K,
    0
)

bs_error = abs(
    bs_price - actual_payoff
)

mc_error = abs(
    mc_price - actual_payoff
)

if actual_payoff > 0:
    bs_error_pct = (
        bs_error / actual_payoff * 100
    )

    mc_error_pct = (
        mc_error / actual_payoff * 100
    )
else:
    bs_error_pct = 0
    mc_error_pct = 0


# ============================================================
# TOP METRICS
# ============================================================

st.subheader("📈 Pricing Results")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Black-Scholes",
        f"${bs_price:.2f}"
    )

with col2:
    st.metric(
        "Monte Carlo",
        f"${mc_price:.2f}"
    )

with col3:
    st.metric(
        "Actual Payoff",
        f"${actual_payoff:.2f}"
    )

with col4:
    st.metric(
        "BS vs MC Difference",
        f"${abs(bs_price - mc_price):.2f}"
    )


# ============================================================
# GREEKS
# ============================================================

st.subheader("Greek Sensitivities")

g1, g2, g3, g4 = st.columns(4)

with g1:
    st.metric(
        "Delta (Δ)",
        f"{delta:.4f}"
    )

with g2:
    st.metric(
        "Gamma (Γ)",
        f"{gamma:.6f}"
    )

with g3:
    st.metric(
        "Vega (ν)",
        f"{vega:.4f}"
    )

with g4:
    st.metric(
        "Theta (Θ)",
        f"{theta:.4f}"
    )


st.markdown("---")


# ============================================================
# CHART 1
# MC TERMINAL DISTRIBUTION
# ============================================================

st.subheader(
    "Chart 1: Monte Carlo Terminal Price Distribution"
)

fig1 = go.Figure()

fig1.add_trace(
    go.Histogram(
        x=simulated_prices,
        nbinsx=70,
        name="Simulated Prices",
        opacity=0.75
    )
)

fig1.add_shape(
    type="line",
    x0=float(K),
    x1=float(K),
    y0=0,
    y1=1,
    xref="x",
    yref="paper",
    line=dict(
        dash="dash",
        color="orange",
        width=2
    )
)

fig1.add_annotation(
    x=float(K),
    y=1,
    xref="x",
    yref="paper",
    text=f"Strike: ${K:.2f}",
    showarrow=False,
    yshift=10
)

fig1.add_shape(
    type="line",
    x0=float(actual_spot),
    x1=float(actual_spot),
    y0=0,
    y1=1,
    xref="x",
    yref="paper",
    line=dict(
        dash="dot",
        color="red",
        width=2
    )
)

fig1.add_annotation(
    x=float(actual_spot),
    y=1,
    xref="x",
    yref="paper",
    text=f"Actual Spot: ${actual_spot:.2f}",
    showarrow=False,
    yshift=30
)

fig1.update_layout(
    title="Monte Carlo Simulated Terminal Prices",
    xaxis_title="Final Stock Price ($)",
    yaxis_title="Frequency",
    height=550,
    template="plotly_white"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)


# ============================================================
# CHART 2
# SPOT PRICE SENSITIVITY
# ============================================================

st.subheader(
    "Chart 2: Option Price Sensitivity Across Spot Prices"
)

spot_range = np.linspace(
    max(0.01, K * 0.5),
    K * 1.5,
    60
)

bs_prices = []
mc_prices = []

for spot in spot_range:

    bs_p, _, _, _, _ = black_scholes_call(
        spot,
        K,
        r,
        sigma,
        T
    )

    mc_p, _ = monte_carlo_call(
        spot,
        K,
        r,
        sigma,
        T,
        num_simulations=20000
    )

    bs_prices.append(bs_p)
    mc_prices.append(mc_p)

intrinsic_prices = np.maximum(
    spot_range - K,
    0
)

fig2 = go.Figure()

fig2.add_trace(
    go.Scatter(
        x=spot_range,
        y=bs_prices,
        mode="lines",
        name="Black-Scholes",
        line=dict(width=3)
    )
)

fig2.add_trace(
    go.Scatter(
        x=spot_range,
        y=mc_prices,
        mode="lines",
        name="Monte Carlo",
        line=dict(width=3)
    )
)

fig2.add_trace(
    go.Scatter(
        x=spot_range,
        y=intrinsic_prices,
        mode="lines",
        name="Intrinsic Value",
        line=dict(
            width=2,
            dash="dash"
        )
    )
)

fig2.add_shape(
    type="line",
    x0=float(S),
    x1=float(S),
    y0=0,
    y1=1,
    xref="x",
    yref="paper",
    line=dict(
        dash="dot",
        width=2
    )
)

fig2.add_annotation(
    x=float(S),
    y=1,
    xref="x",
    yref="paper",
    text=f"Current Spot: ${S:.2f}",
    showarrow=False,
    yshift=10
)

fig2.update_layout(
    title="European Call Price vs Spot Price",
    xaxis_title="Spot Price ($)",
    yaxis_title="Option Price ($)",
    height=550,
    hovermode="x unified",
    template="plotly_white"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# ============================================================
# CHART 3
# MONTE CARLO CONVERGENCE
# ============================================================

st.subheader(
    "Chart 3: Monte Carlo Convergence"
)

convergence_points = [
    1000,
    5000,
    10000,
    25000,
    50000,
    100000,
    250000,
    500000
]

convergence_prices = []

for count in convergence_points:

    price, _ = monte_carlo_call(
        S,
        K,
        r,
        sigma,
        T,
        num_simulations=count
    )

    convergence_prices.append(price)

fig3 = go.Figure()

fig3.add_trace(
    go.Scatter(
        x=convergence_points,
        y=convergence_prices,
        mode="lines+markers",
        name="Monte Carlo"
    )
)

fig3.add_shape(
    type="line",
    x0=min(convergence_points),
    x1=max(convergence_points),
    y0=float(bs_price),
    y1=float(bs_price),
    line=dict(
        dash="dash",
        width=2
    )
)

fig3.add_annotation(
    x=max(convergence_points),
    y=float(bs_price),
    text=f"BS Price: ${bs_price:.2f}",
    showarrow=False,
    xshift=-50,
    yshift=10
)

fig3.update_xaxes(
    type="log"
)

fig3.update_layout(
    title="Monte Carlo Price Convergence",
    xaxis_title="Number of Simulations",
    yaxis_title="Option Price ($)",
    height=550,
    template="plotly_white"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)


# ============================================================
# CHART 4
# MC ERROR
# ============================================================

st.subheader(
    "Chart 4: Monte Carlo Error vs Black-Scholes"
)

mc_errors = [
    abs(price - bs_price)
    for price in convergence_prices
]

fig4 = go.Figure()

fig4.add_trace(
    go.Scatter(
        x=convergence_points,
        y=mc_errors,
        mode="lines+markers",
        name="MC Absolute Error"
    )
)

fig4.update_xaxes(
    type="log"
)

fig4.update_layout(
    title="Monte Carlo Absolute Error",
    xaxis_title="Number of Simulations",
    yaxis_title="Absolute Error ($)",
    height=500,
    template="plotly_white"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)


# ============================================================
# CHART 5
# SAMPLE MONTE CARLO PATHS
# ============================================================

st.subheader(
    "Chart 5: Monte Carlo Stock Price Paths"
)

times, paths, mean_path = generate_mc_paths(
    S,
    r,
    sigma,
    T,
    path_count=30,
    step_count=252
)

fig5 = go.Figure()

for i in range(paths.shape[0]):

    fig5.add_trace(
        go.Scatter(
            x=times,
            y=paths[i],
            mode="lines",
            line=dict(
                width=1
            ),
            opacity=0.25,
            showlegend=False
        )
    )

fig5.add_trace(
    go.Scatter(
        x=times,
        y=mean_path,
        mode="lines",
        name="Mean Path",
        line=dict(
            width=4
        )
    )
)

fig5.add_shape(
    type="line",
    x0=0,
    x1=T,
    y0=float(K),
    y1=float(K),
    line=dict(
        dash="dash",
        width=2
    )
)

fig5.add_annotation(
    x=T,
    y=float(K),
    text=f"Strike: ${K:.2f}",
    showarrow=False,
    xshift=-60,
    yshift=10
)

fig5.update_layout(
    title="Geometric Brownian Motion Price Paths",
    xaxis_title="Time (Years)",
    yaxis_title="Stock Price ($)",
    height=550,
    template="plotly_white"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)


# ============================================================
# CHART 6
# MODEL COMPARISON
# ============================================================

st.subheader(
    "Chart 6: Black-Scholes vs Monte Carlo vs Actual Payoff"
)

comparison_models = [
    "Black-Scholes",
    "Monte Carlo",
    "Actual Payoff"
]

comparison_values = [
    bs_price,
    mc_price,
    actual_payoff
]

fig6 = go.Figure()

fig6.add_trace(
    go.Bar(
        x=comparison_models,
        y=comparison_values,
        text=[
            f"${value:.2f}"
            for value in comparison_values
        ],
        textposition="outside"
    )
)

fig6.update_layout(
    title="European Call Price Comparison",
    xaxis_title="Model",
    yaxis_title="Value ($)",
    height=500,
    template="plotly_white"
)

st.plotly_chart(
    fig6,
    use_container_width=True
)


# ============================================================
# STATISTICAL ANALYSIS
# ============================================================

st.subheader(
    "📊 Detailed Statistical Analysis"
)

stats = pd.DataFrame({
    "Metric": [
        "Spot Price",
        "Strike Price",
        "Time to Expiry",
        "Risk-Free Rate",
        "Volatility",
        "Mean MC Terminal Price",
        "Std Dev Terminal Price",
        "Minimum Terminal Price",
        "Maximum Terminal Price",
        "Black-Scholes Price",
        "Monte Carlo Price",
        "Actual Payoff",
        "BS Error",
        "MC Error",
        "BS Error (%)",
        "MC Error (%)"
    ],

    "Value": [
        f"${S:.2f}",
        f"${K:.2f}",
        f"{T:.2f} years",
        f"{r_percent:.2f}%",
        f"{sigma_percent:.2f}%",
        f"${np.mean(simulated_prices):.2f}",
        f"${np.std(simulated_prices):.2f}",
        f"${np.min(simulated_prices):.2f}",
        f"${np.max(simulated_prices):.2f}",
        f"${bs_price:.2f}",
        f"${mc_price:.2f}",
        f"${actual_payoff:.2f}",
        f"${bs_error:.2f}",
        f"${mc_error:.2f}",
        f"{bs_error_pct:.2f}%",
        f"{mc_error_pct:.2f}%"
    ]
})

st.dataframe(
    stats,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# CONVERGENCE TABLE
# ============================================================

st.subheader(
    "Monte Carlo Convergence Table"
)

convergence_df = pd.DataFrame({
    "Simulations": convergence_points,
    "MC Price": [
        f"${price:.4f}"
        for price in convergence_prices
    ],
    "Error vs BS": [
        f"${error:.4f}"
        for error in mc_errors
    ]
})

st.dataframe(
    convergence_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# INSIGHTS
# ============================================================

st.markdown("---")

st.subheader("🎯 Model Insights")

i1, i2, i3 = st.columns(3)

with i1:

    if bs_error < mc_error:

        st.success(
            f"Black-Scholes is closer to the actual payoff "
            f"by ${mc_error - bs_error:.2f}."
        )

    else:

        st.success(
            f"Monte Carlo is closer to the actual payoff "
            f"by ${bs_error - mc_error:.2f}."
        )


with i2:

    moneyness = (
        (S - K) / K * 100
    )

    if moneyness > 0:

        st.info(
            f"Call is {moneyness:.1f}% "
            f"In-The-Money."
        )

    elif moneyness < 0:

        st.info(
            f"Call is {abs(moneyness):.1f}% "
            f"Out-of-The-Money."
        )

    else:

        st.info(
            "Call is At-The-Money."
        )


with i3:

    model_difference = abs(
        bs_price - mc_price
    )

    st.info(
        f"BS vs MC difference: "
        f"${model_difference:.2f}"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown("""
<div style='text-align:center; color:gray; padding:20px;'>

<b>European Call Pricing Lab</b>

<br><br>

Black-Scholes Formula • Monte Carlo Simulation •
Greeks • Sensitivity • Convergence • GBM

</div>
""", unsafe_allow_html=True)
