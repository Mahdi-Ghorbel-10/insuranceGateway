import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

import { Card, CardContent, Typography, Button, CircularProgress, Box, Alert } from '@mui/material';

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
        headers: { Authorization: `Bearer ${token}` }
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

  const handleClaim = async () => { /* ... same as before ... */ };
  const handleFill = async () => { /* ... same as before ... */ };

  if (loading) {
    return <CircularProgress />;
  }

  if (!contract) {
    return <Alert severity="error">Contract not found.</Alert>;
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" component="div">
          Contract #{contract.id}
        </Typography>
        <Typography sx={{ mb: 1.5 }} color="text.secondary">
          Status: {contract.status}
        </Typography>
        <Typography variant="body2">
          <strong>Insurer:</strong> {contract.insurer}
          <br />
          <strong>Claimed By:</strong> {contract.claimed_by_pharmacy ? contract.claimed_by_pharmacy.name : 'Unclaimed'}
          <br />
          <strong>External Ref:</strong> {contract.external_ref_id || 'N/A'}
        </Typography>

        <Box sx={{ mt: 2 }}>
          {user && user.role === 'pharmacist' && !contract.claimed_by_pharmacy && (
            <Button variant="contained" onClick={handleClaim}>Claim Contract</Button>
          )}

          {user && user.role === 'pharmacist' && contract.claimed_by_pharmacy && contract.status === 'ready_for_pharmacy' && (
            <Box>
              <Typography variant="h6">Fill Prescription</Typography>
              {/* Add form fields for invoice data here */}
              <Button variant="contained" onClick={handleFill}>Mark as Filled</Button>
            </Box>
          )}

          {(contract.status === 'submitted' || contract.status === 'archived') && (
            <Button variant="outlined" href={`/api/contracts/${contract.id}/audit-certificate/`} download>
              Download Audit Certificate
            </Button>
          )}
        </Box>

        {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
      </CardContent>
    </Card>
  );
}

export default ContractDetail;
