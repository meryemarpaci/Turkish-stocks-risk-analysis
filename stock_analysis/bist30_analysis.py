import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from scipy import stats
import seaborn as sns
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

# Set Turkish font support and style
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# BIST30 hisse senetleri ve sektör bilgileri
BIST30_STOCKS = {
    'AKBNK.IS': {'name': 'Akbank', 'sector': 'Bankacılık'},
    'ARCLK.IS': {'name': 'Arçelik', 'sector': 'Dayanıklı Tüketim'},
    'ASELS.IS': {'name': 'Aselsan', 'sector': 'Savunma'},
    'BIMAS.IS': {'name': 'BİM', 'sector': 'Perakende'},
    'EKGYO.IS': {'name': 'Emlak Konut GYO', 'sector': 'Gayrimenkul'},
    'EREGL.IS': {'name': 'Ereğli Demir Çelik', 'sector': 'Metal Ana'},
    'FROTO.IS': {'name': 'Ford Otosan', 'sector': 'Otomotiv'},
    'GARAN.IS': {'name': 'Garanti BBVA', 'sector': 'Bankacılık'},
    'HALKB.IS': {'name': 'Halkbank', 'sector': 'Bankacılık'},
    'ISCTR.IS': {'name': 'İş Bankası (C)', 'sector': 'Bankacılık'},
    'KCHOL.IS': {'name': 'Koç Holding', 'sector': 'Holding'},
    'KOZAL.IS': {'name': 'Koza Altın', 'sector': 'Madencilik'},
    'KOZAA.IS': {'name': 'Koza Anadolu', 'sector': 'Madencilik'},
    'PETKM.IS': {'name': 'Petkim', 'sector': 'Petrokimya'},
    'PGSUS.IS': {'name': 'Pegasus', 'sector': 'Havacılık'},
    'SAHOL.IS': {'name': 'Sabancı Holding', 'sector': 'Holding'},
    'SISE.IS': {'name': 'Şişe Cam', 'sector': 'Cam'},
    'TCELL.IS': {'name': 'Turkcell', 'sector': 'Telekomünikasyon'},
    'THYAO.IS': {'name': 'Türk Hava Yolları', 'sector': 'Havacılık'},
    'TOASO.IS': {'name': 'Tofaş', 'sector': 'Otomotiv'},
    'TUPRS.IS': {'name': 'Tüpraş', 'sector': 'Petrol'},
    'VAKBN.IS': {'name': 'VakıfBank', 'sector': 'Bankacılık'},
    'YKBNK.IS': {'name': 'Yapı Kredi', 'sector': 'Bankacılık'},
    'SMRTG.IS': {'name': 'Smart Güneş', 'sector': 'Enerji'},
    'TAVHL.IS': {'name': 'TAV Havalimanları', 'sector': 'Ulaştırma'}
}

# Define the date range
start_date = '2020-01-01'
end_date = datetime.now().strftime('%Y-%m-%d')

# Make sure directories exist
os.makedirs('data', exist_ok=True)
os.makedirs('plots', exist_ok=True)
os.makedirs('reports', exist_ok=True)

def download_stock_data():
    """Download stock data for all BIST30 stocks."""
    print(f"BIST30 hisse senetleri indiriliyor... ({start_date} - {end_date})")
    
    all_data = {}
    failed_downloads = []
    
    for i, (stock, info) in enumerate(BIST30_STOCKS.items(), 1):
        try:
            print(f"[{i}/{len(BIST30_STOCKS)}] {info['name']} ({stock}) indiriliyor...")
            data = yf.download(stock, start=start_date, end=end_date, auto_adjust=True, progress=False)
            
            if not data.empty:
                all_data[stock] = data
                # Save to CSV
                data.to_csv(f"data/{stock.replace('.', '_')}.csv")
                print(f"✓ {info['name']} başarıyla indirildi")
            else:
                failed_downloads.append(stock)
                print(f"✗ {info['name']} için veri bulunamadı")
                
        except Exception as e:
            failed_downloads.append(stock)
            print(f"✗ {info['name']} indirme hatası: {e}")
    
    if failed_downloads:
        print(f"\nUyarı: {len(failed_downloads)} hisse senedi indirilemedi: {failed_downloads}")
    
    return all_data

