import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

import { List, ListItem, ListItemText, Typography, CircularProgress } from '@mui/material';

function ContractList() {
  const [contracts, setContracts] = useState([]);
  const [loading, setLoading] = useState(true);
  const user = JSON.parse(localStorage.getItem('user'));

  useEffect(() => {
    const fetchContracts = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('/api/contracts/', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setContracts(response.data.results);
        setLoading(false);
      } catch (error) {
        console.error('Failed to fetch contracts', error);
        setLoading(false);
      }
    };
    fetchContracts();
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        {user && user.role === 'pharmacist' ? 'Available and Claimed Contracts' : 'Your Contracts'}
      </Typography>
      <List>
        {contracts.map(contract => (
          <ListItem button component={Link} to={`/contracts/${contract.id}`} key={contract.id}>
            <ListItemText
              primary={`Contract #${contract.id}`}
              secondary={`Status: ${contract.status} ${user && user.role === 'pharmacist' ? (contract.claimed_by_pharmacy ? '- Claimed' : '- Unclaimed') : ''}`}
            />
          </ListItem>
        ))}
      </List>
    </div>
  );
}

export default ContractList;
