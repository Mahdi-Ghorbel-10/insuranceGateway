import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DynamicForm from './DynamicForm';

function ContractCreate() {
  const [patientInsuranceId, setPatientInsuranceId] = useState('');
  const [diagnosisData, setDiagnosisData] = useState(''); // Plaintext for vault
  const [prescriptionData, setPrescriptionData] = useState(''); // Plaintext for vault
  const [insurerId, setInsurerId] = useState('');
  const [formTemplate, setFormTemplate] = useState(null);
  const [formData, setFormData] = useState({});
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const user = JSON.parse(localStorage.getItem('user'));

  useEffect(() => {
    const fetchFormTemplate = async () => {
      if (user && user.specialty) {
        try {
          const token = localStorage.getItem('token');
          // This assumes a simple GET endpoint for templates by specialty
          const response = await axios.get(`/api/form-templates/?specialty=${user.specialty}`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          if (response.data && response.data.length > 0) {
            setFormTemplate(response.data[0]);
          }
        } catch (err) {
          console.error('Failed to fetch form template', err);
        }
      }
    };
    fetchFormTemplate();
  }, [user]);

import { KJUR, KEYUTIL } from 'jsrsasign';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      // 1. Create a hash of the data to be signed
      const dataToSign = JSON.stringify({
        patient_insurance_id: patientInsuranceId,
        diagnosis_data: diagnosisData,
        prescription_data: prescriptionData,
        form_data: formData,
      });

      // 2. Simulate signing with a private key
      // In a real app, this key would be managed securely on the client-side
      const prvKey = KEYUTIL.generateKeypair("EC", "secp256r1").prvKeyObj;
      const signature = new KJUR.crypto.Signature({"alg": "SHA256withECDSA"});
      signature.init(prvKey);
      signature.updateString(dataToSign);
      const sigHex = signature.sign();

      // 3. Send data and signature to the backend
      const token = localStorage.getItem('token');
      const response = await axios.post('/api/contracts/', {
        patient_insurance_id: patientInsuranceId,
        diagnosis_data: diagnosisData,
        prescription_data: prescriptionData,
        insurer: insurerId,
        form_data: formData,
        doctor_signature: sigHex,
      }, {
        headers: { Authorization: `Bearer ${token}` }
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
          <label>Diagnosis Data (for vault):</label>
          <textarea value={diagnosisData} onChange={(e) => setDiagnosisData(e.target.value)} />
        </div>
        <div>
          <label>Prescription Data (for vault):</label>
          <textarea value={prescriptionData} onChange={(e) => setPrescriptionData(e.target.value)} />
        </div>
        <div>
          <label>Insurer ID:</label>
          <input type="text" value={insurerId} onChange={(e) => setInsurerId(e.target.value)} />
        </div>

        {formTemplate && (
          <>
            <h3>{formTemplate.name}</h3>
            <DynamicForm schema={formTemplate.template_schema} formData={formData} setFormData={setFormData} />
          </>
        )}

        {error && <p style={{ color: 'red' }}>{error}</p>}
        {success && <p style={{ color: 'green' }}>{success}</p>}
        <button type="submit">Create Contract</button>
      </form>
    </div>
  );
}

export default ContractCreate;
