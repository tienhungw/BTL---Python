import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Bước 1: Tải dữ liệu
# Giả sử bạn đã có dữ liệu trong file 'result.csv'
data = pd.read_csv('result.csv')

# Bước 2: Lựa chọn các cột để phân tích
# Giả sử bạn sẽ sử dụng các chỉ số như goals, assists, minutes...
features = data[['non-Penalty Goals', 'Penalty Goals', 'assists', 'minutes']]

# Bước 3: Chuẩn hóa dữ liệu
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Bước 4: Áp dụng PCA
pca = PCA(n_components=2)
principal_components = pca.fit_transform(features_scaled)

# Tạo DataFrame cho các thành phần chính
principal_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

# Bước 5: Phân cụm dữ liệu
# Giả sử bạn đã xác định số nhóm từ phương pháp Elbow, ở đây là 3
kmeans = KMeans(n_clusters=3)
data['Cluster'] = kmeans.fit_predict(features_scaled)

# Bước 6: Vẽ biểu đồ phân cụm
plt.figure(figsize=(10, 6))
plt.scatter(principal_df['PC1'], principal_df['PC2'], c=data['Cluster'], cmap='viridis', edgecolor='k', s=100)
plt.title('PCA: Phân Cụm Cầu Thủ Trên Mặt Phẳng 2D')
plt.xlabel('Thành Phần Chính 1 (PC1)')
plt.ylabel('Thành Phần Chính 2 (PC2)')
plt.colorbar(label='Nhóm Cầu Thủ')
plt.grid(True)
plt.show()