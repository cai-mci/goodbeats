import { useState } from 'react';

function RecPage() {
  
  const [song, setSong] = useState('');
  const[recs, setRecs] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchRecommendations = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:5000/api/recommend?song=${encodeURIComponent(song)}`);
      const data = await response.json();
      setRecs(data.message);
    } catch (error) {
      console.error("Error fetching recommendations:", error);
    }
    setLoading(false);
  };

  return (
    <div>
      <h2>Find Similar Songs</h2>
      <form onSubmit={fetchRecommendations}>
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
      <p> {recs} </p>
    </div>
  );
}

export default RecPage;