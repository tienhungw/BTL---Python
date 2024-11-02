import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Bước 1: Đọc dữ liệu từ tệp CSV
data = pd.read_csv('result.csv')

# Bước 2: Chọn các chỉ số cần thiết để phân loại
features = data[['non-Penalty Goals', 'Penalty Goals', 'assists', 'minutes']]

# Xóa các hàng có giá trị NaN (nếu có) mà không gây ra cảnh báo
features = features.dropna()

# Bước 3: Tính WCSS cho các giá trị K khác nhau
wcss = []
for i in range(1, 11):  # Thử K từ 1 đến 10
    kmeans = KMeans(n_clusters=i, random_state=42)
    kmeans.fit(features)
    wcss.append(kmeans.inertia_)

# Bước 4: Vẽ biểu đồ Elbow
plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), wcss, marker='o')
plt.title('Phương pháp Elbow để xác định số lượng cụm')
plt.xlabel('Số lượng cụm (K)')
plt.ylabel('WCSS')
plt.xticks(range(1, 11))
plt.grid()
plt.show()

# Bước 5: Chọn số lượng cụm K tối ưu (ví dụ: K=3)
K = 3  # Điều chỉnh số lượng cụm tùy theo kết quả biểu đồ Elbow

# Bước 6: Khởi tạo mô hình K-means
kmeans = KMeans(n_clusters=K, random_state=42)

# Bước 7: Huấn luyện mô hình và dự đoán các nhãn
clusters = kmeans.fit_predict(features)

# Bước 8: Thêm nhãn cụm vào DataFrame gốc
data['Cluster'] = clusters

# Bước 9: Hiển thị kết quả
print(data[['player', 'Cluster']])

# Bước 10: Trực quan hóa
plt.figure(figsize=(10, 6))
plt.scatter(data['non-Penalty Goals'], data['assists'], c=data['Cluster'], cmap='viridis', marker='o')
plt.title('Phân loại cầu thủ theo K-means')
plt.xlabel('Non-Penalty Goals')
plt.ylabel('Assists')
plt.colorbar(label='Cluster')
plt.show()