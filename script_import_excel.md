# create table
```sql
CREATE TABLE patient_notes (
    patient_id INTEGER PRIMARY KEY,
    notes TEXT
);
```

# check import data is right
```sql
select count(*) from patient_notes;
```