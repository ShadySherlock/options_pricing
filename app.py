"""
Options Pricing Comparison Tool
Interactive Streamlit application for Black-Scholes vs Monte Carlo comparison
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import warnings

from models import black_scholes_call, monte_carlo_call, generate_mc_paths
from config import STOCK_OPTIONS, CHART_COLORS, CONVERGENCE_POINTS, MC_PATH_COUNT, MC_STEP_COUNT, SENSITIVITY_POINTS, SENSITIVITY_SPOT_RANGE

warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIG
# ============================================================================

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
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================

st.title("📊 Options Pricing Comparison: Black-Scholes vs Monte Carlo")
st.markdown("""
Compare theoretical pricing models against real market outcomes. 
Analyze European call options with real historical stock data.
""")

# ============================================================================
# SIDEBAR - USER INPUT
# ============================================================================

st.sidebar.header("⚙️ Configuration")

selected_stock = st.sidebar.selectbox(
    "Select Stock Option",
    list(STOCK_OPTIONS.keys()),
    help="Choose from 5 real stock options with 6-month expiration"
)

stock_data = STOCK_OPTIONS[selected_stock]

st.sidebar.markdown(f"**{stock_data['description']}**")
st.sidebar.markdown("---")
st.sidebar.subheader("Option Parameters")

S = st.sidebar.slider(
    "Spot Price at Inception ($)",
    min_value=stock_data['spot_inception'] * 0.8,
    max_value=stock_data['spot_inception'] * 1.2,
    value=stock_data['spot_inception'],
    step=0.5
)

K = st.sidebar.slider(
    "Strike Price ($)",
    min_value=stock_data['strike'] * 0.8,
    max_value=stock_data['strike'] * 1.2,
    value=stock_data['strike'],
    step=0.5
)

r = st.sidebar.slider(
    "Risk-Free Rate (%)",
    min_value=0.0,
    max_value=10.0,
    value=stock_data['risk_free_rate'] * 100,
    step=0.1
) / 100

sigma = st.sidebar.slider(
    "Volatility (%)",
    min_value=5.0,
    max_value=100.0,
    value=stock_data['volatility'] * 100,
    step=1.0
) / 100

# Calculate time to expiry
inception = pd.to_datetime(stock_data['inception_date'])
expiry = pd.to_datetime(stock_data['expiry_date'])
T = (expiry - inception).days / 365

st.sidebar.markdown("---")
st.sidebar.subheader("Simulation Parameters")

num_sims = st.sidebar.slider(
    "Monte Carlo Simulations",
    min_value=10000,
    max_value=500000,
    value=100000,
    step=10000,
    help="Higher = more accurate but slower"
)

# ============================================================================
# CALCULATIONS
# ============================================================================

# Black-Scholes
bs_price, delta, gamma, vega, theta = black_scholes_call(S, K, r, sigma, T)

# Monte Carlo
mc_price, simulated_prices = monte_carlo_call(S, K, r, sigma, T, num_sims)

# Actual payoff
S_T_actual = stock_data['spot_expiry']
intrinsic_value = max(S_T_actual - K, 0)

# Errors
bs_error = abs(bs_price - intrinsic_value)
mc_error = abs(mc_price - intrinsic_value)
bs_error_pct = (bs_error / intrinsic_value * 100) if intrinsic_value > 0 else 0
mc_error_pct = (mc_error / intrinsic_value * 100) if intrinsic_value > 0 else 0

# ============================================================================
# METRICS DISPLAY
# ============================================================================

st.subheader("📈 Price Comparison")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Black-Scholes",
        f"${bs_price:.2f}",
        f"Error: ${bs_error:.2f} ({bs_error_pct:.1f}%)",
        delta_color="inverse"
    )

with col2:
    st.metric(
        "Monte Carlo",
        f"${mc_price:.2f}",
        f"Error: ${mc_error:.2f} ({mc_error_pct:.1f}%)",
        delta_color="inverse"
    )

with col3:
    st.metric(
        "Actual Payoff",
        f"${intrinsic_value:.2f}",
        f"At expiry: ${S_T_actual:.2f}",
    )

# ============================================================================
# GREEKS DISPLAY
# ============================================================================

st.subheader("Greek Sensitivities (Black-Scholes)")

greek_col1, greek_col2, greek_col3, greek_col4, greek_col5 = st.columns(5)

with greek_col1:
    st.metric("Delta (Δ)", f"{delta:.4f}", "Price sensitivity")

with greek_col2:
    st.metric("Gamma (Γ)", f"{gamma:.6f}", "Delta sensitivity")

with greek_col3:
    st.metric("Vega (ν)", f"{vega:.4f}", "Volatility sensitivity")

with greek_col4:
    st.metric("Theta (Θ)", f"{theta:.4f}", "Time decay/day")

with greek_col5:
    rho = K * T * np.exp(-r * T) * 0.01
    st.metric("Rho (ρ)", f"{rho:.4f}", "Rate sensitivity")

st.markdown("---")

# ============================================================================
# CHART 1: Price Distribution & Comparison
# ============================================================================

st.subheader("Chart 1: MC Distribution & Model Prices")

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    # Histogram of simulated prices
    fig1 = go.Figure()
    fig1.add_trace(go.Histogram(
        x=simulated_prices,
        nbinsx=60,
        name="MC Simulated Prices",
        marker_color='rgba(52, 152, 219, 0.7)',
        opacity=0.7
    ))
    fig1.add_vline(S_T_actual, line_dash="dash", line_color="red", 
                   annotation_text=f"Actual Spot: ${S_T_actual:.2f}",
                   annotation_position="top right")
    fig1.add_vline(K, line_dash="dash", line_color="orange",
                   annotation_text=f"Strike: ${K:.2f}",
                   annotation_position="top left")
    
    fig1.update_layout(
        title="Monte Carlo: Distribution of Simulated Final Prices",
        xaxis_title="Final Spot Price ($)",
        yaxis_title="Frequency",
        hovermode='x unified',
        height=500,
        template="plotly_white"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_chart2:
    # Price comparison bar chart
    prices_df = pd.DataFrame({
        'Model': ['Black-Scholes', 'Monte Carlo', 'Actual Payoff'],
        'Price': [bs_price, mc_price, intrinsic_value],
        'Color': [CHART_COLORS['black_scholes'], CHART_COLORS['monte_carlo'], CHART_COLORS['intrinsic']]
    })
    
    fig2 = go.Figure(data=[
        go.Bar(
            x=prices_df['Model'],
            y=prices_df['Price'],
            marker_color=prices_df['Color'],
            text=[f"${p:.2f}" for p in prices_df['Price']],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Price: $%{y:.2f}<extra></extra>'
        )
    ])
    
    fig2.update_layout(
        title="Price Comparison: Models vs Actual",
        yaxis_title="Option Price ($)",
        hovermode='x unified',
        height=500,
        template="plotly_white",
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ============================================================================
# CHART 2: Sensitivity Analysis
# ============================================================================

st.subheader("Chart 2: Price Sensitivity Across Spot Prices")

spot_range = np.linspace(K - SENSITIVITY_SPOT_RANGE/2, K + SENSITIVITY_SPOT_RANGE/2, SENSITIVITY_POINTS)
bs_prices = []
mc_prices = []

for S_spot in spot_range:
    bs_p, _, _, _, _ = black_scholes_call(S_spot, K, r, sigma, T)
    mc_p, _ = monte_carlo_call(S_spot, K, r, sigma, T, num_simulations=50000)
    bs_prices.append(bs_p)
    mc_prices.append(mc_p)

intrinsic_range = np.maximum(spot_range - K, 0)

fig3 = go.Figure()

fig3.add_trace(go.Scatter(
    x=spot_range, y=bs_prices,
    mode='lines+markers',
    name='Black-Scholes',
    line=dict(color=CHART_COLORS['black_scholes'], width=3),
    marker=dict(size=4)
))

fig3.add_trace(go.Scatter(
    x=spot_range, y=mc_prices,
    mode='lines+markers',
    name='Monte Carlo',
    line=dict(color=CHART_COLORS['monte_carlo'], width=3),
    marker=dict(size=4)
))

fig3.add_trace(go.Scatter(
    x=spot_range, y=intrinsic_range,
    mode='lines',
    name='Intrinsic Value (at expiry)',
    line=dict(color=CHART_COLORS['intrinsic'], width=3, dash='dash')
))

fig3.add_vline(S, line_dash=":", line_color="gray", 
               annotation_text=f"Current Spot: ${S:.2f}")

fig3.update_layout(
    title="Call Option Price Sensitivity Across Spot Prices (6-month maturity)",
    xaxis_title="Spot Price at Inception ($)",
    yaxis_title="Option Price ($)",
    hovermode='x unified',
    height=500,
    template="plotly_white"
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ============================================================================
# CHART 3: MC Convergence
# ============================================================================

st.subheader("Chart 3: Monte Carlo Convergence Analysis")

col_conv1, col_conv2 = st.columns(2)

with col_conv1:
    # MC Convergence
    mc_convergence = []
    
    for sim_count in CONVERGENCE_POINTS:
        mc_p, _ = monte_carlo_call(S, K, r, sigma, T, num_simulations=sim_count)
        mc_convergence.append(mc_p)
    
    fig4 = go.Figure()
    
    fig4.add_trace(go.Scatter(
        x=CONVERGENCE_POINTS, y=mc_convergence,
        mode='lines+markers',
        name='MC Price',
        line=dict(color=CHART_COLORS['monte_carlo'], width=3),
        marker=dict(size=8)
    ))
    
    fig4.add_hline(bs_price, line_dash="dash", line_color=CHART_COLORS['black_scholes'],
                   annotation_text=f"BS Theoretical: ${bs_price:.2f}")
    
    fig4.add_hline(intrinsic_value, line_dash="dash", line_color=CHART_COLORS['intrinsic'],
                   annotation_text=f"Actual Payoff: ${intrinsic_value:.2f}")
    
    fig4.update_xaxes(type="log")
    fig4.update_layout(
        title="Monte Carlo Convergence (log scale)",
        xaxis_title="Number of Simulations",
        yaxis_title="Call Option Price ($)",
        hovermode='x unified',
        height=500,
        template="plotly_white"
    )
    
    st.plotly_chart(fig4, use_container_width=True)

with col_conv2:
    # MC Error Reduction
    errors = [abs(mc_p - intrinsic_value) for mc_p in mc_convergence]
    error_pcts = [(e / intrinsic_value * 100) if intrinsic_value > 0 else 0 for e in errors]
    
    fig5 = go.Figure()
    
    fig5.add_trace(go.Scatter(
        x=CONVERGENCE_POINTS, y=error_pcts,
        mode='lines+markers',
        name='Error %',
        line=dict(color=CHART_COLORS['intrinsic'], width=3),
        marker=dict(size=8),
        fill='tozeroy'
    ))
    
    fig5.update_xaxes(type="log")
    fig5.update_layout(
        title="Absolute Error % vs Actual (log scale)",
        xaxis_title="Number of Simulations",
        yaxis_title="Error (%)",
        hovermode='x unified',
        height=500,
        template="plotly_white"
    )
    
    st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# ============================================================================
# CHART 4: Individual MC Paths
# ============================================================================

st.subheader("Chart 4: Sample Monte Carlo Price Paths (GBM)")

times, paths, mean_path = generate_mc_paths(S, K, r, sigma, T, MC_PATH_COUNT, MC_STEP_COUNT)

fig6 = go.Figure()

# Add individual paths
for i in range(MC_PATH_COUNT):
    fig6.add_trace(go.Scatter(
        x=times * 12,
        y=paths[i, :],
        mode='lines',
        line=dict(color='rgba(52, 152, 219, 0.03)'),
        hoverinfo='skip',
        showlegend=False
    ))

# Add mean path
fig6.add_trace(go.Scatter(
    x=times * 12,
    y=mean_path,
    mode='lines',
    name='Mean Path',
    line=dict(color=CHART_COLORS['mean'], width=3)
))

# Add strike and actual
fig6.add_hline(K, line_dash="dash", line_color=CHART_COLORS['actual'],
               annotation_text=f"Strike: ${K:.2f}")
fig6.add_hline(S_T_actual, line_dash="dash", line_color="green",
               annotation_text=f"Actual Spot: ${S_T_actual:.2f}")

fig6.update_layout(
    title=f"{MC_PATH_COUNT} Sample Monte Carlo Paths (Geometric Brownian Motion)",
    xaxis_title="Time (months)",
    yaxis_title="Spot Price ($)",
    hovermode='x unified',
    height=500,
    template="plotly_white"
)

st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

# ============================================================================
# DETAILED STATISTICS TABLE
# ============================================================================

st.subheader("📊 Detailed Statistical Analysis")

stats_data = {
    'Metric': [
        'Spot Price at Inception',
        'Strike Price',
        'Spot Price at Expiry',
        'Time to Expiry (years)',
        'Risk-Free Rate (%)',
        'Volatility (%)',
        'Mean Simulated Price',
        'Std Dev (MC prices)',
        'Min Simulated Price',
        'Max Simulated Price',
        '---',
        'Black-Scholes Price',
        'Monte Carlo Price',
        'Actual Intrinsic Value',
        '---',
        'BS Error ($)',
        'BS Error (%)',
        'MC Error ($)',
        'MC Error (%)',
        'Model Difference'
    ],
    'Value': [
        f"${S:.2f}",
        f"${K:.2f}",
        f"${S_T_actual:.2f}",
        f"{T:.4f}",
        f"{r*100:.2f}%",
        f"{sigma*100:.2f}%",
        f"${np.mean(simulated_prices):.2f}",
        f"${np.std(simulated_prices):.2f}",
        f"${np.min(simulated_prices):.2f}",
        f"${np.max(simulated_prices):.2f}",
        "",
        f"${bs_price:.2f}",
        f"${mc_price:.2f}",
        f"${intrinsic_value:.2f}",
        "",
        f"${bs_error:.2f}",
        f"{bs_error_pct:.2f}%",
        f"${mc_error:.2f}",
        f"{mc_error_pct:.2f}%",
        f"${abs(bs_price - mc_price):.2f}"
    ]
}

stats_df = pd.DataFrame(stats_data)
st.dataframe(stats_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ============================================================================
# CONVERGENCE TABLE
# ============================================================================

st.subheader("Monte Carlo Convergence Table")

convergence_data = []
for sim_count in CONVERGENCE_POINTS:
    mc_p, _ = monte_carlo_call(S, K, r, sigma, T, num_simulations=sim_count)
    error = abs(mc_p - intrinsic_value)
    error_pct = (error / intrinsic_value * 100) if intrinsic_value > 0 else 0
    
    convergence_data.append({
        'Simulations': f"{sim_count:,}",
        'MC Price ($)': f"{mc_p:.4f}",
        'Error ($)': f"{error:.4f}",
        'Error (%)': f"{error_pct:.2f}%"
    })

conv_df = pd.DataFrame(convergence_data)
st.dataframe(conv_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ============================================================================
# INSIGHTS & SUMMARY
# ============================================================================

st.subheader("🎯 Key Insights")

col_insight1, col_insight2, col_insight3 = st.columns(3)

with col_insight1:
    if bs_error_pct < mc_error_pct:
        insight_text = f"✅ **Black-Scholes** more accurate ({bs_error_pct:.1f}% vs {mc_error_pct:.1f}%)"
        color = "green"
    else:
        insight_text = f"✅ **Monte Carlo** more accurate ({mc_error_pct:.1f}% vs {bs_error_pct:.1f}%)"
        color = "green"
    
    st.markdown(f"<span style='color:{color}'>{insight_text}</span>", unsafe_allow_html=True)

with col_insight2:
    moneyness = (S / K - 1) * 100
    if moneyness > 0:
        st.markdown(f"💰 Option **In-The-Money** by {moneyness:.1f}%")
    elif moneyness < 0:
        st.markdown(f"📉 Option **Out-of-The-Money** by {abs(moneyness):.1f}%")
    else:
        st.markdown("📊 Option **At-The-Money**")

with col_insight3:
    actual_return = ((S_T_actual - S) / S) * 100
    st.markdown(f"📈 Actual Return: **{actual_return:.1f}%**")

st.markdown("""
#### Model Analysis:

1. **Black-Scholes**: Theoretical model assuming constant volatility and log-normal distribution
2. **Monte Carlo**: Numerical simulation using 100k+ random paths
3. **Convergence**: MC price stabilizes as simulations increase
4. **Real Outcome**: Compares both models against actual option payoff at expiry

#### Why Compare?
- Validates pricing theory with real market data
- Shows when models diverge from reality
- 6-month horizon reduces time decay uncertainty
- Portfolio-worthy project demonstrating quantitative finance expertise
""")

st.markdown("---")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px; padding: 20px;'>
    <p>📊 Options Pricing Comparison Tool | Real Data Analysis</p>
    <p>Black-Scholes Formula | Monte Carlo Simulation | Accuracy Metrics</p>
    <p><i>Real option data with 6-month expiration periods</i></p>
</div>
""", unsafe_allow_html=True)
