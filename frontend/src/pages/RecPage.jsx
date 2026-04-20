import { useState } from 'react';

function RecPage() {
  
  const [song, setSong] = useState('');
  const[recs, setRecs] = useState([]);
  const [loading, setLoading] = useState(false);
  const fetchRecommendations = async (e) => {
    e.preventDefault();
    setLoading(true);
    setRecs([]);
    try {
      //const response = await fetch(`http://localhost:5000/api/recommend?song=${encodeURIComponent(song)}`);
      const response = await fetch(`https://goodbeats.onrender.com/api/recommend?song=${encodeURIComponent(song)}`);

      // const response = await fetch(`http://127.0.0.1:5000/api/recommend?song=${encodeURIComponent(song)}`);
      const data = await response.json();
      console.log("full response", data);
      if (data.message){
        setRecs(data.message);
      }
      //setRecs(data.message);
    } catch (error) {
      console.error("Error fetching recommendations:", error);
    }
    setLoading(false);
  };

  return (
    <div>
      <h2>Find Similar Songs</h2>
      <form onSubmit={(e) => fetchRecommendations(e)}>
        <input 
          type="text" 
          placeholder="Enter a song name..." 
          value={song}
          onChange={(e) => setSong(e.target.value)}
          required
          style={{ padding: '8px', width: '250px' }}
        />
        <button type="submit" style={{ padding: '8px 15px', marginLeft: '10px' }}>
          {loading ? 'Searching...' : 'Get Recommendations'}
        </button>
      </form>

      <h3>Recommended for you:</h3>
      {!loading && recs.length>0 &&(
        <div>
          <p>Found {recs.length} similar songs</p>
          <ul style={{listStyle: 'none', padding: 0}}>
            {recs.map((rec, index)=>(
              <li key={index} style={{
                marginBottom: '10px',
                padding: '10px',
                border: '1px solid #ddd',
                borderRadius: '5px',
              }}><strong>{rec[0]}</strong>
                <span style={{color: '#666',marginLeft:'5px'}}>by</span>
                <span style={{marginLeft:'5px'}}>{rec[1]}</span>
                </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default RecPage;