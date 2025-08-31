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
  Switch,
  FormControlLabel,
} from '@mui/material';
import { ingestApi } from '../services/api';

const Settings: React.FC = () => {
  const [gmailClientId, setGmailClientId] = useState('');
  const [gmailClientSecret, setGmailClientSecret] = useState('');
  const [outlookClientId, setOutlookClientId] = useState('');
  const [outlookClientSecret, setOutlookClientSecret] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleGmailSetup = async () => {
    if (!gmailClientId || !gmailClientSecret) {
      setError('Inserisci Client ID e Client Secret per Gmail');
      return;
    }

    setIsLoading(true);
    setError('');
    setSuccess('');

    try {
      await ingestApi.setupGmail({
        client_id: gmailClientId,
        client_secret: gmailClientSecret,
      });
      setSuccess('Integrazione Gmail configurata con successo');
      setGmailClientId('');
      setGmailClientSecret('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Errore nella configurazione Gmail');
    } finally {
      setIsLoading(false);
    }
  };

  const handleOutlookSetup = async () => {
    if (!outlookClientId || !outlookClientSecret) {
      setError('Inserisci Client ID e Client Secret per Outlook');
      return;
    }

    setIsLoading(true);
    setError('');
    setSuccess('');

    try {
      await ingestApi.setupOutlook({
        client_id: outlookClientId,
        client_secret: outlookClientSecret,
      });
      setSuccess('Integrazione Outlook configurata con successo');
      setOutlookClientId('');
      setOutlookClientSecret('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Errore nella configurazione Outlook');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Impostazioni
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          {success}
        </Alert>
      )}

      {/* Email Integration Settings */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Integrazione Email
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Configura l'integrazione automatica con Gmail e Outlook per ricevere email con allegati audio.
          </Typography>

          <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
            {/* Gmail Integration */}
            <Box sx={{ flex: 1 }}>
              <Typography variant="subtitle1" gutterBottom>
                Gmail Integration
              </Typography>
              <TextField
                fullWidth
                label="Client ID"
                value={gmailClientId}
                onChange={(e) => setGmailClientId(e.target.value)}
                margin="normal"
                disabled={isLoading}
              />
              <TextField
                fullWidth
                label="Client Secret"
                type="password"
                value={gmailClientSecret}
                onChange={(e) => setGmailClientSecret(e.target.value)}
                margin="normal"
                disabled={isLoading}
              />
              <Button
                variant="contained"
                onClick={handleGmailSetup}
                disabled={isLoading}
                sx={{ mt: 2 }}
              >
                {isLoading ? <CircularProgress size={20} /> : 'Configura Gmail'}
              </Button>
            </Box>

            <Box sx={{ flex: 1 }}>
              <Typography variant="subtitle1" gutterBottom>
                Outlook Integration
              </Typography>
              <TextField
                fullWidth
                label="Client ID"
                value={outlookClientId}
                onChange={(e) => setOutlookClientId(e.target.value)}
                margin="normal"
                disabled={isLoading}
              />
              <TextField
                fullWidth
                label="Client Secret"
                type="password"
                value={outlookClientSecret}
                onChange={(e) => setOutlookClientSecret(e.target.value)}
                margin="normal"
                disabled={isLoading}
              />
              <Button
                variant="contained"
                onClick={handleOutlookSetup}
                disabled={isLoading}
                sx={{ mt: 2 }}
              >
                {isLoading ? <CircularProgress size={20} /> : 'Configura Outlook'}
              </Button>
            </Box>
          </Box>
        </CardContent>
      </Card>

      {/* System Settings */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Impostazioni Sistema
          </Typography>
          
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <FormControlLabel
              control={<Switch defaultChecked />}
              label="Notifiche email per nuove trascrizioni"
            />
            <FormControlLabel
              control={<Switch defaultChecked />}
              label="Backup automatico database"
            />
            <FormControlLabel
              control={<Switch />}
              label="Modalità debug"
            />
          </Box>
        </CardContent>
      </Card>

      {/* API Information */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Informazioni API
          </Typography>
          
          <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 2 }}>
            <Box sx={{ flex: 1 }}>
              <Typography variant="subtitle2" color="text.secondary">
                Base URL API
              </Typography>
              <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                {process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1'}
              </Typography>
            </Box>
            <Box sx={{ flex: 1 }}>
              <Typography variant="subtitle2" color="text.secondary">
                Versione
              </Typography>
              <Typography variant="body2">
                1.0.0
              </Typography>
            </Box>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Settings;
