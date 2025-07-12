import React, { useState } from 'react';
import axios from 'axios';

function ContractCreate() {
  const [patientInsuranceId, setPatientInsuranceId] = useState('');
  const [diagnosisToken, setDiagnosisToken] = useState('');
  const [prescriptionToken, setPrescriptionToken] = useState('');
  const [insurerId, setInsurerId] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('/api/contracts/', {
        patient_insurance_id: patientInsuranceId,
        diagnosis_token: diagnosisToken,
        prescription_token: prescriptionToken,
        insurer: insurerId,
      }, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      setSuccess(`Contract created successfully with ID: ${response.data.id}`);
    } catch (err) {
      setError('Failed to create contract.');
      console.error(err);
    }
  };

  return (
    <div className="container">
      <h2>Create New Contract</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Patient Insurance ID:</label>
          <input type="text" value={patientInsuranceId} onChange={(e) => setPatientInsuranceId(e.target.value)} />
        </div>
        <div>
          <label>Diagnosis Token:</label>
          <input type="text" value={diagnosisToken} onChange={(e) => setDiagnosisToken(e.target.value)} />
        </div>
        <div>
          <label>Prescription Token:</label>
          <input type="text" value={prescriptionToken} onChange={(e) => setPrescriptionToken(e.target.value)} />
        </div>
        <div>
          <label>Insurer ID:</label>
          <input type="text" value={insurerId} onChange={(e) => setInsurerId(e.target.value)} />
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {success && <p style={{ color: 'green' }}>{success}</p>}
        <button type="submit">Create Contract</button>
      </form>
    </div>
  );
}

export default ContractCreate;
