import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

function ConsultationDetail() {
  const { id } = useParams();
  const [consultation, setConsultation] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchConsultation = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`/api/consultations/${id}/`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        setConsultation(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Failed to fetch consultation details', error);
        setLoading(false);
      }
    };

    fetchConsultation();
  }, [id]);

  const handlePrint = () => {
    // This is a placeholder for a print action.
    // In a real app, this would format the prescription data and open a print dialog.
    alert(`Printing prescription for patient ${consultation.patient_insurance_id}...`);
  };

  if (loading) {
    return <div>Loading consultation details...</div>;
  }

  if (!consultation) {
    return <div>Consultation not found.</div>;
  }

  return (
    <div className="container">
      <h2>Consultation Detail for Patient ID: {consultation.patient_insurance_id}</h2>
      <p><strong>Doctor:</strong> {consultation.doctor}</p>
      <p><strong>Created At:</strong> {new Date(consultation.created_at).toLocaleString()}</p>

      {/* In a real app, you would retrieve and decrypt the prescription here */}
      <button onClick={handlePrint}>Print Prescription</button>
    </div>
  );
}

export default ConsultationDetail;
