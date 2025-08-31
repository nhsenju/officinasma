import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  Button,
  TextField,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  PlayArrow as PlayIcon,
  Pause as PauseIcon,
  Stop as StopIcon,
  Edit as EditIcon,
  Save as SaveIcon,
} from '@mui/icons-material';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { callsApi, transcriptsApi } from '../services/api';

const CallDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  
  const [isEditing, setIsEditing] = useState(false);
  const [editedText, setEditedText] = useState('');
  const [audioElement, setAudioElement] = useState<HTMLAudioElement | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);

  const { data: call, isLoading: callLoading, error: callError } = useQuery({
    queryKey: ['call', id],
    queryFn: () => callsApi.getCall(id!),
  });

  const { data: transcript, isLoading: transcriptLoading } = useQuery({
    queryKey: ['transcript', id],
    queryFn: () => callsApi.getCallTranscript(id!),
    enabled: call?.data?.status === 'completed',
  });

  const updateTranscriptMutation = useMutation({
    mutationFn: (data: { text: string }) =>
      transcriptsApi.updateTranscript(transcript?.data?.id!, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['transcript', id] });
      setIsEditing(false);
    },
  });

  const handlePlayAudio = () => {
    if (audioElement) {
      if (isPlaying) {
        audioElement.pause();
      } else {
        audioElement.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleStopAudio = () => {
    if (audioElement) {
      audioElement.pause();
      audioElement.currentTime = 0;
      setIsPlaying(false);
    }
  };

  const handleEditTranscript = () => {
    setEditedText(transcript?.data?.text || '');
    setIsEditing(true);
  };

  const handleSaveTranscript = () => {
    updateTranscriptMutation.mutate({ text: editedText });
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'processing':
        return 'warning';
      case 'error':
        return 'error';
      default:
        return 'default';
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive':
        return 'success';
      case 'negative':
        return 'error';
      case 'neutral':
        return 'default';
      default:
        return 'default';
    }
  };

  if (callLoading) {
    return (
      <Box display="flex" justifyContent="center" p={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (callError) {
    return (
      <Alert severity="error">
        Errore nel caricamento della chiamata: {callError.message}
      </Alert>
    );
  }

  const callData = call?.data;

  return (
    <Box>
      <Button onClick={() => navigate('/dashboard')} sx={{ mb: 2 }}>
        ← Torna alla Dashboard
      </Button>

      <Typography variant="h4" gutterBottom>
        Dettaglio Chiamata
      </Typography>

      {/* Call Info */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3, flexWrap: 'wrap' }}>
            <Box sx={{ flex: { xs: '1 1 100%', md: '1 1 50%' } }}>
              <Typography variant="subtitle2" color="text.secondary">
                ID Chiamata
              </Typography>
              <Typography variant="body1" sx={{ fontFamily: 'monospace' }}>
                {callData?.id}
              </Typography>
            </Box>
            <Box sx={{ flex: { xs: '1 1 100%', md: '1 1 50%' } }}>
              <Typography variant="subtitle2" color="text.secondary">
                Stato
              </Typography>
              <Chip
                label={callData?.status}
                color={getStatusColor(callData?.status) as 'success' | 'warning' | 'error' | 'default'}
              />
            </Box>
            <Box sx={{ flex: { xs: '1 1 100%', md: '1 1 50%' } }}>
              <Typography variant="subtitle2" color="text.secondary">
                Mittente
              </Typography>
              <Typography variant="body1">{callData?.from_email}</Typography>
            </Box>
            <Box sx={{ flex: { xs: '1 1 100%', md: '1 1 50%' } }}>
              <Typography variant="subtitle2" color="text.secondary">
                Oggetto
              </Typography>
              <Typography variant="body1">{callData?.subject || 'N/A'}</Typography>
            </Box>
            <Box sx={{ flex: { xs: '1 1 100%', md: '1 1 50%' } }}>
              <Typography variant="subtitle2" color="text.secondary">
                Data Ricezione
              </Typography>
              <Typography variant="body1">
                {new Date(callData?.received_at).toLocaleString('it-IT')}
              </Typography>
            </Box>
            <Box sx={{ flex: { xs: '1 1 100%', md: '1 1 50%' } }}>
              <Typography variant="subtitle2" color="text.secondary">
                Durata
              </Typography>
              <Typography variant="body1">
                {callData?.duration ? `${Math.round(callData.duration)}s` : 'N/A'}
              </Typography>
            </Box>
            {callData?.sentiment && (
              <Box sx={{ flex: { xs: '1 1 100%', md: '1 1 50%' } }}>
                <Typography variant="subtitle2" color="text.secondary">
                  Sentiment
                </Typography>
                <Chip
                  label={callData.sentiment}
                  color={getSentimentColor(callData.sentiment) as 'success' | 'error' | 'default'}
                />
              </Box>
            )}
            {callData?.confidence_score && (
              <Box sx={{ flex: { xs: '1 1 100%', md: '1 1 50%' } }}>
                <Typography variant="subtitle2" color="text.secondary">
                  Confidenza
                </Typography>
                <Typography variant="body1">
                  {(callData.confidence_score * 100).toFixed(1)}%
                </Typography>
              </Box>
            )}
          </Box>
        </CardContent>
      </Card>

      {/* Audio Player */}
      {callData?.status === 'completed' && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Audio
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <Button
                variant="contained"
                startIcon={isPlaying ? <PauseIcon /> : <PlayIcon />}
                onClick={handlePlayAudio}
              >
                {isPlaying ? 'Pausa' : 'Riproduci'}
              </Button>
              <Button
                variant="outlined"
                startIcon={<StopIcon />}
                onClick={handleStopAudio}
              >
                Stop
              </Button>
            </Box>
            <audio
              ref={(el) => setAudioElement(el)}
              onEnded={() => setIsPlaying(false)}
              style={{ display: 'none' }}
            >
              <source src={`/api/v1/calls/${id}/audio`} type="audio/mpeg" />
            </audio>
          </CardContent>
        </Card>
      )}

      {/* Transcript */}
      {callData?.status === 'completed' && (
        <Card>
          <CardContent>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6">
                Trascrizione
              </Typography>
              {!isEditing ? (
                <Button
                  startIcon={<EditIcon />}
                  onClick={handleEditTranscript}
                >
                  Modifica
                </Button>
              ) : (
                <Button
                  startIcon={<SaveIcon />}
                  onClick={handleSaveTranscript}
                  disabled={updateTranscriptMutation.isPending}
                >
                  Salva
                </Button>
              )}
            </Box>

            {transcriptLoading ? (
              <CircularProgress />
            ) : (
              <Box>
                {isEditing ? (
                  <TextField
                    fullWidth
                    multiline
                    rows={10}
                    value={editedText}
                    onChange={(e) => setEditedText(e.target.value)}
                    variant="outlined"
                  />
                ) : (
                  <Typography
                    variant="body1"
                    sx={{
                      whiteSpace: 'pre-wrap',
                      backgroundColor: 'grey.50',
                      p: 2,
                      borderRadius: 1,
                      minHeight: 200,
                    }}
                  >
                    {transcript?.data?.text || 'Trascrizione non disponibile'}
                  </Typography>
                )}
              </Box>
            )}
          </CardContent>
        </Card>
      )}

      {callData?.status === 'error' && (
        <Alert severity="error">
          Errore durante la trascrizione. Riprova più tardi.
        </Alert>
      )}
    </Box>
  );
};

export default CallDetail;
