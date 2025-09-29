import os
import psycopg2
import SimpleITK as sitk
import numpy as np
import torch
import numpy as np
import torch
import torch.nn.functional as F
import SimpleITK as sitk
from monai.networks.nets import resnet10
# -----------------------------
# 1. Load .ima file
# -----------------------------
def load_ima(path):
    image = sitk.ReadImage(path)
    array = sitk.GetArrayFromImage(image)  # numpy [D,H,W]
    array = (array - np.min(array)) / (np.max(array) - np.min(array) + 1e-8)  # normalize 0-1
    tensor = torch.tensor(array).unsqueeze(0).unsqueeze(0).float()  # [1,1,D,H,W]
    tensor = F.interpolate(tensor, size=(128, 128, 128), mode="trilinear")   # resize
    return tensor

# -----------------------------
# 2. Get embedding with MONAI ResNet3D
# -----------------------------
def get_embedding(tensor):
    model = resnet10(spatial_dims=3, n_input_channels=1, num_classes=128)
    model.eval()
    with torch.no_grad():
        embedding = model(tensor)  # [1,128]
    return embedding.squeeze().numpy()

def search_similar_images(img_path, top_k=5):
    # 1. Tính embedding cho ảnh query
    tensor = load_ima(img_path)
    query_embedding = get_embedding(tensor)   # numpy (128,)
    query_list = query_embedding.tolist()
    query_str = "[" + ",".join([str(x) for x in query_list]) + "]"

    # 2. Kết nối database
    conn = psycopg2.connect(
		dbname="postgres",
		user="postgres",
		password="12345678",
		host="localhost",
		port="5433"
	)
    cur = conn.cursor()

    # 3. Query tìm top-k ảnh gần nhất
    cur.execute(f"""
        SELECT physical_link, embedding <-> %s AS distance
        FROM image
        ORDER BY distance ASC
        LIMIT {top_k};
    """, (query_str,))
    
    results = cur.fetchall()

    # 4. Đóng kết nối
    cur.close()
    conn.close()

    return results


# ------------------- demo -------------------
# path = r"D:\HCMUT-K22\HQTCSDL\btl\data\MRI_Data\01_MRI_Data\0001\L-SPINE_LSS_20160309_091629_240000\T1_TSE_TRA_0005\T1_TSE_TRA__0001_001.ima"
path = r"D:\HCMUT-K22\HQTCSDL\btl\data\MRI_Data\01_MRI_Data\0001\L-SPINE_LSS_20160309_091629_240000\LOCALIZER_0001\LOCALIZER_0_0001_001.ima"
results = search_similar_images(path, top_k=20)
for r in results:
    print(r)




