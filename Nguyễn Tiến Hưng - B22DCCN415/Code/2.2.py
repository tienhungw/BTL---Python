import pandas as pd


def get_statistics_from_csv(csv_file):
    # Đọc dữ liệu từ tệp CSV
    df = pd.read_csv(csv_file)

    # In danh sách các cột để kiểm tra tên cột
    print("Các cột trong DataFrame:", df.columns.tolist())

    # Đảm bảo rằng cột 'team' tồn tại
    if 'team' not in df.columns:
        raise KeyError("Cột 'team' không tồn tại trong DataFrame.")

    # Tìm kiếm các cột kiểu số và đưa vào danh sách
    numeric_columns = df.select_dtypes(include=['number'])
    numeric_columns_list = numeric_columns.columns.tolist()

    # Tìm trung vị của mỗi chỉ số của toàn cầu thủ
    median_all = numeric_columns.median().round(2)

    # Tìm trung bình và độ lệch chuẩn của mỗi chỉ số của toàn cầu thủ
    mean_all = numeric_columns.mean().round(2)
    std_all = numeric_columns.std().round(2)

    # Gộp tất cả thành 1 bảng
    overall_df = pd.DataFrame({
        'STT': [0],
        'team': ['all'],
        **{f'Median of {col}': [median_all[col]] for col in numeric_columns_list},
        **{f'Mean of {col}': [mean_all[col]] for col in numeric_columns_list},
        **{f'Std of {col}': [std_all[col]] for col in numeric_columns_list}
    })

    # Tìm trung vị của mỗi chỉ số theo đội
    median_team = df.groupby('team')[numeric_columns_list].median().round(2)

    # Tìm trung bình và độ lệch chuẩn của mỗi chỉ số theo đội
    mean_team = df.groupby('team')[numeric_columns_list].mean().round(2)
    std_team = df.groupby('team')[numeric_columns_list].std().round(2)

    # Gộp các bảng này thành 1 bảng
    team_df = pd.DataFrame({
        'STT': range(1, len(median_team) + 1),
        'team': median_team.index,
        **{f'Median of {col}': median_team[col].values for col in numeric_columns_list},
        **{f'Mean of {col}': mean_team[col].values for col in numeric_columns_list},
        **{f'Std of {col}': std_team[col].values for col in numeric_columns_list}
    })

    # Gộp hai bảng thành 1 và ghi dữ liệu vào file results22.csv
    final_df = pd.concat([overall_df, team_df], ignore_index=True)
    final_df.to_csv('results2.csv', index=False)

    # Đọc và in nội dung của file CSV để kiểm tra
    print(pd.read_csv("results2.csv"))


# Đọc và xử lý dữ liệu từ tệp result.csv
get_statistics_from_csv('result.csv')