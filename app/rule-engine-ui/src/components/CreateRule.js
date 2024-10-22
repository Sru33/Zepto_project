import React, { useState } from 'react';

const CreateRule = ({ onAddRule }) => {
  const [rule, setRule] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (rule) {
      onAddRule(rule);
      setRule('');
    }
  };

  return (
    <div>
      <h2>Create a Rule</h2>
      <form onSubmit={handleSubmit}>
        <input 
          type="text" 
          value={rule} 
          onChange={(e) => setRule(e.target.value)} 
          placeholder="e.g., age > 30 AND department = 'Sales'"
        />
        <button type="submit">Create Rule</button>
      </form>
    </div>
  );
};

export default CreateRule;
