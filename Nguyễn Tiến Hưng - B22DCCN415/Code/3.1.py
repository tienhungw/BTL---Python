import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Bước 1: Đọc dữ liệu từ tệp CSV
data = pd.read_csv('result.csv')

# Hiển thị các cột có thể được sử dụng để phân loại
print(data.columns)

# Bước 2: Chọn các chỉ số cần thiết để phân loại
# Giả sử các cột bạn muốn sử dụng là 'non-Penalty Goals', 'Penalty Goals', 'assists', 'minutes'
features = data[['non-Penalty Goals', 'Penalty Goals', 'assists', 'minutes']]

# Xóa các hàng có giá trị NaN (nếu có)
features.dropna(inplace=True)

# Bước 3: Chọn số lượng cụm K
K = 3  # Bạn có thể điều chỉnh giá trị này tùy theo nhu cầu

# Bước 4: Khởi tạo mô hình K-means
kmeans = KMeans(n_clusters=K, random_state=42)

# Bước 5: Huấn luyện mô hình và dự đoán các nhãn
clusters = kmeans.fit_predict(features)

# Bước 6: Thêm nhãn cụm vào DataFrame gốc
data['Cluster'] = clusters

# Bước 7: Hiển thị kết quả
print(data[['player', 'Cluster']])

# Bước 8: Trực quan hóa
plt.figure(figsize=(10, 6))
plt.scatter(data['non-Penalty Goals'], data['assists'], c=data['Cluster'], cmap='viridis', marker='o')
plt.title('Phân loại cầu thủ theo K-means')
plt.xlabel('Non-Penalty Goals')
plt.ylabel('Assists')
plt.colorbar(label='Cluster')
plt.show()