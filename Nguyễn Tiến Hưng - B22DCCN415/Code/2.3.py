import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Đọc dữ liệu từ file CSV
data = pd.read_csv('result.csv')

# Xác định các cột chỉ số cần phân tích
metrics = [
    'goals', 'assists', 'xG', 'npxG', 'xAG', 'PrgC', 'PrgP', 'PrgR', 'GA', 'GA90',
    'SoTA', 'Saves', 'Save%', 'W', 'D', 'L', 'CS', 'CS%', 'PKatt', 'PKA', 'PKsv',
    'PKm', 'Sh', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'Dist', 'FK',
    'PK', 'Cmp', 'Att', 'Cmp%', 'TotDist', 'PrgDist', 'Ast', 'xA', 'KP', '1/3',
    'PPA', 'CrsPA', 'PrgP'
]

# Tạo thư mục để lưu các biểu đồ histogram
output_dir = 'histograms'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Vẽ biểu đồ histogram cho mỗi chỉ số của toàn bộ giải đấu
for metric in metrics:
    if metric in data.columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(data[metric].dropna(), kde=True, bins=30)
        plt.title(f'Histogram of {metric} for All Players')
        plt.xlabel(metric)
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.savefig(os.path.join(output_dir, f'{metric}_all_players.png'))
        plt.close()

# Vẽ biểu đồ histogram cho mỗi chỉ số cho từng đội bóng
team_list = data['team'].unique()
for team in team_list:
    team_subset = data[data['team'] == team]
    for metric in metrics:
        if metric in team_subset.columns:
            plt.figure(figsize=(10, 6))
            sns.histplot(team_subset[metric].dropna(), kde=True, bins=30)
            plt.title(f'Histogram of {metric} for {team}')
            plt.xlabel(metric)
            plt.ylabel('Frequency')
            plt.grid(True)
            plt.savefig(os.path.join(output_dir, f'{metric}_{team}.png'))
            plt.close()

print(f"Histograms have been saved in the '{output_dir}' directory.")
