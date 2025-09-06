# Instruction

## 1. Install dependency
```sh
python -m venv venv
pip install -r requirements.txt
```
## 2. Create container && db
```sh
# create db
docker run -d \
  --name pgvector \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=12345678 \
  -p 5433:5432 \
  ankane/pgvector
```
## 3. Create db name: "hqtcsdl"
```
run db_script.mb
```
## 4. Import text before image 
```txt
import text before import image
1. create container
2. create db: "hqtcsdl"
3. create table
4. import text
5. import image
```
## 5. Gg sheet phân công nhiệm vụ
```
https://docs.google.com/spreadsheets/d/1hS-_YQi27MtEl6X23bmODDbj0iMJxvFEgNwssJnIAXQ/edit?gid=0#gid=0
```