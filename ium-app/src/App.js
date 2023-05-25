import React, { useState } from 'react';
import FileUploader from './FileUploader';
import PredictionForm from './PredictionForm';
import axios from 'axios';

// function App() {
//   const [prediction, setPrediction] = useState('');

//   const handleFileUpload = (file) => {
//     // Add code to handle file upload
//   };

//   const handleGetPrediction = (number) => {
//     axios
//       .post('http://localhost:5000/get-prediction', { number: number })
//       .then((response) => {
//         setPrediction(response.data.result);
//         console.log(number);
//       })
//       .catch((error) => {
//         console.error('Błąd podczas wysyłania żądania:', error);
//       });
//   };

//   return (
//     <div>
//       <h1>IUM Projekt - 23L</h1>
//       <button>SERWOWANIE PREDYKCJI</button>
//       <button>EKSPERYMENT A/B</button>
//       <FileUploader handleFileUpload={handleFileUpload} />
//       <PredictionForm handleGetPrediction={handleGetPrediction} />
//       <p>Prediction: {prediction}</p>
//     </div>
//   );
// }

// export default App;

const App = () => {
  const [prediction, setPrediction] = useState('');
  const [showPrediction, setShowPrediction] = useState(false);
  const [showExperiment, setShowExperiment] = useState(false);

  const handlePredictionClick = () => {
    setShowPrediction(true);
    setShowExperiment(false);
  };

  const handleExperimentClick = () => {
    setShowPrediction(false);
    setShowExperiment(true);
  };

  const handleFileUpload = (file) => {
    // Dodaj kod obsługi ładowania pliku
  };


  const handleGetPrediction = (number) => {
        axios
          .post('http://localhost:5000/get-prediction', { number: number })
          .then((response) => {
            setPrediction(response.data.result);
          })
          .catch((error) => {
            console.error('Błąd podczas wysyłania żądania:', error);
          });
      };

  return (
    <div>
      <h1>[IUM] - Projekt - Dur czy moll?</h1>

      <button onClick={handlePredictionClick}>SERWOWANIE PREDYKCJI</button>
      <button onClick={handleExperimentClick}>EKSPERYMENT</button>

      {showPrediction && (
        <div>
          <h2>Serwowanie predykcji</h2>
          {/* Komponent FileUploader do ładowania pliku */}
          <FileUploader handleFileUpload={handleFileUpload} />
          {/* Komponent PredictionForm do wprowadzania danych i wywoływania predykcji */}
          <PredictionForm handleGetPrediction={handleGetPrediction} />
          <p>Prediction: {prediction}</p>
        </div>
      )}

      {showExperiment && (
        <div>
          <h2>Eksperyment</h2>
          <p>eksperyment</p>
        </div>
      )}
    </div>
  );
};

export default App;
