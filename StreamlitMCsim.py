import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np

# Define the function to run the simulation
def investment_simulator(starting_capital, win_percent, win_amount, loss_amount, num_trades, num_simulations):
    all_results = []
    for _ in range(num_simulations):
        results = [starting_capital]
        for _ in range(num_trades):
            if random.random() < win_percent:
                results.append(results[-1] + win_amount)
            else:
                results.append(results[-1] - loss_amount)
        all_results.append(results)
    return all_results

# Streamlit code
st.title('Monte Carlo Simulation of Investment Strategy')

# Get user inputs
starting_capital = st.number_input('Enter your starting capital', min_value=0)
win_percent = st.number_input('Enter your win percent (as a decimal between 0 and 1)', 0.0, 1.0)
win_amount = st.number_input('Enter the amount you win when you do win', min_value=0)
loss_amount = st.number_input('Enter the amount you lose when you do lose', min_value=0)
num_trades = st.number_input('Enter the number of trades you want to simulate', min_value=0, format="%i")
num_simulations = st.number_input('Enter the number of simulations you want to run', min_value=0, format="%i", value=10)

if st.button('Run Simulations'):
    # Run the simulation with the user inputs
    all_results = investment_simulator(starting_capital, win_percent, win_amount, loss_amount, num_trades, num_simulations)
    
    # Calculate final values and ROIs
    final_values = [results[-1] for results in all_results]
    rois = [(final - starting_capital) * 100.0 / starting_capital for final in final_values]
    
    # Calculate and display summary statistics
    avg_roi = np.mean(rois)
    top_5_roi = np.percentile(rois, 95)
    bottom_5_roi = np.percentile(rois, 5)
    st.write(f'Average ROI: {avg_roi:.2f}%')
    st.write(f'Top 5% ROI: {top_5_roi:.2f}%')
    st.write(f'Bottom 5% ROI: {bottom_5_roi:.2f}%')
    
    # Plot the results of each simulation
    fig, ax = plt.subplots(figsize=(10, 6))
    for results in all_results:
        ax.plot(results)
    
    ax.set_title('Monte Carlo Simulation of Investment Strategy')
    ax.set_xlabel('Trade Number')
    ax.set_ylabel('Portfolio Value')
    
    # Add legend after plotting all lines
    ax.legend([f'Average ROI: {avg_roi:.2f}%', 
               f'Top 5% ROI: {top_5_roi:.2f}%', 
               f'Bottom 5% ROI: {bottom_5_roi:.2f}%'], 
              loc='upper left')
    
    st.pyplot(fig)
