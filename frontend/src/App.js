import React, { useState } from 'react';
import {
  Container,
  Box,
  Typography,
  TextField,
  Button,
  Paper,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
  Alert
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import FitnessCenterIcon from '@mui/icons-material/FitnessCenter';
import MedicalServicesIcon from '@mui/icons-material/MedicalServices';
import axios from 'axios';

function App() {
  const [symptoms, setSymptoms] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);

  const analyzeSymptoms = async () => {
    if (!symptoms.trim()) {
      setError('Please enter your symptoms');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:8000/predict', {
        message: symptoms
      });
      setResults(response.data);
    } catch (err) {
      setError('An error occurred while analyzing symptoms');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center" color="primary">
          Medical Symptom Analysis
        </Typography>

        <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
          <TextField
            fullWidth
            multiline
            rows={4}
            variant="outlined"
            label="Describe your symptoms"
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
            sx={{ mb: 2 }}
          />
          <Button
            variant="contained"
            color="primary"
            onClick={analyzeSymptoms}
            disabled={loading}
            fullWidth
            size="large"
          >
            {loading ? <CircularProgress size={24} /> : 'Analyze Symptoms'}
          </Button>
        </Paper>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {results && (
          <Box>
            <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
              <Typography variant="h5" gutterBottom>
                Extracted Symptoms
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {results.symptoms.map((symptom, index) => (
                  <Chip
                    key={index}
                    label={symptom}
                    color="primary"
                    variant="outlined"
                  />
                ))}
              </Box>
            </Paper>

            <Typography variant="h5" gutterBottom>
              Top Matching Diseases
            </Typography>
            {results.top_diseases.map((disease, index) => (
              <Accordion key={index} sx={{ mb: 2 }}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', width: '100%', alignItems: 'center' }}>
                    <Typography variant="h6">{disease.disease}</Typography>
                    <Chip
                      label={`${(disease.similarity * 100).toFixed(1)}% match`}
                      color="success"
                      size="small"
                    />
                  </Box>
                </AccordionSummary>
                <AccordionDetails>
                  <Box sx={{ display: 'flex', gap: 2 }}>
                    <Paper elevation={2} sx={{ p: 2, flex: 1 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <FitnessCenterIcon color="primary" sx={{ mr: 1 }} />
                        <Typography variant="h6">Recommended Workouts</Typography>
                      </Box>
                      <List dense>
                        {disease.workouts.map((workout, i) => (
                          <ListItem key={i}>
                            <ListItemText primary={workout} />
                          </ListItem>
                        ))}
                      </List>
                    </Paper>
                    <Paper elevation={2} sx={{ p: 2, flex: 1 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <MedicalServicesIcon color="primary" sx={{ mr: 1 }} />
                        <Typography variant="h6">Precautions</Typography>
                      </Box>
                      <List dense>
                        {disease.precautions.map((precaution, i) => (
                          <ListItem key={i}>
                            <ListItemText primary={precaution} />
                          </ListItem>
                        ))}
                      </List>
                    </Paper>
                  </Box>
                </AccordionDetails>
              </Accordion>
            ))}
          </Box>
        )}
      </Box>
    </Container>
  );
}

export default App; 