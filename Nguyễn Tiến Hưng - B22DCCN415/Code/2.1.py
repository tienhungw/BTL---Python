import pandas as pd

# Đọc dữ liệu từ file CSV
df = pd.read_csv('result.csv')

# In danh sách các cột để kiểm tra
print("Columns in the DataFrame:", df.columns.tolist())

# Hàm tìm top 3 cầu thủ có điểm cao nhất và thấp nhất cho mỗi chỉ số
def get_top_and_bottom(df, metric):
    # Chuyển các giá trị không thể chuyển đổi thành số thành NaN
    df[metric] = pd.to_numeric(df[metric], errors='coerce')

    # Loại bỏ các hàng chứa giá trị NaN trong cột được phân tích
    df_valid = df.dropna(subset=[metric])

    # Tìm top 3 cầu thủ có điểm cao nhất
    top_3 = df_valid.nlargest(3, metric)[['player', 'team', 'nationality', 'position', 'age', metric]]

    # Tìm top 3 cầu thủ có điểm thấp nhất
    bottom_3 = df_valid.nsmallest(3, metric)[['player', 'team', 'nationality', 'position', 'age', metric]]

    return top_3, bottom_3

# Các chỉ số cần phân tích
stats_to_check = [
    'goals', 'assists', 'xG', 'npxG', 'xAG', 'PrgC', 'PrgP', 'PrgR',
    'GA', 'GA90', 'SoTA', 'Saves', 'Save%', 'W', 'D', 'L', 'CS', 'CS%',
    'PKatt', 'PKA', 'PKsv', 'PKm', 'Save%',
    'Sh', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'Dist', 'FK', 'PK', 'PKatt',
    'Cmp', 'Att', 'Cmp%', 'TotDist', 'PrgDist', 'Ast', 'xA', 'A-xAG', 'KP', '1/3', 'PPA', 'CrsPA', 'PrgP',
    'Live', 'Dead', 'FK', 'TB', 'Sw', 'Crs', 'TI', 'CK',
    'In', 'Out', 'Str', 'Cmp', 'Off', 'Blocks',
    'SCA', 'SCA90', 'PassLive', 'PassDead', 'TO', 'Sh', 'Fld', 'Def',
    'GCA', 'GCA90', 'PassLive', 'PassDead', 'TO', 'Sh', 'Fld', 'Def',
    'Tkl', 'TklW', 'Def 3rd', 'Mid 3rd', 'Att 3rd', 'Tkl', 'Att', 'Tkl%', 'Lost',
    'Blocks', 'Sh', 'Pass', 'Int', 'Tkl + Int', 'Clr', 'Err',
    'Touches', 'Def Pen', 'Def 3rd', 'Mid 3rd', 'Att 3rd', 'Att Pen', 'Live',
    'Att', 'Succ', 'Succ%', 'Tkld', 'Tkld%',
    'Carries', 'TotDist', 'ProDist', 'ProgC', '1/3', 'CPA', 'Mis', 'Dis',
    'Rec', 'PrgR', 'Starts', 'Mn/Start', 'Compl', 'Subs', 'Mn/Sub', 'unSub', 'PPM', 'onG', 'onGA',
    'onxG', 'onxGA', 'Fls', 'Fld', 'Off', 'Crs', 'OG', 'Recov',
    'Won', 'Lost', 'Won%'
]

# Tạo từ điển để lưu kết quả phân tích
analysis_results = {}

# Lặp qua các chỉ số để phân tích
for stat in stats_to_check:
    if stat in df.columns:
        top, bottom = get_top_and_bottom(df, stat)
        analysis_results[stat] = {
            'top': top,
            'bottom': bottom
        }
    else:
        print(f"Column '{stat}' does not exist in DataFrame.")

# Hiển thị kết quả
for stat, players in analysis_results.items():
    print(f"Top 3 players for {stat}:")
    print(players['top'].to_string(index=False))
    print(f"Bottom 3 players for {stat}:")
    print(players['bottom'].to_string(index=False))
    print("\n")
