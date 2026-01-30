import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Circular Economy Marketplace
        </Typography>
        <Box>
          <Button color="inherit" onClick={() => navigate('/')}>
            Marketplace
          </Button>
          {user?.role === 'admin' && (
            <Button color="inherit" onClick={() => navigate('/admin')}>
              Admin
            </Button>
          )}
          <Button color="inherit" onClick={handleLogout}>
            Logout ({user?.username})
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;
