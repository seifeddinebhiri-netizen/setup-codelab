import { useState } from 'react'

import './App.css'
import axios from 'axios'

function App() {
  const [ticker, setTicker] = useState('')
  const [stockData, setStockData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const fetchStock = async () => {
    if (!ticker) return;
    setLoading(true);
    setError('');
    setStockData(null);

    try {
      // connecting to your local FastAPI backend
      const response = await axios.get(`http://localhost:8000/stock/${ticker}`);
      setStockData(response.data);
    } catch (err) {
      setError('Stock not found or backend is offline.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '2rem', textAlign: 'center' }}>
      <h1>💸 FinTech AI Dashboard</h1>
      
      <div style={{ display: 'flex', gap: '10px', justifyContent: 'center', marginBottom: '20px' }}>
        <input 
          type="text" 
          value={ticker}
          onChange={(e) => setTicker(e.target.value.toUpperCase())}
          placeholder="Enter Symbol (e.g., AAPL)"
          style={{ padding: '10px', fontSize: '16px' }}
        />
        <button onClick={fetchStock} disabled={loading} style={{ padding: '10px 20px' }}>
          {loading ? 'Analyzing...' : 'Get Data'}
        </button>
      </div>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {stockData && (
        <div style={{ border: '1px solid #ccc', borderRadius: '10px', padding: '20px', marginTop: '20px' }}>
          <h2>{stockData.symbol}</h2>
          <h1 style={{ color: '#4CAF50', fontSize: '3rem', margin: '10px 0' }}>
            ${stockData.price}
          </h1>
          <div style={{ background: '#f0f0f0', padding: '10px', borderRadius: '5px' }}>
            <strong>🤖 AI Insight:</strong>
            <p>{stockData.ai_message}</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
