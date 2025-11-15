## Lọc các bệnh nhân lơn tuổi và lấy thêm thông tin hình ảnh (cte)
```sql
WITH older_patients AS (
    SELECT patient_id, age
    FROM patient
    WHERE age > 40
)
SELECT i.img_id, i.modality, p.age
FROM image i
JOIN older_patients p ON p.patient_id = i.patient_id;
```
## Bạn cần tính: Số image mỗi patient & Số series mỗi patient (Có chung nguồn series_study và image)
```sql
WITH img_count AS (
    SELECT patient_id, COUNT(*) AS total_img
    FROM image
    GROUP BY patient_id
),
seri_count AS (
    SELECT patient_id, COUNT(*) AS total_seri
    FROM series_study
    GROUP BY patient_id
)
SELECT p.patient_id, img_count.total_img, seri_count.total_seri
FROM patient p
LEFT JOIN img_count ON p.patient_id = img_count.patient_id
LEFT JOIN seri_count ON p.patient_id = seri_count.patient_id;
```
## Bạn muốn FORCE PostgreSQL phải lưu CTE vào RAM/disk (không inline). CTE Materialize để kiểm soát kế hoạch thực thi
```sql
WITH MATERIALIZED large_series AS (
    SELECT *
    FROM series_study
)
SELECT *
FROM large_series
JOIN image USING (seri_id);
```
## Lấy danh sách image kèm thông tin series và patient
```sql
-- query 1
SELECT i.img_id, s.seri_title, p.age
FROM image i
JOIN series_study s ON i.seri_id = s.seri_id
JOIN patient p ON i.patient_id = p.patient_id
WHERE p.age > 40 AND s.study_title LIKE '%CT%';

-- query 2
SELECT img_id
FROM image
WHERE modality = 'CT' AND body_part = 'HEAD';
```