import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Login from './components/Login';
import ContractList from './components/ContractList';
import ContractDetail from './components/ContractDetail';
import ContractCreate from './components/ContractCreate';
import ConsultationList from './components/ConsultationList';
import ConsultationDetail from './components/ConsultationDetail';
import Home from './components/Home';
import './App.css';

import { AppBar, Toolbar, Typography, Button, Container } from '@mui/material';

function App() {
  return (
    <Router>
      <div>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Insurance Platform
            </Typography>
            <Button color="inherit" component={Link} to="/">Home</Button>
            <Button color="inherit" component={Link} to="/login">Login</Button>
            <Button color="inherit" component={Link} to="/consultations">Consultations</Button>
            <Button color="inherit" component={Link} to="/contracts">Contracts</Button>
            <Button color="inherit" component={Link} to="/contracts/new">Create Contract</Button>
          </Toolbar>
        </AppBar>

        <Container sx={{ mt: 4 }}>
          <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/consultations" element={<ConsultationList />} />
          <Route path="/consultations/:id" element={<ConsultationDetail />} />
          <Route path="/contracts" element={<ContractList />} />
          <Route path="/contracts/new" element={<ContractCreate />} />
          <Route path="/contracts/:id" element={<ContractDetail />} />
          <Route path="/" element={<Home />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
