# 🚗 Sistema di Riconoscimento Targhe con Livestream AI

## Panoramica

Il sistema di riconoscimento targhe con livestream AI è una funzionalità avanzata che monitora continuamente un flusso video per rilevare automaticamente le targhe dei veicoli, applicare blur per la privacy e verificare se i veicoli rilevati hanno appuntamenti programmati.

## 🎯 Funzionalità Principali

### 1. **Monitoraggio Livestream Continuo**
- Monitora un flusso video in tempo reale (webcam o stream URL)
- Riconosce automaticamente le targhe italiane
- Applica blur alle facce e targhe per la privacy
- Salva immagini delle targhe rilevate

### 2. **Riconoscimento Targhe**
- Utilizza OpenCV per il rilevamento delle targhe
- OCR per la lettura del testo delle targhe
- Validazione del formato italiano (AA123AA)
- Confidenza del riconoscimento

### 3. **Verifica Appuntamenti**
- Cerca automaticamente nel database se la targa è registrata
- Verifica se ci sono appuntamenti per il giorno corrente
- Mostra informazioni complete su veicolo e cliente

### 4. **Privacy e Sicurezza**
- **Blur automatico delle facce** rilevate
- **Blur automatico delle targhe** rilevate
- Salvataggio sicuro delle immagini
- Logging delle rilevazioni

## 🚀 Come Utilizzare

### Accesso all'Interfaccia

1. Apri il browser e vai su `http://localhost:3000`
2. Effettua il login con le credenziali
3. Clicca su **"Livestream AI"** nella navigazione

### Configurazione del Monitoraggio

#### 1. **Avvio del Monitoraggio**
- **URL Stream Input**: Inserisci l'URL del flusso video
  - `0` per webcam locale
  - `rtsp://...` per stream IP camera
  - `http://...` per stream HTTP
- **URL Stream Output** (opzionale): Per salvare il video con blur
  - Es: `output.avi` per salvare localmente
- Clicca **"Avvia Monitoraggio"**

#### 2. **Controllo dello Stato**
- **Monitoraggio Attivo**: Indica se il sistema è in funzione
- **Blur Facce e Targhe**: Mostra che la privacy è attiva
- **Ferma Monitoraggio**: Per arrestare il sistema

### Visualizzazione dei Risultati

#### Tab 1: **Rilevazioni Recenti**
- Lista delle targhe rilevate in tempo reale
- Informazioni su veicolo e cliente
- Stato degli appuntamenti
- Timestamp della rilevazione

#### Tab 2: **Immagini Targhe**
- Galleria delle immagini delle targhe salvate
- Visualizzazione a griglia con timestamp
- Possibilità di eliminare le immagini
- Visualizzazione ingrandita

#### Tab 3: **Ricerca Manuale**
- Ricerca manuale di una targa specifica
- Risultati dettagliati con informazioni complete

## 🔧 Configurazione Tecnica

### Requisiti di Sistema

- **OpenCV**: Per il processing video
- **Cascade Classifiers**: Per il rilevamento facce e targhe
- **OCR**: Per la lettura del testo delle targhe
- **Database**: PostgreSQL per i dati

### Struttura delle Directory

```
backend/
├── uploads/
│   └── plates/          # Immagini delle targhe salvate
│       ├── plate_AB123CD_20231201_143022.jpg
│       └── ...
└── app/
    └── services/
        └── license_plate_service.py  # Servizio principale
```

### API Endpoints

#### Monitoraggio Livestream
- `POST /api/v1/ai/livestream/start` - Avvia monitoraggio
- `POST /api/v1/ai/livestream/stop` - Ferma monitoraggio
- `GET /api/v1/ai/livestream/status` - Stato del monitoraggio

#### Riconoscimento Targhe
- `POST /api/v1/ai/plate/detect` - Processa targa manualmente
- `GET /api/v1/ai/plate/search/{targa}` - Cerca targa nel database

#### Gestione Immagini
- `GET /api/v1/ai/plates/images` - Lista immagini salvate
- `GET /api/v1/ai/plates/images/{filename}` - Scarica immagine
- `DELETE /api/v1/ai/plates/images/{filename}` - Elimina immagine

