import os
import psycopg2
import SimpleITK as sitk
import numpy as np
import torch
import numpy as np
import torch
import torch.nn.functional as F
import SimpleITK as sitk
import psycopg2
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

# Kết nối database
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="12345678",
    host="localhost",
    port="5433"
)
cur = conn.cursor()

# Thư mục gốc chứa dữ liệu MRI
base_dir = r"D:/HCMUT-K22/HQTCSDL/btl/data/MRI_Data/01_MRI_Data"

# Duyệt từng bệnh nhân (patient)
for patient_id in os.listdir(base_dir):
    patient_path = os.path.join(base_dir, patient_id)
    if not os.path.isdir(patient_path):
        continue
    
    patient_sex    = ""
    patient_age    = ""
    patient_weight = ""
    patient_size   = ""
    seri_id = 0

    # Duyệt từng study
    for study_title in os.listdir(patient_path):
        study_path = os.path.join(patient_path, study_title)
        print(study_path)
        if not os.path.isdir(study_path):
            continue

        study_id = f"{patient_id}_{study_title}"  # tự tạo study_id

        # Duyệt từng series
        for seri_title in os.listdir(study_path):
            seri_path = os.path.join(study_path, seri_title)
            print(seri_path)
            if not os.path.isdir(seri_path):
                continue

            seri_id = seri_id + 1

            # Insert series nếu chưa có
            cur.execute("""
                INSERT INTO series (seri_id, study_id, parent_id,
                                    seri_link, seri_title, study_link, study_title)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (seri_id) DO NOTHING;
            """, (
                seri_id,
                study_id,
                patient_id,
                seri_path,
                seri_title,
                study_path,
                study_title
            ))

# ------------------ debug only ------------------
            # print("seri_record inserted: " + 
            #     str(seri_id) + " - " + 
            #     seri_title + " - " + 
            #     seri_path + " - " + 
            #     study_id + " - " + 
            #     study_title + " - " + 
            #     patient_id)
# ------------------ debug only ------------------

            # Duyệt từng ảnh trong series
            for img_file in os.listdir(seri_path):
                if not img_file.endswith(".ima"):
                    continue

                img_path = os.path.join(seri_path, img_file)

                try:
                    # Đọc ảnh bằng SimpleITK
                    image = sitk.ReadImage(img_path)
                    size = image.GetSize()   # (width, height, depth)
                    width, height = size[0], size[1]

                    # Metadata
                    modality       = image.GetMetaData("0008|0060") if image.HasMetaDataKey("0008|0060") else None
                    method         = image.GetMetaData("0018|0020") if image.HasMetaDataKey("0018|0020") else None
                    body_part      = image.GetMetaData("0018|0015") if image.HasMetaDataKey("0018|0015") else None
                    patient_sex    = image.GetMetaData("0010|0040") if image.HasMetaDataKey("0010|0040") else None
                    patient_age    = image.GetMetaData("0010|1010").strip('Y') if image.HasMetaDataKey("0010|1010") else None
                    patient_weight = image.GetMetaData("0010|1030") if image.HasMetaDataKey("0010|1030") else None
                    patient_size   = image.GetMetaData("0010|1020") if image.HasMetaDataKey("0010|1020") else None

                    # ==== Tạo embedding 128 chiều ====
                    tensor = load_ima(img_path)
                    embedding = get_embedding(tensor)

                    # Insert vào bảng image
                    cur.execute("""
                        INSERT INTO image (seri_id, patient_id, embedding,
                                            physical_link, height, width,
                                            modality, method, body_part)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        seri_id,
                        patient_id,
                        embedding.tolist(),  # chuyển numpy array sang list
                        img_path,
                        height,
                        width,
                        modality,
                        method,
                        body_part
                    ))

# ------------------ debug only ------------------
                    # print("image_record inserted: " + 
                    #     str(seri_id) + " - " + 
                    #     patient_id + " - " + 
                    #     str(height) + " - " + 
                    #     str(width) + " - " + 
                    #     str(modality) + " - " + 
                    #     str(method) + " - " + 
                    #     str(body_part) + " - " + 
                    #     img_path + " - " + 
                    #     str(embedding[:3]) + "...")
# ------------------ debug only ------------------

                except Exception as e:
                    print(f"⚠️ Lỗi khi đọc {img_path}: {e}")
# ------------------ debug only ------------------
            # print(f"✅ Xong img {img_path}")
            # break
        # print(f"✅ Xong study {study_id}")
        # break
    # print("Patient info: " + 
    #     str(patient_id) + " - " +
    #     str(patient_sex) + " - " +
    #     str(patient_age) + " - " +
    #     str(patient_weight) + " - " +
    #     str(patient_size))
    cur.execute("""
        UPDATE patient
        SET
            sex = %s,
            age = %s,
            weight = %s,
            size = %s
        WHERE patient_id = %s;
    """, (
        patient_sex, 
        patient_age, 
        patient_weight, 
        patient_size, 
        patient_id
    ))
    # print(f"✅ Xong patient {patient_id}")
    # break
# ------------------ debug only ------------------

# Commit và đóng kết nối
conn.commit()
cur.close()
conn.close()
print("✅ Import xong dữ liệu MRI vào database!")