def calculate_returns_and_metrics(data_dict):
    """Calculate returns and various risk metrics."""
    results = {}
    
    print("\nGetiri ve risk metrikleri hesaplanıyor...")
    
    for stock, data in data_dict.items():
        if data is not None and not data.empty:
            # Use Close price
            price_col = 'Close'
            if 'Adj Close' in data.columns:
                price_col = 'Adj Close'
            
            # Calculate returns
            data['Returns'] = np.log(data[price_col] / data[price_col].shift(1))
            data = data.dropna()
            
            if len(data) > 20:  # Minimum data requirement
                returns = data['Returns'].values
                
                # Calculate Z-scores
                mean_return = returns.mean()
                std_return = returns.std()
                data['Z_Score'] = (returns - mean_return) / std_return
                
                # Calculate comprehensive metrics
                results[stock] = {
                    'data': data,
                    'name': BIST30_STOCKS[stock]['name'],
                    'sector': BIST30_STOCKS[stock]['sector'],
                    'mean_return': mean_return,
                    'std_return': std_return,
                    'annual_return': mean_return * 252,
                    'annual_volatility': std_return * np.sqrt(252),
                    'sharpe_ratio': (mean_return * 252) / (std_return * np.sqrt(252)) if std_return > 0 else 0,
                    'skewness': stats.skew(returns),
                    'kurtosis': stats.kurtosis(returns),
                    'var_95': np.percentile(returns, 5),  # Value at Risk (95%)
                    'var_99': np.percentile(returns, 1),  # Value at Risk (99%)
                    'max_drawdown': calculate_max_drawdown(data[price_col]),
                    'extreme_positive': (data['Z_Score'] > 2).sum(),
                    'extreme_negative': (data['Z_Score'] < -2).sum(),
                    'total_observations': len(returns)
                }
    
    return results

def calculate_max_drawdown(prices):
    """Calculate maximum drawdown."""
    try:
        # Calculate percentage changes
        returns = prices.pct_change().fillna(0)
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        return drawdown.min()
    except Exception as e:
        print(f"Max drawdown calculation error: {e}")
        return 0.0

def create_risk_ranking(results):
    """Create risk ranking and categorization."""
    print("\nRisk sıralaması oluşturuluyor...")
    
    # Create DataFrame for analysis
    df_metrics = []
    for stock, metrics in results.items():
        df_metrics.append({
            'Symbol': stock,
            'Name': metrics['name'],
            'Sector': metrics['sector'],
            'Annual_Return': metrics['annual_return'],
            'Annual_Volatility': metrics['annual_volatility'],
            'Sharpe_Ratio': metrics['sharpe_ratio'],
            'Skewness': metrics['skewness'],
            'Kurtosis': metrics['kurtosis'],
            'VaR_95': metrics['var_95'],
            'Max_Drawdown': metrics['max_drawdown'],
            'Extreme_Days': metrics['extreme_positive'] + metrics['extreme_negative']
        })
    
    df = pd.DataFrame(df_metrics)
    
    # Handle NaN values and reset index
    df = df.fillna(0).reset_index(drop=True)
    
    # Calculate risk scores with safe ranking
    try:
        df['Risk_Score'] = (
            df['Annual_Volatility'].rank(pct=True, method='dense') * 0.3 +
            df['Kurtosis'].rank(pct=True, method='dense') * 0.2 +
            df['Extreme_Days'].rank(pct=True, method='dense') * 0.2 +
            df['Max_Drawdown'].abs().rank(pct=True, method='dense') * 0.2 +
            df['VaR_95'].abs().rank(pct=True, method='dense') * 0.1
        )
    except Exception as e:
        print(f"Risk score calculation error: {e}")
        # Fallback: simple scoring
        df['Risk_Score'] = df['Annual_Volatility'] / df['Annual_Volatility'].max()
    
    # Categorize risk levels
    df['Risk_Category'] = pd.cut(df['Risk_Score'], 
                                bins=[0, 0.33, 0.66, 1], 
                                labels=['Düşük Risk', 'Orta Risk', 'Yüksek Risk'])
    
    # Sort by risk score
    df = df.sort_values('Risk_Score')
    
    # Save detailed results
    df.to_csv('reports/risk_ranking.csv', index=False)
    
    return df

