import React, { useState, useEffect } from 'react';
import { 
  VideoCameraIcon, 
  CpuChipIcon, 
  ChartBarIcon, 
  PlayIcon, 
  StopIcon, 
  MagnifyingGlassIcon,
  EyeIcon,
  XMarkIcon,
  CameraIcon,
  DocumentMagnifyingGlassIcon
} from '@heroicons/react/24/outline';
import { aiApi } from '../services/api';

interface Detection {
  id: number;
  license_plate: string;
  confidence_score: number;
  detection_data: any;
  is_automatic: boolean;
  created_at: string;
}

interface LivestreamStatus {
  is_streaming: boolean;
  is_task_running: boolean;
  status: 'active' | 'inactive';
}

interface PlateImage {
  filename: string;
  license_plate: string;
  timestamp: string;
  filepath: string;
  size: number;
}

const LivestreamMonitor: React.FC = () => {
  const [streamUrl, setStreamUrl] = useState('rtsp://127.0.0.1:8554/webcam');
  const [outputUrl, setOutputUrl] = useState('');
  const [status, setStatus] = useState<LivestreamStatus | null>(null);
  const [recentDetections, setRecentDetections] = useState<Detection[]>([]);
  const [plateImages, setPlateImages] = useState<PlateImage[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchPlate, setSearchPlate] = useState('');
  const [searchResult, setSearchResult] = useState<any>(null);
  const [searchDialogOpen, setSearchDialogOpen] = useState(false);
  const [selectedTab, setSelectedTab] = useState(0);
  const [selectedImage, setSelectedImage] = useState<PlateImage | null>(null);
  const [imageDialogOpen, setImageDialogOpen] = useState(false);

  useEffect(() => {
    loadStatus();
    loadRecentDetections();
    loadPlateImages();
    
    // Polling per aggiornare lo stato ogni 5 secondi
    const interval = setInterval(() => {
      loadStatus();
      loadRecentDetections();
      loadPlateImages();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const loadStatus = async () => {
    try {
      const response = await aiApi.getLivestreamStatus();
      setStatus(response.data);
    } catch (error) {
      console.error('Errore nel caricamento status:', error);
    }
  };

  const loadRecentDetections = async () => {
    try {
      const response = await aiApi.getRecentDetections();
      const detections = Array.isArray(response.data) ? response.data : [];
      setRecentDetections(detections);
    } catch (error) {
      console.error('Errore nel caricamento rilevamenti:', error);
      setRecentDetections([]);
    }
  };

  const loadPlateImages = async () => {
    try {
      const response = await aiApi.getPlateImages();
      // Assicurati che sia sempre un array
      const images = Array.isArray(response.data) ? response.data : [];
      setPlateImages(images);
    } catch (error) {
      console.error('Errore nel caricamento immagini:', error);
      setPlateImages([]);
    }
  };

  const startAITask = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Usa sempre lo stream fisso
      const fixedStreamUrl = 'rtsp://127.0.0.1:8554/webcam';
      await aiApi.startLivestream(fixedStreamUrl, outputUrl, {
        enable_face_blur: true,
        enable_plate_blur: true,
        save_plate_images: true
      });
      
      loadStatus();
    } catch (error) {
      console.error('Errore nell\'avvio del task AI:', error);
      setError('Errore nell\'avvio del task AI');
    } finally {
      setLoading(false);
    }
  };

  const stopAITask = async () => {
    try {
      setLoading(true);
      setError(null);
      
      await aiApi.stopLivestream();
      
      loadStatus();
    } catch (error) {
      console.error('Errore nell\'arresto del task AI:', error);
      setError('Errore nell\'arresto del task AI');
    } finally {
      setLoading(false);
    }
  };

  const handleSearchPlate = async () => {
    if (!searchPlate.trim()) return;
    
    try {
      setLoading(true);
      const response = await aiApi.searchPlate(searchPlate);
      setSearchResult(response.data);
      setSearchDialogOpen(true);
    } catch (error) {
      console.error('Errore nella ricerca targa:', error);
      setError('Errore nella ricerca della targa');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('it-IT');
  };

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Monitoraggio Livestream AI</h1>
          <p className="text-gray-600">Sistema di monitoraggio automatico con rilevamento targhe</p>
        </div>
        
        <div className="flex space-x-3">
          <button
            onClick={stopAITask}
            disabled={loading || !status?.is_task_running}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <StopIcon className="h-4 w-4 mr-2" />
            {loading ? 'Arresto...' : 'Ferma Monitoraggi'}
          </button>
        </div>
      </div>

      {/* Error Alert */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {/* Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-blue-50">
              <VideoCameraIcon className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Status Stream</p>
              <p className="text-lg font-semibold text-gray-900">
                {status?.is_streaming ? 'Attivo' : 'Inattivo'}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-green-50">
              <CpuChipIcon className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Task AI</p>
              <p className="text-lg font-semibold text-gray-900">
                {status?.is_task_running ? 'In Esecuzione' : 'Fermato'}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-purple-50">
              <ChartBarIcon className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Rilevamenti</p>
              <p className="text-lg font-semibold text-gray-900">
                {recentDetections.length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Stream Configuration */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Configurazione Stream</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              URL Stream RTSP
            </label>
            <input
              type="text"
              value={streamUrl}
              onChange={(e) => setStreamUrl(e.target.value)}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="rtsp://127.0.0.1:8554/webcam"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              URL Stream Output (opzionale)
            </label>
            <input
              type="text"
              value={outputUrl}
              onChange={(e) => setOutputUrl(e.target.value)}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="output.avi per salvare video con blur"
            />
          </div>
          
          <div className="flex space-x-3">
            <button
              onClick={startAITask}
              disabled={loading || status?.is_task_running}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <PlayIcon className="h-4 w-4 mr-2" />
              Avvia
            </button>
            <button
              onClick={stopAITask}
              disabled={loading || !status?.is_task_running}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <StopIcon className="h-4 w-4 mr-2" />
              Ferma
            </button>
          </div>
        </div>
      </div>

      {/* Search Plate */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Cerca Targa</h2>
        <div className="flex space-x-3">
          <input
            type="text"
            value={searchPlate}
            onChange={(e) => setSearchPlate(e.target.value)}
            placeholder="Inserisci targa da cercare..."
            className="block flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
          <button
            onClick={handleSearchPlate}
            disabled={loading || !searchPlate.trim()}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <MagnifyingGlassIcon className="h-4 w-4 mr-2" />
            Cerca
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            <button
              onClick={() => setSelectedTab(0)}
              className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center ${
                selectedTab === 0
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <DocumentMagnifyingGlassIcon className="h-4 w-4 mr-2" />
              Rilevamenti Recenti
            </button>
            <button
              onClick={() => setSelectedTab(1)}
              className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center ${
                selectedTab === 1
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <CameraIcon className="h-4 w-4 mr-2" />
              Immagini Targhe
            </button>
          </nav>
        </div>

        <div className="p-6">
          {selectedTab === 0 && (
            <div className="space-y-4">
              <h3 className="text-lg font-medium text-gray-900">Rilevamenti Recenti</h3>
              {!Array.isArray(recentDetections) || recentDetections.length === 0 ? (
                <p className="text-gray-500">Nessun rilevamento recente</p>
              ) : (
                <div className="space-y-3">
                  {recentDetections.map((detection) => (
                    <div key={detection.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div className="flex items-center space-x-4">
                        <div className="p-2 rounded-full bg-blue-50">
                          <VideoCameraIcon className="h-5 w-5 text-blue-600" />
                        </div>
                        <div>
                          <p className="font-medium text-gray-900">{detection.license_plate}</p>
                          <p className="text-sm text-gray-500">
                            Confidenza: {(detection.confidence_score * 100).toFixed(1)}%
                          </p>
                          <p className="text-sm text-gray-500">
                            {formatDate(detection.created_at)}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          detection.is_automatic ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'
                        }`}>
                          {detection.is_automatic ? 'Automatico' : 'Manuale'}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {selectedTab === 1 && (
            <div className="space-y-4">
              <h3 className="text-lg font-medium text-gray-900">Immagini Targhe Salvate</h3>
              {!Array.isArray(plateImages) || plateImages.length === 0 ? (
                <p className="text-gray-500">Nessuna immagine salvata</p>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {plateImages.map((image) => (
                    <div key={image.filename} className="border border-gray-200 rounded-lg overflow-hidden">
                      <div className="p-4">
                        <p className="font-medium text-gray-900">{image.license_plate}</p>
                        <p className="text-sm text-gray-500">{formatDate(image.timestamp)}</p>
                        <p className="text-sm text-gray-500">{(image.size / 1024).toFixed(1)} KB</p>
                      </div>
                      <div className="px-4 pb-4">
                        <button
                          onClick={() => {
                            setSelectedImage(image);
                            setImageDialogOpen(true);
                          }}
                          className="inline-flex items-center justify-center w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                        >
                          <EyeIcon className="h-4 w-4 mr-2" />
                          Visualizza
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Search Result Dialog */}
      {searchDialogOpen && searchResult && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-xl max-w-md w-full">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold text-gray-900">Risultato Ricerca</h2>
                <button
                  onClick={() => setSearchDialogOpen(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <XMarkIcon className="h-6 w-6" />
                </button>
              </div>
              
              <div className="space-y-4">
                <div>
                  <p className="text-sm font-medium text-gray-600">Targa</p>
                  <p className="text-lg font-semibold text-gray-900">{searchResult.license_plate}</p>
                </div>
                
                {searchResult.vehicle && (
                  <div>
                    <p className="text-sm font-medium text-gray-600">Veicolo</p>
                    <p className="text-gray-900">
                      {searchResult.vehicle.brand} {searchResult.vehicle.model} ({searchResult.vehicle.year})
                    </p>
                  </div>
                )}
                
                {searchResult.customer && (
                  <div>
                    <p className="text-sm font-medium text-gray-600">Proprietario</p>
                    <p className="text-gray-900">{searchResult.customer.full_name}</p>
                  </div>
                )}
                
                {searchResult.appointments && searchResult.appointments.length > 0 && (
                  <div>
                    <p className="text-sm font-medium text-gray-600">Appuntamenti Oggi</p>
                    <div className="space-y-2">
                      {searchResult.appointments.map((appointment: any, index: number) => (
                        <div key={index} className="p-3 bg-blue-50 rounded-lg">
                          <p className="font-medium text-blue-900">
                            {new Date(appointment.appointment_date).toLocaleTimeString('it-IT')}
                          </p>
                          <p className="text-sm text-blue-700">{appointment.service?.name}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                
                {(!searchResult.vehicle && !searchResult.customer && (!searchResult.appointments || searchResult.appointments.length === 0)) && (
                  <div className="p-4 bg-yellow-50 rounded-lg">
                    <p className="text-yellow-800">Nessuna informazione trovata per questa targa</p>
                  </div>
                )}
              </div>
              
              <div className="flex justify-end mt-6">
                <button
                  onClick={() => setSearchDialogOpen(false)}
                  className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Chiudi
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Image Dialog */}
      {imageDialogOpen && selectedImage && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-xl max-w-2xl w-full">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold text-gray-900">
                  Immagine Targa: {selectedImage.license_plate}
                </h2>
                <button
                  onClick={() => setImageDialogOpen(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <XMarkIcon className="h-6 w-6" />
                </button>
              </div>
              
              <div className="space-y-4">
                <div className="bg-gray-100 rounded-lg p-4 text-center">
                  <p className="text-gray-600">Immagine non disponibile nel frontend</p>
                  <p className="text-sm text-gray-500 mt-2">
                    Percorso: {selectedImage.filepath}
                  </p>
                </div>
                
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="font-medium text-gray-600">Targa</p>
                    <p className="text-gray-900">{selectedImage.license_plate}</p>
                  </div>
                  <div>
                    <p className="font-medium text-gray-600">Data/Ora</p>
                    <p className="text-gray-900">{formatDate(selectedImage.timestamp)}</p>
                  </div>
                  <div>
                    <p className="font-medium text-gray-600">Dimensione</p>
                    <p className="text-gray-900">{(selectedImage.size / 1024).toFixed(1)} KB</p>
                  </div>
                  <div>
                    <p className="font-medium text-gray-600">Nome File</p>
                    <p className="text-gray-900">{selectedImage.filename}</p>
                  </div>
                </div>
              </div>
              
              <div className="flex justify-end mt-6">
                <button
                  onClick={() => setImageDialogOpen(false)}
                  className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Chiudi
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default LivestreamMonitor;
