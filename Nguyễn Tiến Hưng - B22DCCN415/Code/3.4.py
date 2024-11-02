import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse


def radar_chart(player1, player2, attributes):
    # Tải dữ liệu từ file CSV
    data = pd.read_csv('result.csv')

    # Lấy chỉ số của từng cầu thủ
    p1_data = data[data['player'] == player1][attributes].values.flatten()
    p2_data = data[data['player'] == player2][attributes].values.flatten()

    # Kiểm tra xem cầu thủ có tồn tại trong dữ liệu không
    if len(p1_data) == 0 or len(p2_data) == 0:
        print(f"Không tìm thấy thông tin cho cầu thủ {player1} hoặc {player2}.")
        return

    # Số lượng chỉ số
    num_vars = len(attributes)

    # Tạo một mảng góc cho mỗi chỉ số
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Đảm bảo biểu đồ khép kín
    p1_data = np.concatenate((p1_data, [p1_data[0]]))
    p2_data = np.concatenate((p2_data, [p2_data[0]]))
    angles += angles[:1]

    # Vẽ biểu đồ radar
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.fill(angles, p1_data, color='blue', alpha=0.25, label=player1)
    ax.fill(angles, p2_data, color='orange', alpha=0.25, label=player2)

    # Thiết lập các nhãn và tiêu đề
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(attributes)
    ax.set_title(f'So sánh giữa {player1} và {player2}', size=15, color='black', weight='bold')
    ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    plt.show()


if __name__ == '__main__':
    # Nhập tên cầu thủ và các chỉ số từ người dùng
    player1 = input("Nhập tên cầu thủ thứ nhất: ")
    player2 = input("Nhập tên cầu thủ thứ hai: ")
    attributes_input = input("Nhập các chỉ số cần so sánh, phân cách bằng dấu phẩy (ví dụ: goals,assists,passes): ")

    # Chia danh sách các chỉ số thành một danh sách
    attributes = [attr.strip() for attr in attributes_input.split(',')]

    # Vẽ biểu đồ radar
    radar_chart(player1, player2, attributes)