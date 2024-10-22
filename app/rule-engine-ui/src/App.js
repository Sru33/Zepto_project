import React, { useState } from 'react';
import CreateRule from './components/CreateRule';
import CombineRules from './components/CombineRules';
import EvaluateRule from './components/EvaluateRule';
import './App.css'; // Import the CSS file

const App = () => {
  const [rules, setRules] = useState([]);
  const [combinedRule, setCombinedRule] = useState('');

  const addRule = (newRule) => {
    setRules((prevRules) => [...prevRules, newRule]);
  };

  const combineRules = (rulesToCombine) => {
    const combined = rulesToCombine.join(' AND ');
    setCombinedRule(combined);
  };

  const evaluateRule = (data) => {
    const rulesArray = combinedRule.split(' AND ');
    const results = rulesArray.map((rule) => {
      const [attribute, condition] = rule.split(/(?<=\w) (?=\W)/);
      const [operator, value] = condition.trim().split(/(?<=\D) (?=\d)/);
      switch (operator) {
        case '>':
          return data[attribute] > Number(value);
        case '<':
          return data[attribute] < Number(value);
        case '=':
          return data[attribute] === value.replace(/'/g, '');
        default:
          return false;
      }
    });

    console.log('Evaluation Results:', results);
    alert(`Evaluation Result: ${results.every(res => res) ? 'All rules satisfied' : 'Some rules not satisfied'}`);
  };

  return (
    <div className="container">
      <h1>Rule Engine UI</h1>
      <CreateRule onAddRule={addRule} />
      <CombineRules onCombine={combineRules} />
      <EvaluateRule onEvaluate={evaluateRule} />
      
      <div>
        <h3>Created Rules:</h3>
        <ul>
          {rules.map((rule, index) => (
            <li key={index}>{rule}</li>
          ))}
        </ul>
        
        <h3>Combined Rule:</h3>
        <p>{combinedRule}</p>
      </div>
    </div>
  );
};

export default App;