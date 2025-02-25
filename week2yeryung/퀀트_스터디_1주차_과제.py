# -*- coding: utf-8 -*-
"""퀀트 스터디 1주차 과제

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pXdEni0D3GNGL7SjycBbDxfojo3zfqMq
"""

import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. 포트폴리오 자산 및 비율 설정
assets = ["AAPL", "MSFT", "NVDA", "AMZN", "GLD"]  # 테크 주식 + 금 ETF
weights = [0.30, 0.25, 0.20, 0.15, 0.10]  # 30%, 25%, 20%, 15%, 10%
initial_investment = 1_000_000  # 1백만 달러

# 2. 2015년부터 현재까지 데이터 다운로드
start_date = "2015-01-01"
end_date = "2025-01-01"
data = yf.download(assets, start=start_date, end=end_date)

# Access 'Adj Close' if it exists, otherwise use 'Close'
data = data["Adj Close"] if "Adj Close" in data.columns else data["Close"]

# 결측치 제거
data.dropna(inplace=True)

# 3. 자산별 초기 투자 금액 계산
initial_allocations = [initial_investment * weight for weight in weights]
print("초기 자산 배분:")
for asset, allocation in zip(assets, initial_allocations):
    print(f"{asset}: ${allocation:,.2f}")

# 4. 일간 수익률 계산
daily_returns = data.pct_change().dropna()

# 5. 가중 포트폴리오 수익률 계산
portfolio_daily_returns = (daily_returns * weights).sum(axis=1)
portfolio_cumulative_returns = (1 + portfolio_daily_returns).cumprod()

# 6. 개별 자산 및 포트폴리오의 누적 수익 분석
individual_cumulative_returns = (1 + daily_returns).cumprod()

# 7. Maximum Drawdown(MDD) 및 총 수익률 계산 함수
def calculate_metrics(prices):
    normalized = prices / prices.iloc[0]
    cumulative_max = np.maximum.accumulate(normalized)
    drawdown = (normalized - cumulative_max) / cumulative_max
    max_drawdown = drawdown.min()
    total_return = (normalized.iloc[-1] - 1) * 100
    return max_drawdown * 100, total_return, drawdown

# 8. 개별 자산 및 포트폴리오 분석
results = {}
drawdown_data = {}

for asset in assets:
    mdd, total_return, drawdown = calculate_metrics(data[asset])
    results[asset] = {"MDD": mdd, "Total Return": total_return}
    drawdown_data[asset] = drawdown

# 포트폴리오 분석
portfolio_mdd, portfolio_total_return, portfolio_drawdown = calculate_metrics(portfolio_cumulative_returns)
results["Portfolio"] = {"MDD": portfolio_mdd, "Total Return": portfolio_total_return}
drawdown_data["Portfolio"] = portfolio_drawdown

# 9. 결과 출력
print("\n금융상품별 분석 결과:")
for asset, metrics in results.items():
    print(f"{asset}: 최대 낙폭 (MDD): {metrics['MDD']:.2f}%, 총 수익률: {metrics['Total Return']:.2f}%")

# 10. 시각화
fig, axes = plt.subplots(len(assets) * 2 + 2, 1, figsize=(12, 6 * (len(assets) + 1)),
                         gridspec_kw={'height_ratios': [3, 1] * (len(assets) + 1)})

axes = axes.flatten()

# 개별 자산 성과 및 MDD 차트
for i, asset in enumerate(assets):
    main_ax = axes[i * 2]  # 성과 차트
    sub_ax = axes[i * 2 + 1]  # MDD 차트

    # 성과 차트
    main_ax.plot(data[asset], label=f"{asset} Adjusted Close", color='blue')
    main_ax.set_title(f"{asset} Performance")
    main_ax.set_xlabel("Date")
    main_ax.set_ylabel("Price (USD)")
    main_ax.legend(loc='upper left')
    main_ax.grid()

    # MDD 차트
    sub_ax.plot(drawdown_data[asset] * 100, label=f"{asset} Drawdown", color='red')
    sub_ax.set_title(f"{asset} Maximum Drawdown (MDD)")
    sub_ax.set_xlabel("Date")
    sub_ax.set_ylabel("Drawdown (%)")
    sub_ax.legend(loc='upper left')
    sub_ax.grid()

# 포트폴리오 성과 및 MDD 차트
portfolio_index = len(assets) * 2
main_ax = axes[portfolio_index]
sub_ax = axes[portfolio_index + 1]

# 포트폴리오 성과 차트
main_ax.plot(portfolio_cumulative_returns, label="Portfolio Cumulative Returns", color='green', linewidth=2)
main_ax.set_title("Portfolio Performance")
main_ax.set_xlabel("Date")
main_ax.set_ylabel("Cumulative Returns")
main_ax.legend(loc='upper left')
main_ax.grid()

# 포트폴리오 MDD 차트
sub_ax.plot(portfolio_drawdown * 100, label="Portfolio Drawdown", color='red')
sub_ax.set_title("Portfolio Maximum Drawdown (MDD)")
sub_ax.set_xlabel("Date")
sub_ax.set_ylabel("Drawdown (%)")
sub_ax.legend(loc='upper left')
sub_ax.grid()

