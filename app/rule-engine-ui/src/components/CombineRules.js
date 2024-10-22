import React, { useState } from 'react';

const CombineRules = ({ onCombine }) => {
  const [rules, setRules] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (rules) {
      onCombine(rules.split(',').map(rule => rule.trim())); // Trim whitespace
      setRules('');
    }
  };

  return (
    <div>
      <h2>Combine Rules</h2>
      <form onSubmit={handleSubmit}>
        <input 
          type="text" 
          value={rules} 
          onChange={(e) => setRules(e.target.value)} 
          placeholder="e.g., rule1, rule2"
        />
        <button type="submit">Combine Rules</button>
      </form>
    </div>
  );
};

export default CombineRules;