## 📊 Logging e Monitoraggio

### Log del Sistema
Il sistema registra automaticamente:
- Avvio/arresto del monitoraggio
- Targhe rilevate con timestamp
- Errori di riconoscimento
- Salvataggio delle immagini

### Esempi di Log
```
INFO: Livestream monitoring avviato
INFO: Targa rilevata: AB123CD
INFO: ✅ Appuntamento trovato per Mario Rossi - Fiat Panda
INFO: Immagine targa salvata: uploads/plates/plate_AB123CD_20231201_143022.jpg
```

## 🔒 Sicurezza e Privacy

### Protezione della Privacy
1. **Blur Automatico**: Facce e targhe vengono sfocate automaticamente
2. **Salvataggio Sicuro**: Le immagini sono salvate in directory protette
3. **Logging Sicuro**: I log non contengono dati sensibili
4. **Accesso Controllato**: Solo utenti autorizzati possono accedere

### Configurazione Blur
- **Faccia**: Blur gaussiano 25x25 pixel
- **Targa**: Blur gaussiano 35x35 pixel
- **Rettangoli indicatori**: Mostrano le aree sfocate

## 🛠️ Risoluzione Problemi

### Problemi Comuni

#### 1. **Stream non accessibile**
```
Errore: Impossibile aprire lo stream
```
**Soluzione**: Verifica l'URL dello stream e la connessione di rete

#### 2. **Nessuna targa rilevata**
```
INFO: Nessuna rilevazione recente
```
**Soluzione**: 
- Verifica la qualità del video
- Controlla l'illuminazione
- Assicurati che le targhe siano visibili

#### 3. **Errore OCR**
```
ERROR: Errore nell'estrazione testo
```
**Soluzione**: 
- Migliora la qualità del video
- Verifica l'angolazione della targa
- Controlla l'illuminazione

### Debug e Diagnostica

#### Controllo Log Backend
```bash
docker compose logs backend | grep -i "targa\|livestream"
```

#### Test API Manuale
```bash
# Test ricerca targa
curl -X GET "http://localhost:8000/api/v1/ai/plate/search/AB123CD"

# Test stato livestream
curl -X GET "http://localhost:8000/api/v1/ai/livestream/status"
```

## 📈 Statistiche e Metriche

### Dashboard Statistiche
- **Targhe rilevate oggi**: Numero di rilevazioni giornaliere
- **Appuntamenti trovati**: Corrispondenze con database
- **Tasso di accuratezza**: Percentuale di rilevazioni corrette
- **Immagini salvate**: Numero di foto targhe archiviate

### Metriche di Performance
- **FPS**: Frames per secondo processati
- **Latenza**: Tempo di risposta del riconoscimento
- **Memoria**: Utilizzo risorse sistema
- **CPU**: Carico di elaborazione

## 🔮 Sviluppi Futuri

### Funzionalità Pianificate
1. **Notifiche Push**: Avvisi in tempo reale per appuntamenti
2. **Analisi Avanzata**: Machine learning per migliorare accuratezza
3. **Integrazione SMS/Email**: Notifiche automatiche ai clienti
4. **Dashboard Analytics**: Statistiche avanzate e report
5. **Multi-camera**: Supporto per più stream simultanei

### Miglioramenti Tecnici
1. **OCR Avanzato**: Integrazione con servizi cloud (Google Vision, AWS Rekognition)
2. **Riconoscimento Veicoli**: Identificazione marca/modello
3. **Tracking Temporale**: Monitoraggio movimento veicoli
4. **Backup Automatico**: Sincronizzazione cloud delle immagini

## 📞 Supporto

Per assistenza tecnica o segnalazione problemi:
- Controlla i log del sistema
- Verifica la configurazione
- Consulta questa documentazione
- Contatta il team di sviluppo

---

**Nota**: Questo sistema è progettato per rispettare la privacy e la sicurezza. Tutte le immagini e i dati sono gestiti secondo le normative vigenti sulla protezione dei dati personali.
