#!/bin/bash

# Porta RTSP (default 8554)
PORT=8554
STREAM_NAME=webcam

# Percorso a mediamtx (assicurati che sia installato con brew o scaricato)
MEDIA_SERVER_BIN=$(which mediamtx)

if [ -z "$MEDIA_SERVER_BIN" ]; then
  echo "Errore: mediamtx non trovato. Installa con: brew install mediamtx"
  exit 1
fi

echo "Avvio MediaMTX sulla porta $PORT..."
$MEDIA_SERVER_BIN &   # lo avvia in background
SERVER_PID=$!

sleep 2  # aspetta che il server salga

echo "Streaming webcam con ffmpeg..."
ffmpeg -f avfoundation -framerate 30 -pixel_format nv12 -i "0" \
  -c:v libx264 -preset ultrafast -tune zerolatency \
  -f rtsp rtsp://127.0.0.1:$PORT/$STREAM_NAME

# Quando chiudi ffmpeg, kill del server
kill $SERVER_PID
