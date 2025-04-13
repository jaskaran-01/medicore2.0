import React from 'react';
import { Card, CardContent, Typography, Box, Grid, Paper } from '@mui/material';
import ReactMarkdown from 'react-markdown';
import { DiagnosisResponse } from '../types';

interface DiagnosisCardProps {
    diagnosis: DiagnosisResponse;
}

const DiagnosisCard: React.FC<DiagnosisCardProps> = ({ diagnosis }) => {
    const { disease_info, symptoms, wikipedia_image } = diagnosis;

    return (
        <Card sx={{ mt: 2, maxWidth: '100%' }}>
            <CardContent>
                <Grid container spacing={2}>
                    {wikipedia_image && (
                        <Grid item xs={12} md={4}>
                            <Box
                                component="img"
                                src={wikipedia_image}
                                alt={disease_info.disease}
                                sx={{
                                    width: '100%',
                                    height: 'auto',
                                    borderRadius: 1,
                                }}
                            />
                        </Grid>
                    )}
                    <Grid item xs={12} md={wikipedia_image ? 8 : 12}>
                        <Typography variant="h6" gutterBottom>
                            {disease_info.disease}
                        </Typography>
                        
                        <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                            Detected Symptoms:
                        </Typography>
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                            {symptoms.map((symptom, index) => (
                                <Paper
                                    key={index}
                                    sx={{
                                        p: 1,
                                        bgcolor: 'primary.light',
                                        color: 'primary.contrastText',
                                    }}
                                >
                                    {symptom}
                                </Paper>
                            ))}
                        </Box>

                        {disease_info.description && (
                            <>
                                <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                                    Description:
                                </Typography>
                                <Typography paragraph>
                                    {disease_info.description}
                                </Typography>
                            </>
                        )}

                        {disease_info.workout && (
                            <>
                                <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                                    Recommended Workout:
                                </Typography>
                                <ReactMarkdown>{disease_info.workout}</ReactMarkdown>
                            </>
                        )}

                        {disease_info.precautions && (
                            <>
                                <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                                    Precautions:
                                </Typography>
                                <ReactMarkdown>{disease_info.precautions}</ReactMarkdown>
                            </>
                        )}

                        {disease_info.diet && (
                            <>
                                <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                                    Recommended Diet:
                                </Typography>
                                <ReactMarkdown>{disease_info.diet}</ReactMarkdown>
                            </>
                        )}
                    </Grid>
                </Grid>
            </CardContent>
        </Card>
    );
};

export default DiagnosisCard; 