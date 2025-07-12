import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function ContractList() {
  const [contracts, setContracts] = useState([]);
  const [loading, setLoading] = useState(true);
  const user = JSON.parse(localStorage.getItem('user'));

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
      <h2>{user && user.role === 'pharmacist' ? 'Available and Claimed Contracts' : 'Your Contracts'}</h2>
      <ul>
        {contracts.map(contract => (
          <li key={contract.id}>
            <Link to={`/contracts/${contract.id}`}>
              Contract #{contract.id} - Status: {contract.status}
              {user && user.role === 'pharmacist' && (
                <span> - {contract.claimed_by_pharmacy ? `Claimed by You` : 'Unclaimed'}</span>
              )}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ContractList;
