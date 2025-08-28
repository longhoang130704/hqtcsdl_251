const XLSX = require('xlsx');
const { Client } = require('pg');

// Cấu hình kết nối database
const dbConfig = {
    user: 'postgres',
    host: 'localhost',
    database: 'hqtcsdl',
    password: '12345678',
    port: 5432,
};

// Đặt đường dẫn chính xác tới file Excel của bạn
const excelFilePath = 'D:/HCMUT-K22/HQTCSDL/btl/data/Radiologists Report.xlsx';




async function importRadiologistReport() {
    let client;
    try {
        console.log('Đang đọc file Excel...');
        const workbook = XLSX.readFile(excelFilePath);
        const sheetName = workbook.SheetNames[0]; // Lấy sheet đầu tiên
        const worksheet = workbook.Sheets[sheetName];
        
        // Chuyển đổi dữ liệu từ sheet thành JSON
        const data = XLSX.utils.sheet_to_json(worksheet, { raw: true });
        
        if (data.length === 0) {
            console.log('Không có dữ liệu trong file Excel.');
            return;
        }

        console.log(`Tìm thấy ${data.length} hàng dữ liệu.`);

        // Kết nối đến database
        client = new Client(dbConfig);
        await client.connect();
        console.log('Đã kết nối thành công tới PostgreSQL.');

        // Bắt đầu giao dịch để đảm bảo tính toàn vẹn dữ liệu
        await client.query('BEGIN');
        
        for (const row of data) {
            // Lấy dữ liệu từ các cột dựa trên tên cột trong file Excel
            const patientIdFromExcel = row['Patient ID'];
            const notesFromExcel = row['Clinician\'s Notes'];
            
            // Xử lý dữ liệu rỗng: nếu giá trị từ Excel là undefined, gán null để chèn vào DB
            const patientId = (patientIdFromExcel === undefined || patientIdFromExcel === '') ? null : patientIdFromExcel;
            const notes = (notesFromExcel === undefined || notesFromExcel === '') ? null : notesFromExcel;

            // Kiểm tra nếu cả hai cột đều rỗng thì bỏ qua hàng đó
            if (patientId === null && notes === null) {
                console.warn('Bỏ qua một hàng vì không có dữ liệu.');
                continue;
            }

            // Câu lệnh SQL để chèn dữ liệu
            const queryText = `
                INSERT INTO patient_notes(patient_id, notes) 
                VALUES($1, $2) 
                ON CONFLICT (patient_id) DO UPDATE SET notes = EXCLUDED.notes;
            `;
            const values = [patientId, notes];
            
            try {
                await client.query(queryText, values);
                console.log(`Đã chèn/cập nhật ghi chú cho Patient ID: ${patientId}.`);
            } catch (err) {
                console.error(`Lỗi khi chèn dữ liệu cho Patient ID ${patientId}:`, err.message);
            }
        }
        
        await client.query('COMMIT');
        console.log('Quá trình nhập dữ liệu hoàn tất.');

    } catch (error) {
        if (client) {
            await client.query('ROLLBACK');
            console.error('Đã xảy ra lỗi, giao dịch đã được ROLLBACK.');
        }
        console.error('Lỗi nghiêm trọng:', error.message);
    } finally {
        if (client) {
            await client.end();
            console.log('Đã đóng kết nối database.');
        }
    }
}

// importRadiologistReport();