def plot_comprehensive_analysis(results, risk_df):
    """Create comprehensive visualization plots."""
    print("\nKapsamlı görselleştirmeler oluşturuluyor...")
    
    # 1. Risk Dashboard
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('BIST30 Risk Analizi Dashboard', fontsize=20, fontweight='bold')
    
    # Risk Score vs Return
    scatter = axes[0, 0].scatter(risk_df['Risk_Score'], risk_df['Annual_Return']*100, 
                                c=risk_df['Annual_Volatility']*100, s=100, alpha=0.7, cmap='viridis')
    axes[0, 0].set_xlabel('Risk Skoru')
    axes[0, 0].set_ylabel('Yıllık Getiri (%)')
    axes[0, 0].set_title('Risk-Getiri İlişkisi')
    plt.colorbar(scatter, ax=axes[0, 0], label='Yıllık Volatilite (%)')
    
    # Volatility by Sector
    sector_vol = risk_df.groupby('Sector')['Annual_Volatility'].mean().sort_values(ascending=False)
    axes[0, 1].bar(range(len(sector_vol)), sector_vol*100)
    axes[0, 1].set_xticks(range(len(sector_vol)))
    axes[0, 1].set_xticklabels(sector_vol.index, rotation=45, ha='right')
    axes[0, 1].set_ylabel('Ortalama Yıllık Volatilite (%)')
    axes[0, 1].set_title('Sektörel Volatilite Karşılaştırması')
    
    # Skewness vs Kurtosis
    risk_colors = {'Düşük Risk': 'green', 'Orta Risk': 'orange', 'Yüksek Risk': 'red'}
    for category in risk_df['Risk_Category'].unique():
        if pd.notna(category):
            subset = risk_df[risk_df['Risk_Category'] == category]
            axes[0, 2].scatter(subset['Skewness'], subset['Kurtosis'], 
                             label=category, alpha=0.7, s=80, color=risk_colors.get(category, 'blue'))
    axes[0, 2].set_xlabel('Çarpıklık (Skewness)')
    axes[0, 2].set_ylabel('Basıklık (Kurtosis)')
    axes[0, 2].set_title('Dağılım Özellikleri')
    axes[0, 2].legend()
    axes[0, 2].axhline(y=0, color='black', linestyle='--', alpha=0.5)
    axes[0, 2].axvline(x=0, color='black', linestyle='--', alpha=0.5)
    
    # Sharpe Ratio Ranking
    top_sharpe = risk_df.nlargest(10, 'Sharpe_Ratio')
    axes[1, 0].barh(range(len(top_sharpe)), top_sharpe['Sharpe_Ratio'])
    axes[1, 0].set_yticks(range(len(top_sharpe)))
    axes[1, 0].set_yticklabels(top_sharpe['Name'], fontsize=8)
    axes[1, 0].set_xlabel('Sharpe Oranı')
    axes[1, 0].set_title('En İyi Sharpe Oranları')
    
    # Risk Distribution
    risk_counts = risk_df['Risk_Category'].value_counts()
    colors = [risk_colors.get(cat, 'blue') for cat in risk_counts.index]
    axes[1, 1].pie(risk_counts.values, labels=risk_counts.index, autopct='%1.1f%%', colors=colors)
    axes[1, 1].set_title('Risk Kategorisi Dağılımı')
    
    # Extreme Days vs Volatility
    axes[1, 2].scatter(risk_df['Annual_Volatility']*100, risk_df['Extreme_Days'], alpha=0.7, s=80)
    axes[1, 2].set_xlabel('Yıllık Volatilite (%)')
    axes[1, 2].set_ylabel('Aşırı Hareket Günleri')
    axes[1, 2].set_title('Volatilite vs Aşırı Hareketler')
    
    plt.tight_layout()
    plt.savefig('plots/risk_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Sector Analysis
    plot_sector_analysis(risk_df)
    
    # 3. Individual Stock Distributions (top 6 by market interest)
    plot_individual_distributions(results, ['AKBNK.IS', 'GARAN.IS', 'THYAO.IS', 'EREGL.IS', 'BIMAS.IS', 'SISE.IS'])

def plot_sector_analysis(risk_df):
    """Plot detailed sector analysis."""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('BIST30 Sektörel Analiz', fontsize=18, fontweight='bold')
    
    # Sector performance summary
    sector_summary = risk_df.groupby('Sector').agg({
        'Annual_Return': 'mean',
        'Annual_Volatility': 'mean',
        'Sharpe_Ratio': 'mean',
        'Risk_Score': 'mean'
    }).round(4)
    
    # Average return by sector
    sector_summary['Annual_Return'].plot(kind='bar', ax=axes[0, 0], color='skyblue')
    axes[0, 0].set_title('Sektörel Ortalama Yıllık Getiri')
    axes[0, 0].set_ylabel('Yıllık Getiri')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # Risk-Return by sector
    axes[0, 1].scatter(sector_summary['Risk_Score'], sector_summary['Annual_Return'], s=200, alpha=0.7)
    for i, sector in enumerate(sector_summary.index):
        axes[0, 1].annotate(sector, (sector_summary['Risk_Score'].iloc[i], sector_summary['Annual_Return'].iloc[i]),
                           xytext=(5, 5), textcoords='offset points', fontsize=8)
    axes[0, 1].set_xlabel('Ortalama Risk Skoru')
    axes[0, 1].set_ylabel('Ortalama Yıllık Getiri')
    axes[0, 1].set_title('Sektörel Risk-Getiri Pozisyonu')
    
    # Volatility comparison
    sector_summary['Annual_Volatility'].plot(kind='bar', ax=axes[1, 0], color='lightcoral')
    axes[1, 0].set_title('Sektörel Ortalama Volatilite')
    axes[1, 0].set_ylabel('Yıllık Volatilite')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # Sharpe ratio comparison
    sector_summary['Sharpe_Ratio'].plot(kind='bar', ax=axes[1, 1], color='lightgreen')
    axes[1, 1].set_title('Sektörel Ortalama Sharpe Oranı')
    axes[1, 1].set_ylabel('Sharpe Oranı')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('plots/sector_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save sector summary
    sector_summary.to_csv('reports/sector_summary.csv')

def plot_individual_distributions(results, selected_stocks):
    """Plot distribution analysis for selected stocks."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Seçili Hisse Senetleri Dağılım Analizi', fontsize=16, fontweight='bold')
    
    for i, stock in enumerate(selected_stocks):
        if stock in results:
            row, col = i // 3, i % 3
            data = results[stock]['data']
            returns = data['Returns'].values
            
            # Plot histogram with normal comparison
            axes[row, col].hist(returns, bins=50, density=True, alpha=0.7, color='skyblue', edgecolor='black')
            
            # Overlay normal distribution
            mu, sigma = returns.mean(), returns.std()
            x = np.linspace(returns.min(), returns.max(), 100)
            normal_dist = stats.norm.pdf(x, mu, sigma)
            axes[row, col].plot(x, normal_dist, 'r-', linewidth=2, label='Normal Dağılım')
            
            axes[row, col].set_title(f"{results[stock]['name']}\nÇarpıklık: {results[stock]['skewness']:.3f}, "
                                   f"Basıklık: {results[stock]['kurtosis']:.3f}")
            axes[row, col].set_xlabel('Günlük Getiri')
            axes[row, col].set_ylabel('Yoğunluk')
            axes[row, col].legend()
    
    plt.tight_layout()
    plt.savefig('plots/individual_distributions.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_correlation_matrix(results):
    """Create correlation matrix of returns."""
    print("\nKorelasyon matrisi oluşturuluyor...")
    
    # Prepare returns data
    returns_data = {}
    for stock, data in results.items():
        returns_data[data['name']] = data['data']['Returns']
    
    returns_df = pd.DataFrame(returns_data)
    correlation_matrix = returns_df.corr()
    
    # Plot correlation heatmap
    plt.figure(figsize=(16, 14))
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
    sns.heatmap(correlation_matrix, mask=mask, annot=True, fmt='.2f', 
                center=0, cmap='coolwarm', square=True, cbar_kws={'label': 'Korelasyon'})
    plt.title('BIST30 Hisse Senetleri Korelasyon Matrisi', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('plots/correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save correlation matrix
    correlation_matrix.to_csv('reports/correlation_matrix.csv')
    
    return correlation_matrix

def generate_summary_report(results, risk_df):
    """Generate comprehensive summary report."""
    print("\nÖzet rapor oluşturuluyor...")
    
    report_lines = []
    report_lines.append("# BIST30 Risk Analizi Raporu")
    report_lines.append(f"**Analiz Tarihi:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report_lines.append(f"**Veri Aralığı:** {start_date} - {end_date}")
    report_lines.append(f"**Analiz Edilen Hisse Sayısı:** {len(results)}")
    report_lines.append("")
    
    # Executive Summary
    report_lines.append("## Yönetici Özeti")
    avg_return = risk_df['Annual_Return'].mean() * 100
    avg_volatility = risk_df['Annual_Volatility'].mean() * 100
    avg_sharpe = risk_df['Sharpe_Ratio'].mean()
    
    report_lines.append(f"- **Ortalama Yıllık Getiri:** {avg_return:.2f}%")
    report_lines.append(f"- **Ortalama Yıllık Volatilite:** {avg_volatility:.2f}%")
    report_lines.append(f"- **Ortalama Sharpe Oranı:** {avg_sharpe:.3f}")
    report_lines.append("")
    
    # Risk Categories
    report_lines.append("## Risk Kategorileri")
    risk_counts = risk_df['Risk_Category'].value_counts()
    for category, count in risk_counts.items():
        if pd.notna(category):
            percentage = (count / len(risk_df)) * 100
            report_lines.append(f"- **{category}:** {count} hisse ({percentage:.1f}%)")
    report_lines.append("")
    
    # Top Performers
    report_lines.append("## En İyi Performans")
    top_return = risk_df.nlargest(5, 'Annual_Return')[['Name', 'Annual_Return', 'Risk_Category']]
    report_lines.append("### En Yüksek Getiri")
    for _, row in top_return.iterrows():
        report_lines.append(f"- **{row['Name']}:** {row['Annual_Return']*100:.2f}% ({row['Risk_Category']})")
    report_lines.append("")
    
    top_sharpe = risk_df.nlargest(5, 'Sharpe_Ratio')[['Name', 'Sharpe_Ratio', 'Risk_Category']]
    report_lines.append("### En Yüksek Sharpe Oranı")
    for _, row in top_sharpe.iterrows():
        report_lines.append(f"- **{row['Name']}:** {row['Sharpe_Ratio']:.3f} ({row['Risk_Category']})")
    report_lines.append("")
    
    # Sector Performance
    report_lines.append("## Sektörel Performans")
    sector_summary = risk_df.groupby('Sector').agg({
        'Annual_Return': 'mean',
        'Annual_Volatility': 'mean',
        'Sharpe_Ratio': 'mean'
    }).round(4)
    
    best_sector = sector_summary.loc[sector_summary['Sharpe_Ratio'].idxmax()]
    report_lines.append(f"**En İyi Sektör (Sharpe Oranı):** {sector_summary['Sharpe_Ratio'].idxmax()}")
    report_lines.append(f"- Ortalama Getiri: {best_sector['Annual_Return']*100:.2f}%")
    report_lines.append(f"- Ortalama Volatilite: {best_sector['Annual_Volatility']*100:.2f}%")
    report_lines.append(f"- Ortalama Sharpe: {best_sector['Sharpe_Ratio']:.3f}")
    report_lines.append("")
    
    # Risk Warnings
    report_lines.append("## Risk Uyarıları")
    high_risk_stocks = risk_df[risk_df['Risk_Category'] == 'Yüksek Risk']['Name'].tolist()
    if high_risk_stocks:
        report_lines.append("**Yüksek Risk Kategorisindeki Hisseler:**")
        for stock in high_risk_stocks:
            report_lines.append(f"- {stock}")
    report_lines.append("")
    
    # Methodology
    report_lines.append("## Metodoloji")
    report_lines.append("### Risk Skoru Hesaplama")
    report_lines.append("Risk skoru aşağıdaki faktörlerin ağırlıklı ortalamasıdır:")
    report_lines.append("- Yıllık Volatilite (30%)")
    report_lines.append("- Basıklık/Kurtosis (20%)")
    report_lines.append("- Aşırı Hareket Günleri (20%)")
    report_lines.append("- Maksimum Düşüş (20%)")
    report_lines.append("- Value at Risk %95 (10%)")
    report_lines.append("")
    
    report_lines.append("### İstatistiksel Ölçümler")
    report_lines.append("- **Z-Skor:** Standardize edilmiş getiri (|Z| > 2 aşırı hareket)")
    report_lines.append("- **Çarpıklık:** Dağılımın asimetrisi (+ sağa çarpık, - sola çarpık)")
    report_lines.append("- **Basıklık:** Dağılımın kuyruk kalınlığı (yüksek = daha fazla aşırı değer)")
    report_lines.append("- **Sharpe Oranı:** Risk başına getiri (yüksek = daha iyi)")
    report_lines.append("- **VaR %95:** %95 güven aralığında maksimum beklenen kayıp")
    
    # Save report
    with open('reports/summary_report.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))

def main():
    """Main function to run the comprehensive BIST30 analysis."""
    print("=== BIST30 Kapsamlı Risk Analizi ===")
    print(f"Analiz Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*50)
    
    # Download data
    all_data = download_stock_data()
    
    if not all_data:
        print("Hata: Hiç veri indirilemedi!")
        return
    
    # Calculate metrics
    results = calculate_returns_and_metrics(all_data)
    
    if not results:
        print("Hata: Hiç metrik hesaplanamadı!")
        return
    
    print(f"\n✓ {len(results)} hisse senedi için analiz tamamlandı")
    
    # Create risk ranking
    risk_df = create_risk_ranking(results)
    
    # Generate visualizations
    plot_comprehensive_analysis(results, risk_df)
    
    # Create correlation matrix
    correlation_matrix = create_correlation_matrix(results)
    
    # Generate summary report
    generate_summary_report(results, risk_df)
    
    print("\n" + "="*50)
    print("✓ Analiz başarıyla tamamlandı!")
    print("\nOluşturulan dosyalar:")
    print("📊 plots/risk_dashboard.png - Ana risk dashboard")
    print("📊 plots/sector_analysis.png - Sektörel analiz")
    print("📊 plots/individual_distributions.png - Bireysel dağılımlar")
    print("📊 plots/correlation_matrix.png - Korelasyon matrisi")
    print("📋 reports/risk_ranking.csv - Risk sıralaması")
    print("📋 reports/sector_summary.csv - Sektör özeti")
    print("📋 reports/correlation_matrix.csv - Korelasyon verileri")
    print("📄 reports/summary_report.md - Kapsamlı rapor")
    print("\n" + "="*50)

if __name__ == "__main__":
    main() 