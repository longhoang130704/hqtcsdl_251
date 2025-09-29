# Case study

## 1. CASE 1 :Tìm kiếm thông tin của bệnh nhân khi biết mã bệnh nhân 
( VD bệnh nhân có id là 0003 )
```sql
SELECT p.patient_id , p.sex, p.age, p.weight, p.note, i.physical_link , s.seri_link, s.seri_title ,s.seri_time                                                                                            
FROM series AS s
JOIN patient AS p ON s.parent_id::bigint = p.patient_id 
JOIN image AS i ON i.seri_id= s.seri_id 
WHERE parent_id = '0003'  
ORDER BY seri_time ASC

```

## 2. Tìm kiếm thông tin về những bệnh nhân có note gần giống với note cần tìm (rank score gần bằng 1)
(VD ở đây là Feature of muscle spasm)

```sql
SELECT p.patient_id ,p.sex,  p.age , p.weight, p.size , p.note,
ts_rank(to_tsvector('english', note), plainto_tsquery('english', 'Feature of muscle spasm.')) AS rank_score
FROM patient AS p
WHERE
    to_tsvector('english', note) @@ plainto_tsquery('english', 'Feature of muscle spasm.')
ORDER BY rank_score DESC;

```

## 3. Thiết bị hoặc phương thức nào thường được các bác sĩ sử dụng để chụp
```sql
-- Đối với việc xác định thiết bị thường dùng : 
SELECT modality ,COUNT(modality) 
FROM image 
GROUP BY modality
ORDER BY COUNT(modality);

-- Đối với việc xác định phương thức mà các bác sĩ sử dụng  :
SELECT method ,COUNT(method) 
FROM image 
GROUP BY method
ORDER BY COUNT(method);

```

## 4. Chúng ta biết về thông tin bệnh nhân và chúng ta muốn tìm kiếm những bức ảnh chụp MRI của bệnh nhân đó
(VD ở đây bệnh nhân là nam cao 1m8 , nặng 80 kg và có note)

```sql
SELECT DISTINCT p.patient_id, i.physical_link , s.seri_link, s.seri_title ,s.seri_time 
FROM series AS s 
JOIN patient AS p on s.parent_id::bigint = p.patient_id 
JOIN image as i on i.seri_id= s.seri_id 
WHERE Trim(p.sex) = 'M' and 
	  p.age='27' and 
	  p.weight='80.00' and 
	  p.size='1.80' and
      REGEXP_REPLACE(note, E'[[:space:]]', '', 'g')  = 
      REGEXP_REPLACE('LSS MRI Features of muscle spasm. small central  disc protrusion noted at L5-S1 level abutting the thecal sac. no significant thecal  sac or nerve root compression noted.', E'[[:space:]]', '', 'g')

```

## 5. Bác sỹ có hình ảnh tổng quát, cần xem thêm hình ảnh chi tiết để có thể chẩn đoán chính xác bệnh.
```sql
SELECT physical_link, embedding <-> %s AS distance
FROM image
ORDER BY distance ASC
LIMIT 20;
```
