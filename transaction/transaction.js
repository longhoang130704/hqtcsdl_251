// Start a session.
session = db.getMongo().startSession({ readPreference: { mode: "primary" } });
coll1 = session.getDatabase("hqtcsdl").patient;
coll2 = session.getDatabase("hqtcsdl").series;
coll3 = session.getDatabase("hqtcsdl").image;
function InsertPatientAndSeries(patient_id, weight, seri_id, study_id) {
  session.startTransaction({
    readConcern: { level: "local" },
    writeConcern: { w: "majority" },
  });
  // Operations inside the transaction
  try {
    patient = coll1.findOne({ patient_id: patient_id });
    if (patient) {
      throw new Error("Patient already exists");
    }
    coll1.insertOne({ patient_id: patient_id, weight: weight });
    series = coll2.findOne({ study_id: study_id });
    if (series) {
      throw new Error("Series already exists");
    }
    coll2.insertOne({
      seri_id: seri_id,
      study_id: study_id,
      parent_id: patient_id,
      seri_link: "",
      seri_title: "",
      study_link: "",
      study_title: "",
    });
  } catch (error) {
    // Abort transaction on error
    session.abortTransaction();
    throw error;
  }
  // Commit the transaction using write concern set at transaction start
  session.commitTransaction();
}
// Start a transaction
InsertPatientAndSeries(
  3695,
  80.3,
  99,
  "0001_L-SPINE_LSS_20160309_091629_240045"
);
session.endSession();
