from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
import structlog

logger = structlog.get_logger()

# Metrics definitions
TRANSCRIPTION_REQUESTS = Counter(
    'transcription_requests_total',
    'Total transcription requests',
    ['status', 'language']
)

TRANSCRIPTION_DURATION = Histogram(
    'transcription_duration_seconds',
    'Time spent on transcription',
    ['model', 'language']
)

AUDIO_FILE_SIZE = Histogram(
    'audio_file_size_bytes',
    'Size of uploaded audio files',
    ['format']
)

ACTIVE_TRANSCRIPTIONS = Gauge(
    'active_transcriptions',
    'Number of currently active transcriptions'
)

EMAIL_INGESTION_SUCCESS = Counter(
    'email_ingestion_total',
    'Email ingestion attempts',
    ['status', 'provider']
)

EXPORT_REQUESTS = Counter(
    'export_requests_total',
    'Export requests by format',
    ['format', 'status']
)

def setup_metrics():
    """Initialize metrics"""
    logger.info("Setting up Prometheus metrics")

def get_metrics():
    """Return metrics in Prometheus format"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

def record_transcription_request(status: str, language: str = "unknown"):
    """Record a transcription request"""
    TRANSCRIPTION_REQUESTS.labels(status=status, language=language).inc()

def record_transcription_duration(duration: float, model: str = "whisper-1", language: str = "unknown"):
    """Record transcription duration"""
    TRANSCRIPTION_DURATION.labels(model=model, language=language).observe(duration)

def record_audio_file_size(size: int, format: str):
    """Record audio file size"""
    AUDIO_FILE_SIZE.labels(format=format).observe(size)

def set_active_transcriptions(count: int):
    """Set the number of active transcriptions"""
    ACTIVE_TRANSCRIPTIONS.set(count)

def record_email_ingestion(status: str, provider: str):
    """Record email ingestion attempt"""
    EMAIL_INGESTION_SUCCESS.labels(status=status, provider=provider).inc()

def record_export_request(format: str, status: str):
    """Record export request"""
    EXPORT_REQUESTS.labels(format=format, status=status).inc()
