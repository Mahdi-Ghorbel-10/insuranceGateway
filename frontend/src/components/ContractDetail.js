import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

function ContractDetail() {
  const { id } = useParams();
  const [contract, setContract] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const user = JSON.parse(localStorage.getItem('user'));

  const fetchContract = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`/api/contracts/${id}/`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      setContract(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch contract details', error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchContract();
  }, [id]);

  const handleClaim = async () => {
    setError('');
    try {
      const token = localStorage.getItem('token');
      await axios.post(`/api/contracts/${id}/claim/`, {}, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      // Refresh the contract details
      fetchContract();
    } catch (err) {
      setError('Failed to claim contract.');
      console.error(err);
    }
  };

  if (loading) {
    return <div>Loading contract details...</div>;
  }

  if (!contract) {
    return <div>Contract not found.</div>;
  }

  return (
    <div className="container">
      <h2>Contract Detail #{contract.id}</h2>
      <p><strong>Status:</strong> {contract.status}</p>
      <p><strong>Insurer:</strong> {contract.insurer}</p>
      <p><strong>Claimed By Pharmacy:</strong> {contract.claimed_by_pharmacy || 'Unclaimed'}</p>
      <p><strong>External Ref ID:</strong> {contract.external_ref_id || 'N/A'}</p>

      {user && user.role === 'pharmacist' && !contract.claimed_by_pharmacy && (
        <button onClick={handleClaim}>Claim Contract</button>
      )}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {/* Decrypted data would be handled here in a real app */}
    </div>
  );
}

export default ContractDetail;
