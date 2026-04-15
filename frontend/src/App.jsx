import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import RecPage from './pages/RecPage';
import ComparisonPage from './pages/ComparisonPage';
import './App.css';
import SignupPage from './pages/SignupPage';

function App() {
  return (
    <Router>
      <div className="App">
        <nav style={{ padding: '20px', backgroundColor: '#282c34', color: 'white' }}>
          <Link to="/" style={{ margin: '10px', color: 'white' }}>Home</Link>
          <Link to="/recommend" style={{ margin: '10px', color: 'white' }}>Get Recommendations</Link>
          <Link to="/compare" style={{ margin: '10px', color: 'white' }}>Compare Songs</Link>
          <Link to="/signup" style={{ margin: '10px', color: 'white' }}>Help Us Train Our Data</Link>
        </nav>
        <div style={{ padding: '20px' }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/recommend" element={<RecPage />} />
            <Route path="/compare" element={<ComparisonPage />} />
            <Route path="/signup" element={<SignupPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
