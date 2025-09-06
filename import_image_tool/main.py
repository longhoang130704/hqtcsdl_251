# path = r"D:/HCMUT-K22/HQTCSDL/btl/data/MRI_Data/01_MRI_Data/0008/L-SPINE_CLINICAL_LIBRARIES_20160605_112202_964000/LOCALIZER_0001/LOCALIZER_0_0008_001.ima"
# path = r"D:\HCMUT-K22\HQTCSDL\btl\data\MRI_Data\01_MRI_Data\0008\L-SPINE_CLINICAL_LIBRARIES_20160605_112202_964000\LOCALIZER_0001\LOCALIZER_0_0008_002.ima"
# path = r"D:\HCMUT-K22\HQTCSDL\btl\data\MRI_Data\01_MRI_Data\0008\L-SPINE_CLINICAL_LIBRARIES_20160605_112202_964000\T1_TSE_SAG_320_0004\T1_TSE_SAG__0008_001.ima"
# path = r"D:\HCMUT-K22\HQTCSDL\btl\data\MRI_Data\01_MRI_Data\0001\L-SPINE_LSS_20160309_091629_240000\T2_TSE_SAG_384_0002\T2_TSE_SAG__0001_001.ima"
# path = r"D:\HCMUT-K22\HQTCSDL\btl\data\MRI_Data\01_MRI_Data\0002\L-SPINE_CLINICAL_LIBRARIES_20160621_112938_873000\LOCALIZER_0001\LOCALIZER_0_0002_001.ima"
path = r"D:\HCMUT-K22\HQTCSDL\btl\data\MRI_Data\01_MRI_Data\0069\L-SPINE_LSS_20151130_081056_708000\LOCALIZER_0001\LOCALIZER_0_0069_001.ima"

import pydicom

# đọc file .ima
dcm = pydicom.dcmread(path)

# lấy ảnh dưới dạng numpy array
# img = dcm.pixel_array
# print(img.shape)

print(dcm)


# import os
# import numpy as np
# import pydicom

# folder = r"D:\HCMUT-K22\HQTCSDL\btl\data\MRI_Data\01_MRI_Data\0008\L-SPINE_CLINICAL_LIBRARIES_20160605_112202_964000\LOCALIZER_0001"

# slices = []
# for f in sorted(os.listdir(folder)):
#     if f.endswith(".ima"):
#         dcm = pydicom.dcmread(os.path.join(folder, f))
#         slices.append(dcm)

# volume = np.stack(slices, axis=-1)  # (height, width, số slice)
# print(volume.shape)

# for ele in slices:
#     print(ele.PatientName)
#     print(ele.PatientSex)
