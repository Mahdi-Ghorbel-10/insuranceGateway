import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function ContractList() {
  const [contracts, setContracts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchContracts = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('/api/contracts/', {
          headers: {
            Authorization: `Bearer ${token}` // Assuming JWT or similar
          }
        });
        setContracts(response.data.results); // Assuming DRF pagination
        setLoading(false);
      } catch (error) {
        console.error('Failed to fetch contracts', error);
        setLoading(false);
      }
    };

    fetchContracts();
  }, []);

  if (loading) {
    return <div>Loading contracts...</div>;
  }

  return (
    <div className="container">
      <h2>Your Contracts</h2>
      <ul>
        {contracts.map(contract => (
          <li key={contract.id}>
            <Link to={`/contracts/${contract.id}`}>
              Contract #{contract.id} - Status: {contract.status}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ContractList;
