import pandas as pd

# Đọc dữ liệu từ file CSV
df = pd.read_csv('result.csv')

# In danh sách các cột để kiểm tra
print("Columns in the DataFrame:", df.columns.tolist())

# Hàm để tìm đội bóng có điểm số cao nhất cho mỗi chỉ số
def find_top_team_per_stat(df, column):
    # Chuyển các giá trị không thể chuyển đổi sang số thành NaN
    df[column] = pd.to_numeric(df[column], errors='coerce')

    # Loại bỏ các hàng với giá trị NaN
    df_cleaned = df.dropna(subset=[column])

    # Kiểm tra nếu không có giá trị hợp lệ
    if df_cleaned.empty:
        return None

    # Tìm đội bóng có chỉ số cao nhất
    top_team = df_cleaned.loc[df_cleaned[column].idxmax()][['team', column]]

    return top_team

# Các chỉ số cần phân tích (loại bỏ các cột trùng lặp)
columns_to_analyze = list(set([
    'goals', 'assists', 'xG', 'npxG', 'xAG', 'PrgC', 'PrgP', 'PrgR',
    'GA', 'GA90', 'SoTA', 'Saves', 'Save%', 'W', 'D', 'L', 'CS', 'CS%',
    'PKatt', 'PKA', 'PKsv', 'PKm', 'Sh', 'SoT', 'SoT%', 'Sh/90', 'SoT/90',
    'G/Sh', 'G/SoT', 'Dist', 'FK', 'Cmp', 'Att', 'Cmp%', 'TotDist', 'PrgDist',
    'Ast', 'xA', 'A-xAG', 'KP', '1/3', 'PPA', 'CrsPA', 'Live', 'Dead', 'TB',
    'Sw', 'Crs', 'TI', 'CK', 'In', 'Out', 'Str', 'Off', 'Blocks', 'SCA',
    'SCA90', 'PassLive', 'PassDead', 'TO', 'Fld', 'Def', 'GCA', 'GCA90',
    'Tkl', 'TklW', 'Def 3rd', 'Mid 3rd', 'Att 3rd', 'Att', 'Tkl%', 'Lost',
    'Int', 'Tkl + Int', 'Clr', 'Err', 'Touches', 'Def Pen', 'Att Pen',
    'Succ', 'Succ%', 'Tkld', 'Tkld%', 'Carries', 'ProDist', 'ProgC', 'CPA',
    'Mis', 'Dis', 'Rec', 'Starts', 'Mn/Start', 'Compl', 'Subs', 'Mn/Sub',
    'unSub', 'PPM', 'onG', 'onGA', 'onxG', 'onxGA', 'Fls', 'OG', 'Recov',
    'Won', 'Lost', 'Won%'
]))

# Tạo từ điển để lưu kết quả
results = {}

# Tìm đội bóng có chỉ số cao nhất cho mỗi chỉ số
for column in columns_to_analyze:
    if column in df.columns:
        top_team = find_top_team_per_stat(df, column)
        if top_team is not None:
            results[column] = top_team
        else:
            print(f"No valid data for column '{column}'.")
    else:
        print(f"Column '{column}' does not exist in DataFrame.")

# Hiển thị kết quả
for stat, team in results.items():
    print(f"Team with the highest {stat}:")
    print(team.to_string(index=False))
    print("\n")
