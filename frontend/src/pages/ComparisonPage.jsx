import { useState, useEffect } from 'react';

function ComparisonPage() {
  const [songs, setSongs] = useState(['']);
  const [score, setScore] = useState('');

  // Fetch 2 random songs when the component loads
  const fetchRandomSongs = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/random-songs');
      const data = await response.json();
      setSongs([data.song,data.song2]);
    } catch (error) {
      console.error("Error fetching random songs:", error);
    }
  };

  useEffect(() => {
    fetchRandomSongs();
  },[]);


  // TODO - define fucntion to submit data to http://localhost:5000/api/compare, method = POST
  const submitComparisonData = async () => {
    return
  };

  return (
    <div>
      <h2>Rate the similarity of these 2 songs:</h2>
      <p> {songs[0]} {songs[1]}</p>
    </div>
  );
}

export default ComparisonPage;