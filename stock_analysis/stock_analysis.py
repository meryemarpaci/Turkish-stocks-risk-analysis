import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from scipy import stats
import seaborn as sns
from datetime import datetime
import os

# Set Turkish font support for matplotlib
plt.rcParams['font.family'] = 'DejaVu Sans'

# Define the Turkish stocks to analyze
# Using BIST (Borsa Istanbul) stock symbols with .IS suffix for Yahoo Finance
stocks = ['THYAO.IS', 'EREGL.IS']  # Turkish Airlines and Eregli Demir Celik
stock_names = {'THYAO.IS': 'Türk Hava Yolları', 'EREGL.IS': 'Ereğli Demir Çelik'}

# Define the date range (from 2020 to present)
start_date = '2020-01-01'
end_date = datetime.now().strftime('%Y-%m-%d')

# Make sure data and plots directories exist
os.makedirs('data', exist_ok=True)
os.makedirs('plots', exist_ok=True)

def download_stock_data():
    """Download stock data from Yahoo Finance."""
    print(f"Downloading stock data for {stocks} from {start_date} to {end_date}...")
    
    all_data = {}
    for stock in stocks:
        try:
            data = yf.download(stock, start=start_date, end=end_date, auto_adjust=True)
            all_data[stock] = data
            print(f"Successfully downloaded data for {stock}")
            # Save to CSV
            data.to_csv(f"data/{stock.replace('.', '_')}.csv")
            print(f"Data saved to data/{stock.replace('.', '_')}.csv")
        except Exception as e:
            print(f"Error downloading {stock}: {e}")
    
    return all_data

def calculate_returns(data_dict):
    """Calculate daily returns from price data."""
    returns_dict = {}
    
    for stock, data in data_dict.items():
        if data is not None and not data.empty:
            # Check if 'Adj Close' exists, otherwise use 'Close'
            price_col = 'Close'
            if 'Adj Close' in data.columns:
                price_col = 'Adj Close'
            elif 'Adj_Close' in data.columns:
                price_col = 'Adj_Close'
            
            print(f"Using '{price_col}' column for {stock}")
            # Calculate log returns
            data['Returns'] = np.log(data[price_col] / data[price_col].shift(1))
            returns_dict[stock] = data.dropna()  # Drop NaN values
    
    return returns_dict

def calculate_z_scores(returns_dict):
    """Calculate Z-scores for the returns."""
    z_scores_dict = {}
    
    for stock, data in returns_dict.items():
        if not data.empty:
            mean_return = data['Returns'].mean()
            std_return = data['Returns'].std()
            
            # Calculate Z-scores
            data['Z_Score'] = (data['Returns'] - mean_return) / std_return
            z_scores_dict[stock] = data
    
    return z_scores_dict

def analyze_distribution(z_scores_dict):
    """Analyze the distribution of returns and Z-scores."""
    results = {}
    
    for stock, data in z_scores_dict.items():
        if not data.empty:
            returns = data['Returns'].values
            z_scores = data['Z_Score'].values
            
            # Calculate kurtosis and skewness
            kurtosis = stats.kurtosis(returns)
            skewness = stats.skew(returns)
            
            # Normal distribution has kurtosis = 0
            excess_kurtosis = kurtosis
            
            results[stock] = {
                'Mean Return': returns.mean(),
                'Std Dev': returns.std(),
                'Skewness': skewness,
                'Kurtosis': kurtosis,
                'Excess Kurtosis': excess_kurtosis,  # Excess kurtosis = kurtosis - 3 for raw kurtosis
                'Max Z-Score': z_scores.max(),
                'Min Z-Score': z_scores.min(),
                'Z-Score > 2 Count': (z_scores > 2).sum(),
                'Z-Score < -2 Count': (z_scores < -2).sum(),
            }
            
            # Print the results
            print(f"\nAnalysis for {stock_names.get(stock, stock)}:")
            for key, value in results[stock].items():
                print(f"{key}: {value:.4f}")
    
    return results

