import React, { useState } from 'react';

const EvaluateRule = ({ onEvaluate }) => {
  const [data, setData] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (data) {
      try {
        const parsedData = JSON.parse(data);
        onEvaluate(parsedData);
        setData('');
      } catch (error) {
        alert('Invalid JSON format. Please check your input.');
      }
    }
  };

  return (
    <div>
      <h2>Evaluate Rule</h2>
      <form onSubmit={handleSubmit}>
        <textarea 
          value={data} 
          onChange={(e) => setData(e.target.value)} 
          placeholder='{"age": 35, "department": "Sales", "salary": 60000}'
        />
        <button type="submit">Evaluate Rule</button>
      </form>
    </div>
  );
};

export default EvaluateRule;
