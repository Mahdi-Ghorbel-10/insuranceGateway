import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function ConsultationList() {
  const [consultations, setConsultations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchConsultations = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('/api/consultations/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        setConsultations(response.data.results);
        setLoading(false);
      } catch (error) {
        console.error('Failed to fetch consultations', error);
        setLoading(false);
      }
    };

    fetchConsultations();
  }, []);

  if (loading) {
    return <div>Loading consultations...</div>;
  }

  return (
    <div className="container">
      <h2>Your Consultations</h2>
      <ul>
        {consultations.map(consultation => (
          <li key={consultation.id}>
            <Link to={`/consultations/${consultation.id}`}>
              Consultation for Patient ID: {consultation.patient_insurance_id}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ConsultationList;