plt.tight_layout()
plt.show()

import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. 포트폴리오 자산 및 비율 설정
assets = ["AAPL", "AMZN", "GOOGL", "NFLX", "GLD"]  # 요구된 포트폴리오 구성
weights = [0.30, 0.25, 0.20, 0.15, 0.10]  # 요구된 비율
initial_investment = 1_000_000  # 1백만 달러

# 2. 데이터 다운로드 (2015년부터 현재까지)
start_date = "2015-01-01"
end_date = "2025-01-01"

# Yahoo Finance에서 데이터 다운로드
yahoo_data = yf.download(assets, start=start_date, end=end_date)
# Access 'Adj Close' if it exists, otherwise use 'Close'
yahoo_data = yahoo_data["Adj Close"] if "Adj Close" in yahoo_data.columns else yahoo_data["Close"]

# 결측치 제거
yahoo_data.dropna(inplace=True)

# 3. 자산별 초기 투자 금액 계산
initial_allocations = [initial_investment * weight for weight in weights]
print("초기 자산 배분:")
for asset, allocation in zip(assets, initial_allocations):
    print(f"{asset}: ${allocation:,.2f}")

# 4. 일간 및 누적 수익률 계산
daily_returns = yahoo_data.pct_change().dropna()
portfolio_daily_returns = (daily_returns * weights).sum(axis=1)
portfolio_cumulative_returns = (1 + portfolio_daily_returns).cumprod()
individual_cumulative_returns = (1 + daily_returns).cumprod()

# 5. Maximum Drawdown(MDD) 및 총 수익률 계산
def calculate_metrics(prices):
    normalized = prices / prices.iloc[0]
    cumulative_max = np.maximum.accumulate(normalized)
    drawdown = (normalized - cumulative_max) / cumulative_max
    max_drawdown = drawdown.min()
    total_return = (normalized.iloc[-1] - 1) * 100
    return max_drawdown * 100, total_return, drawdown

# 개별 자산 및 포트폴리오 분석
results = {}
drawdown_data = {}
for asset in yahoo_data.columns:
    mdd, total_return, drawdown = calculate_metrics(yahoo_data[asset])
    results[asset] = {"MDD": mdd, "Total Return": total_return}
    drawdown_data[asset] = drawdown

# 포트폴리오 분석
portfolio_mdd, portfolio_total_return, portfolio_drawdown = calculate_metrics(portfolio_cumulative_returns)
results["Portfolio"] = {"MDD": portfolio_mdd, "Total Return": portfolio_total_return}
drawdown_data["Portfolio"] = portfolio_drawdown

# 6. 결과 출력
print("\n금융상품별 분석 결과:")
for asset, metrics in results.items():
    print(f"{asset}: 최대 낙폭 (MDD): {metrics['MDD']:.2f}%, 총 수익률: {metrics['Total Return']:.2f}%")

# 7. 시각화
fig, axes = plt.subplots(len(assets) * 2 + 2, 1, figsize=(12, 6 * (len(assets) + 1)),
                         gridspec_kw={'height_ratios': [3, 1] * (len(assets) + 1)})

axes = axes.flatten()

# 개별 자산 성과 및 MDD 차트
for i, asset in enumerate(assets):
    main_ax = axes[i * 2]  # 성과 차트
    sub_ax = axes[i * 2 + 1]  # MDD 차트

    # 성과 차트
    main_ax.plot(yahoo_data[asset], label=f"{asset} Adjusted Close", color='blue')
    main_ax.set_title(f"{asset} Performance")
    main_ax.set_xlabel("Date")
    main_ax.set_ylabel("Price (USD)")
    main_ax.legend(loc='upper left')
    main_ax.grid()

    # MDD 차트
    sub_ax.plot(drawdown_data[asset] * 100, label=f"{asset} Drawdown", color='red')
    sub_ax.set_title(f"{asset} Maximum Drawdown (MDD)")
    sub_ax.set_xlabel("Date")
    sub_ax.set_ylabel("Drawdown (%)")
    sub_ax.legend(loc='upper left')
    sub_ax.grid()

# 포트폴리오 성과 및 MDD 차트
portfolio_index = len(assets) * 2
main_ax = axes[portfolio_index]
sub_ax = axes[portfolio_index + 1]

# 포트폴리오 성과 차트
main_ax.plot(portfolio_cumulative_returns, label="Portfolio Cumulative Returns", color='green', linewidth=2)
main_ax.set_title("Portfolio Performance")
main_ax.set_xlabel("Date")
main_ax.set_ylabel("Cumulative Returns")
main_ax.legend(loc='upper left')
main_ax.grid()

# 포트폴리오 MDD 차트
sub_ax.plot(portfolio_drawdown * 100, label="Portfolio Drawdown", color='red')
sub_ax.set_title("Portfolio Maximum Drawdown (MDD)")
sub_ax.set_xlabel("Date")
sub_ax.set_ylabel("Drawdown (%)")
sub_ax.legend(loc='upper left')
sub_ax.grid()

plt.tight_layout()
plt.show()



