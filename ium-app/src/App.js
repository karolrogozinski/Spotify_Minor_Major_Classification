import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [showPrediction, setShowPrediction] = useState(false);
  const [showExperiment, setShowExperiment] = useState(false);
  const [model, setShowModel] = useState(false);
  const [selectedTracksFile, setSelectedTracksFile] = useState(null);
  const [selectedArtistsFile, setSelectedArtistsFile] = useState(null);
  const [baseModel, setBaseModel] = useState(false)
  const [finalModel, setFinalModel] = useState(false)

  const [baseStats, setList1] = useState([]);
  const [finalStats, setList2] = useState([]);

  const handleTracksFileChange = (event) => {
    setSelectedTracksFile(event.target.files[0]);
  };

  const handleArtistsFileChange = (event) => {
    setSelectedArtistsFile(event.target.files[0]);
  };

  const handlePredictionClick = () => {
    setShowModel(true);
    setShowPrediction(false);
    setShowExperiment(false);
  };

  const handleExperimentClick = () => {
    setShowPrediction(false);
    setShowExperiment(true);
    setShowModel(false)
  };

  const handleBaseModelClick = () => {

    setBaseModel(true);
    setFinalModel(false);

    setShowModel(false);
    setShowPrediction(true);
    setShowExperiment(false);
  };

  const handleFinalModelClick = () => {

    setBaseModel(false);
    setFinalModel(true);

    setShowModel(false);
    setShowPrediction(true);
    setShowExperiment(false);
  };

  const handleCompareModels = () => {
    const formData = new FormData();
    formData.append('tracks', selectedTracksFile);
    formData.append('artists', selectedArtistsFile);

    axios
      .post('http://localhost:5000/experiment', formData)
      .then((response) => {
        const { baseStats, finalStats } = response.data;
        setList1(baseStats || []);
        setList2(finalStats || []);
      })
      .catch((error) => {
        console.error('Błąd podczas wysyłania żądania:', error);
      });

  }

  const handleGetBasePredictions = () => {
    const formData = new FormData();
    formData.append('file', selectedTracksFile);
  
    axios
      .post('http://localhost:5000/get-base-predictions', formData)
      .then((response) => {
        // setPrediction(response.data.predictions);
      })
      .catch((error) => {
        console.error('Błąd podczas wysyłania żądania:', error);
      });
  };

  const handleGetFinalPredictions = () => {
    const formData = new FormData();
    formData.append('tracks', selectedTracksFile);
    formData.append('artists', selectedArtistsFile);
  
    axios
      .post('http://localhost:5000/get-final-predictions', formData)
      .then((response) => {
        // setPrediction(response.data.predictions);
      })
      .catch((error) => {
        console.error('Błąd podczas wysyłania żądania:', error);
      });
  };

  return (
    
    <div>
      <div style={{ justifyContent: 'center', textAlign: 'center' }}>
      <h1>[IUM] - Projekt - Dur czy moll?</h1>

      <button onClick={handlePredictionClick}>SERWOWANIE PREDYKCJI</button>
      <span style={{ marginRight: '20px' }}></span>
      <button onClick={handleExperimentClick}>EKSPERYMENT</button>
      </div>
      {model && (
        <div>
          <h2>Wybierz model:</h2>
          <button onClick={handleBaseModelClick}>MODEL PODSTAWOWY</button>
          <span style={{ marginRight: '20px' }}></span>
          <button onClick={handleFinalModelClick}>MODEL DOCELOWY</button>

        </div>
      )}

      {baseModel && showPrediction && (
        <div style={{ justifyContent: 'center', textAlign: 'center' }}>
          <div>
            <h2>Serwowanie predykcji za pomocą modelu PODSTAWOWEGO.</h2>
            <h3>Aby otrzymać predykcje dotyczące trybu utworów, należy załadować plik z utworami w formacie .jsonl i nacisnąc przycisk 'POBIERZ PREDYKCJE'. </h3>
            <h3>Predykcje zostaną pobrane do pliku base_model_predictions.txt do folderu aplikacji.</h3>

            <input type="file" onChange={handleTracksFileChange} />

            <button onClick={handleGetBasePredictions}>POBIERZ PREDYKCJE</button>
          </div>
        </div>
      )}

      {finalModel && showPrediction && (
        <div style={{ justifyContent: 'center', textAlign: 'center' }}>
          <div>
            <h2>Serwowanie predykcji za pomocą modelu DOCELOWEGO.</h2>
            <h3>Aby otrzymać predykcje dotyczące trybu utworów, należy załadować plik z utworami oraz plik z artystami tychże utworów (oba w formacie .jsonl) i nacisnąć przycisk 'POBIERZ PREDYKCJE'. </h3>
            <h3>Predykcje zostaną pobrane do pliku final_model_predictions.txt do folderu aplikacji.</h3>

            <label>
              Tracks file:    
              <input type="file" onChange={handleTracksFileChange}/>
            </label>

            <label>
              Artists file:    
              <input type="file" onChange={handleArtistsFileChange}/>
            </label>

            <button onClick={handleGetFinalPredictions}>POBIERZ PREDYKCJE</button>
          </div>
        </div>
      )}

      {showExperiment && (
        <div style={{ justifyContent: 'center', textAlign: 'center' }}>
          <div>
            <h2>Eksperyment A/B</h2>
            <h3>Aby uzyskać informacje na temat danych jakościowych dotyczących działania obu modeli należy załadować pliki z utworami oraz artystami w formacie .jsonl oraz nacisnąć przycisk 'PORÓWNAJ MODELE'</h3>
            <h4>Wyniki zostaną wyświetlone na ekranie.</h4>

            <label>
              Tracks file:    
              <input type="file" onChange={handleTracksFileChange}/>
            </label>

            <label>
              Artists file:    
              <input type="file" onChange={handleArtistsFileChange}/>
            </label>

            <button onClick={handleCompareModels}>PORÓWNAJ MODELE</button>

            <div style={{ display: 'flex', justifyContent: 'center' }}>
              <div>
                <h3>Model postawowy:</h3>
                <ul>
                  {baseStats && baseStats.length > 0 ? (
                    baseStats.map((item, index) => <li key={index}>{item}</li>)
                  ) : (
                    <li>Brak statystyk do wyświetlenia</li>
                  )}
                </ul>
              </div>

              <div>
                <h3>Model docelowy:</h3>
                <ul>
                  {finalStats && finalStats.length > 0 ? (
                    finalStats.map((item, index) => <li key={index}>{item}</li>)
                  ) : (
                    <li>Brak statystyk do wyświetlenia</li>
                  )}
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
    
  );
};

export default App;
