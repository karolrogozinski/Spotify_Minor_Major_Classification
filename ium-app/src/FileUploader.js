import React from 'react';

const FileUploader = ({ handleFileUpload }) => {
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    handleFileUpload(file);
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
    </div>
  );
};

export default FileUploader;