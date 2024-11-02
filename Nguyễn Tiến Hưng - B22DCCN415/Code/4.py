import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_transfer_data(url):
    # Gửi yêu cầu GET tới trang web
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Tìm bảng chuyển nhượng với class phù hợp
    transfer_table = soup.find('table', class_='table')

    if transfer_table is None:
        print("Bảng chuyển nhượng không tìm thấy.")
        return []

    rows = transfer_table.find_all('tr')[1:]  # Bỏ qua tiêu đề bảng

    transfer_data = []

    for row in rows:
        columns = row.find_all('td')
        if len(columns) >= 4:  # Đảm bảo có đủ cột
            player_from = columns[0].get_text(strip=True)
            player_to = columns[1].get_text(strip=True)
            transfer_date = columns[2].get_text(strip=True)
            price = columns[3].get_text(strip=True)

            transfer_data.append({
                'Player From': player_from,
                'Player To': player_to,
                'Date': transfer_date,
                'Price': price
            })

    return transfer_data


# URL của trang web chứa thông tin chuyển nhượng
url = 'https://www.footballtransfers.com/en/transfers/confirmed'
transfer_data = scrape_transfer_data(url)

# Chuyển đổi dữ liệu thành DataFrame
df = pd.DataFrame(transfer_data)

if not df.empty:
    print(df.head())  # Hiển thị 5 dòng đầu tiên của DataFrame
    # Lưu dữ liệu vào file CSV
    df.to_csv('transfers_2023_2024.csv', index=False)
else:
    print("Không có dữ liệu để lưu.")