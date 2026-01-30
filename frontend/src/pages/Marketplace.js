import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  Box,
  TextField,
  MenuItem,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { listingsAPI } from '../services/api';

function Marketplace() {
  const [listings, setListings] = useState([]);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchListings();
  }, [category, search]);

  const fetchListings = async () => {
    try {
      const params = {};
      if (category) params.category = category;
      if (search) params.search = search;
      
      const response = await listingsAPI.getAll(params);
      setListings(response.data);
    } catch (error) {
      console.error('Failed to fetch listings:', error);
    }
  };

  const categories = [
    'metal', 'plastic', 'wood', 'textile', 
    'electronic', 'glass', 'paper', 'other'
  ];

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Marketplace
      </Typography>

      <Box sx={{ mb: 3, display: 'flex', gap: 2 }}>
        <TextField
          label="Search"
          variant="outlined"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          sx={{ flex: 1 }}
        />
        <TextField
          select
          label="Category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          sx={{ minWidth: 200 }}
        >
          <MenuItem value="">All Categories</MenuItem>
          {categories.map((cat) => (
            <MenuItem key={cat} value={cat}>
              {cat.charAt(0).toUpperCase() + cat.slice(1)}
            </MenuItem>
          ))}
        </TextField>
        <Button
          variant="contained"
          onClick={() => navigate('/listings/new')}
        >
          Create Listing
        </Button>
      </Box>

      <Grid container spacing={3}>
        {listings.map((listing) => (
          <Grid item xs={12} sm={6} md={4} key={listing.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {listing.title}
                </Typography>
                <Chip
                  label={listing.category}
                  size="small"
                  sx={{ mb: 1 }}
                />
                <Typography variant="body2" color="text.secondary" paragraph>
                  {listing.description?.substring(0, 100)}...
                </Typography>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="h6" color="primary">
                    ${listing.price_per_unit}/{listing.unit}
                  </Typography>
                  <Typography variant="body2">
                    Qty: {listing.quantity}
                  </Typography>
                </Box>
                <Button
                  fullWidth
                  variant="outlined"
                  sx={{ mt: 2 }}
                  onClick={() => navigate(`/listings/${listing.id}`)}
                >
                  View Details
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {listings.length === 0 && (
        <Typography variant="body1" align="center" sx={{ mt: 4 }}>
          No listings found
        </Typography>
      )}
    </Container>
  );
}

export default Marketplace;
