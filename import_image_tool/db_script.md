## create container
```sh
# create db
docker run -d \
  --name pgvector \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=12345678 \
  -p 5433:5432 \
  ankane/pgvector
```
## create table
```sql
--
CREATE TABLE patient (
    patient_id BIGINT PRIMARY KEY,
    sex VARCHAR(10),                   -- giới tính (tự do nhập)
    age INT,                           -- tuổi
    weight DECIMAL(5,2),               -- cân nặng
    size DECIMAL(5,2),                 -- chiều cao
    note TEXT                          -- ghi chú
);

CREATE TABLE series (
    seri_id BIGINT PRIMARY KEY,           
    study_id VARCHAR(50),                   
    parent_id VARCHAR(50),                 
    seri_link TEXT,                         
    seri_title VARCHAR(255),                
    seri_time TIMESTAMP,                    
    study_link TEXT,                        
    study_title VARCHAR(255),               
    study_time TIMESTAMP
);


-- create vector extension
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE image (
    img_id BIGSERIAL PRIMARY KEY,
    seri_id INT REFERENCES series(seri_id),
    patient_id INT REFERENCES patient(patient_id),
    embedding VECTOR(128),             -- vector 128 chiều
    physical_link TEXT,
    height INT,
    width INT,
    modality VARCHAR(100),             -- thiết bị
    method VARCHAR(255),               -- Scanning Sequence
    ppsd VARCHAR(255),                 -- Performed Procedure Step Description
    type VARCHAR(100),                 -- Image Type
    body_part VARCHAR(100)             -- bộ phận cơ thể
);
--
```