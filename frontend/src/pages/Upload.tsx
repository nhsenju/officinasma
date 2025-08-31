import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Alert,
  CircularProgress,
  Paper,
  Container,
  Chip,
} from '@mui/material';
import { 
  CloudUpload as UploadIcon,
  AudioFile as AudioIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon
} from '@mui/icons-material';
import { ingestApi } from '../services/api';

const Upload: React.FC = () => {
  const [fromEmail, setFromEmail] = useState('');
  const [subject, setSubject] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // Validate file type
      const allowedTypes = ['audio/wav', 'audio/mpeg', 'audio/mp4', 'audio/ogg'];
      if (!allowedTypes.includes(file.type)) {
        setError('Formato file non supportato. Usa WAV, MP3, M4A o OGG.');
        return;
      }
      
      // Validate file size (100MB max)
      if (file.size > 100 * 1024 * 1024) {
        setError('File troppo grande. Dimensione massima: 100MB.');
        return;
      }
      
      setSelectedFile(file);
      setError('');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedFile || !fromEmail) {
      setError('Compila tutti i campi obbligatori.');
      return;
    }

    setIsLoading(true);
    setError('');
    setSuccess('');

    try {
      const formData = new FormData();
      formData.append('from_email', fromEmail);
      formData.append('subject', subject);
      formData.append('audio_file', selectedFile);

      const response = await ingestApi.ingestEmail(formData);
      
      setSuccess(`File caricato con successo! ID chiamata: ${response.data.call_id}`);
      setFromEmail('');
      setSubject('');
      setSelectedFile(null);
      
      // Reset file input
      const fileInput = document.getElementById('file-input') as HTMLInputElement;
      if (fileInput) fileInput.value = '';
      
    } catch (err: any) {
      const errorMessage = typeof err.response?.data?.detail === 'string' 
        ? err.response.data.detail 
        : 'Errore durante il caricamento';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      {/* Header Section */}
      <Box sx={{ textAlign: 'center', mb: 4 }}>
        <Typography 
          variant="h3" 
          sx={{ 
            fontWeight: 800,
            fontSize: '2.5rem',
            color: '#1e293b',
            mb: 2,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent'
          }}
        >
          Carica File Audio
        </Typography>
        <Typography 
          variant="body1" 
          sx={{ 
            fontSize: '1.1rem',
            color: '#64748b',
            maxWidth: 600,
            mx: 'auto'
          }}
        >
          Carica i tuoi file audio per la trascrizione automatica e l'analisi del sentiment
        </Typography>
      </Box>

      {/* Main Upload Card */}
      <Card sx={{ 
        borderRadius: 3,
        boxShadow: '0 10px 25px rgba(0,0,0,0.1)',
        border: '1px solid #e2e8f0',
        overflow: 'hidden'
      }}>
        <CardContent sx={{ p: 4 }}>
          <Box component="form" onSubmit={handleSubmit}>
            {/* Form Fields */}
            <Box sx={{ display: 'grid', gap: 3, mb: 4 }}>
              <TextField
                fullWidth
                label="Email mittente *"
                value={fromEmail}
                onChange={(e) => setFromEmail(e.target.value)}
                required
                disabled={isLoading}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    borderRadius: 2,
                    fontSize: '1rem',
                    '&:hover fieldset': {
                      borderColor: '#667eea',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: '#667eea',
                    },
                  },
                  '& .MuiInputLabel-root': {
                    fontSize: '0.9rem',
                    fontWeight: 500
                  }
                }}
              />
              
              <TextField
                fullWidth
                label="Oggetto email"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                disabled={isLoading}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    borderRadius: 2,
                    fontSize: '1rem',
                    '&:hover fieldset': {
                      borderColor: '#667eea',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: '#667eea',
                    },
                  },
                  '& .MuiInputLabel-root': {
                    fontSize: '0.9rem',
                    fontWeight: 500
                  }
                }}
              />
            </Box>

            {/* File Upload Area */}
            <Paper
              sx={{
                p: 4,
                mb: 4,
                border: '2px dashed',
                borderColor: selectedFile ? '#10b981' : '#cbd5e1',
                borderRadius: 3,
                textAlign: 'center',
                cursor: 'pointer',
                background: selectedFile ? 'linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%)' : '#ffffff',
                transition: 'all 0.3s ease',
                '&:hover': {
                  borderColor: selectedFile ? '#10b981' : '#667eea',
                  background: selectedFile ? 'linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%)' : '#f8fafc',
                  transform: 'translateY(-2px)',
                  boxShadow: '0 8px 25px rgba(0,0,0,0.1)'
                },
              }}
              onClick={() => document.getElementById('file-input')?.click()}
            >
              <input
                id="file-input"
                type="file"
                accept=".wav,.mp3,.m4a,.ogg"
                onChange={handleFileSelect}
                style={{ display: 'none' }}
              />
              
              {selectedFile ? (
                <Box>
                  <Box sx={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'center', 
                    mb: 2 
                  }}>
                    <CheckIcon sx={{ 
                      fontSize: 48, 
                      color: '#10b981', 
                      mr: 2 
                    }} />
                    <AudioIcon sx={{ 
                      fontSize: 32, 
                      color: '#10b981' 
                    }} />
                  </Box>
                  <Typography 
                    variant="h6" 
                    sx={{ 
                      color: '#10b981',
                      fontWeight: 700,
                      mb: 1
                    }}
                  >
                    File selezionato
                  </Typography>
                  <Typography 
                    variant="body1" 
                    sx={{ 
                      color: '#059669',
                      fontWeight: 500,
                      mb: 2
                    }}
                  >
                    {selectedFile.name}
                  </Typography>
                  <Chip 
                    label={`${(selectedFile.size / 1024 / 1024).toFixed(2)} MB`}
                    color="success"
                    size="small"
                    sx={{ 
                      fontSize: '0.75rem',
                      fontWeight: 600
                    }}
                  />
                </Box>
              ) : (
                <Box>
                  <Box sx={{ 
                    p: 3, 
                    borderRadius: 3, 
                    bgcolor: '#f8fafc',
                    display: 'inline-flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    mb: 3
                  }}>
                    <UploadIcon sx={{ 
                      fontSize: 64, 
                      color: '#667eea',
                      filter: 'drop-shadow(0 4px 8px rgba(102, 126, 234, 0.3))'
                    }} />
                  </Box>
                  <Typography 
                    variant="h6" 
                    sx={{ 
                      color: '#1e293b',
                      fontWeight: 700,
                      mb: 2
                    }}
                  >
                    Clicca per selezionare un file audio
                  </Typography>
                  <Typography 
                    variant="body1" 
                    sx={{ 
                      color: '#64748b',
                      mb: 3
                    }}
                  >
                    Trascina qui il file o clicca per sfogliare
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, justifyContent: 'center', flexWrap: 'wrap' }}>
                    {['WAV', 'MP3', 'M4A', 'OGG'].map((format) => (
                      <Chip 
                        key={format}
                        label={format}
                        size="small"
                        sx={{ 
                          fontSize: '0.7rem',
                          fontWeight: 600,
                          bgcolor: '#e2e8f0',
                          color: '#475569'
                        }}
                      />
                    ))}
                  </Box>
                  <Typography 
                    variant="caption" 
                    sx={{ 
                      color: '#94a3b8',
                      display: 'block',
                      mt: 2
                    }}
                  >
                    Dimensione massima: 100MB
                  </Typography>
                </Box>
              )}
            </Paper>

            {/* Status Messages */}
            {error && (
              <Alert 
                severity="error" 
                sx={{ 
                  mb: 3,
                  borderRadius: 2,
                  '& .MuiAlert-icon': {
                    fontSize: '1.2rem'
                  }
                }}
                icon={<ErrorIcon />}
              >
                {error}
              </Alert>
            )}

            {success && (
              <Alert 
                severity="success" 
                sx={{ 
                  mb: 3,
                  borderRadius: 2,
                  '& .MuiAlert-icon': {
                    fontSize: '1.2rem'
                  }
                }}
                icon={<CheckIcon />}
              >
                {success}
              </Alert>
            )}

            {/* Submit Button */}
            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              disabled={isLoading || !selectedFile || !fromEmail}
              sx={{
                py: 2,
                borderRadius: 2,
                fontSize: '1.1rem',
                fontWeight: 700,
                textTransform: 'none',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                boxShadow: '0 4px 15px rgba(102, 126, 234, 0.4)',
                '&:hover': {
                  background: 'linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%)',
                  transform: 'translateY(-2px)',
                  boxShadow: '0 8px 25px rgba(102, 126, 234, 0.5)',
                },
                '&:disabled': {
                  background: '#e2e8f0',
                  color: '#94a3b8',
                  transform: 'none',
                  boxShadow: 'none'
                },
                transition: 'all 0.3s ease'
              }}
            >
              {isLoading ? (
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <CircularProgress size={24} color="inherit" />
                  <Typography>Caricamento in corso...</Typography>
                </Box>
              ) : (
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <UploadIcon />
                  <Typography>Carica e Trascrivi</Typography>
                </Box>
              )}
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Container>
  );
};

export default Upload;