def plot_distributions(z_scores_dict):
    """Plot histograms and QQ plots of returns to visualize distributions."""
    
    for stock, data in z_scores_dict.items():
        if not data.empty:
            returns = data['Returns'].values
            
            # Create a figure with subplots
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            fig.suptitle(f'Dağılım Analizi - {stock_names.get(stock, stock)}', fontsize=16)
            
            # Histogram of returns
            sns.histplot(returns, kde=True, ax=axes[0, 0])
            axes[0, 0].set_title('Getiri Dağılımı')
            axes[0, 0].set_xlabel('Günlük Getiri')
            axes[0, 0].set_ylabel('Frekans')
            
            # Normal Q-Q plot
            stats.probplot(returns, plot=axes[0, 1])
            axes[0, 1].set_title('Normal Q-Q Plot')
            
            # Z-score time series
            axes[1, 0].plot(data.index, data['Z_Score'])
            axes[1, 0].set_title('Z-Skor Zaman Serisi')
            axes[1, 0].set_xlabel('Tarih')
            axes[1, 0].set_ylabel('Z-Skor')
            axes[1, 0].axhline(y=2, color='r', linestyle='--')
            axes[1, 0].axhline(y=-2, color='r', linestyle='--')
            
            # Box plot
            sns.boxplot(y=returns, ax=axes[1, 1])
            axes[1, 1].set_title('Getiri Kutu Grafiği')
            axes[1, 1].set_ylabel('Günlük Getiri')
            
            plt.tight_layout(rect=[0, 0, 1, 0.95])
            plt.savefig(f"plots/{stock.replace('.', '_')}_distribution.png")
            plt.close()

def plot_comparison(results):
    """Plot comparison of skewness and kurtosis between stocks."""
    
    stocks_list = list(results.keys())
    names = [stock_names.get(stock, stock) for stock in stocks_list]
    
    metrics = ['Skewness', 'Kurtosis']
    values = [[results[stock][metric] for stock in stocks_list] for metric in metrics]
    
    fig, ax = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot skewness comparison
    ax[0].bar(names, values[0])
    ax[0].set_title('Çarpıklık (Skewness) Karşılaştırması')
    ax[0].set_ylabel('Çarpıklık Değeri')
    ax[0].axhline(y=0, color='r', linestyle='-')
    
    # Plot kurtosis comparison
    ax[1].bar(names, values[1])
    ax[1].set_title('Basıklık (Kurtosis) Karşılaştırması')
    ax[1].set_ylabel('Basıklık Değeri')
    ax[1].axhline(y=0, color='r', linestyle='-')
    
    plt.tight_layout()
    plt.savefig("plots/comparison.png")
    plt.close()

def filter_extreme_days(z_scores_dict, threshold=2):
    """Filter and show days with extreme movements (high Z-scores)."""
    
    for stock, data in z_scores_dict.items():
        if not data.empty:
            # Filter for extreme days (Z-score > threshold or Z-score < -threshold)
            extreme_days = data[(data['Z_Score'] > threshold) | (data['Z_Score'] < -threshold)].copy()
            
            if not extreme_days.empty:
                print(f"\nAşırı Hareket Günleri - {stock_names.get(stock, stock)} (|Z-Skor| > {threshold}):")
                extreme_days['Date'] = extreme_days.index.strftime('%Y-%m-%d')
                extreme_days = extreme_days.sort_values('Z_Score', ascending=False)
                
                # Format for better readability
                for idx, row in extreme_days.iterrows():
                    # Make sure to use the scalar value, not a Series
                    return_value = row['Returns']
                    if isinstance(return_value, pd.Series):
                        return_value = return_value.iloc[0]
                    
                    direction = "Yükseliş" if return_value > 0 else "Düşüş"
                    
                    # Same for Z-Score
                    z_score = row['Z_Score']
                    if isinstance(z_score, pd.Series):
                        z_score = z_score.iloc[0]
                        
                    print(f"{row['Date']}: Z-Skor = {z_score:.2f}, Getiri = {return_value*100:.2f}% ({direction})")
                
                # Save to CSV
                extreme_days.to_csv(f"data/{stock.replace('.', '_')}_extreme_days.csv")

def main():
    """Main function to run the analysis."""
    
    print("Türk Hisse Senedi Analizi Başlatılıyor...")
    
    # Download stock data
    all_data = download_stock_data()
    
    # Calculate returns
    returns_dict = calculate_returns(all_data)
    
    # Calculate Z-scores
    z_scores_dict = calculate_z_scores(returns_dict)
    
    # Analyze distributions
    results = analyze_distribution(z_scores_dict)
    
    # Plot distributions
    plot_distributions(z_scores_dict)
    
    # Plot comparison
    plot_comparison(results)
    
    # Filter extreme days
    filter_extreme_days(z_scores_dict)
    
    print("\nAnaliz tamamlandı.")
    print("Grafikler plots dizinine kaydedildi.")
    print("Veri dosyaları data dizinine kaydedildi.")

if __name__ == "__main__":
    main() 