import React, { useState } from 'react';

const PredictionForm = ({ handleGetPrediction }) => {
  const [number, setNumber] = useState('');

  const handleNumberChange = (event) => {
    setNumber(event.target.value);
  };

  return (
    <div>
      <input type="text" value={number} onChange={handleNumberChange} />
      <button onClick={() => handleGetPrediction(number)}>GET PREDICTION</button>
    </div>
  );
};

export default PredictionForm;
