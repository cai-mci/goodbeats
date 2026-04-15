import { useState } from 'react';

function SignupPage() {
  
  const [email, setEmail] = useState("");
  const [first, setFirst] = useState("");
  const [last, setLast] = useState("");
  const [loading, setLoading] = useState(false);
  
  const submitSignup = async () => {
        const fetchRecommendations = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
        const response = await fetch(`http://localhost:5000/api/signup?email=${encodeURIComponent(email)}&first=${encodeURIComponent(first)}&last=${encodeURIComponent(last)}`);
        } catch (error) {
        console.error("Error submitting information:", error);
        }
        setLoading(false);
    };
  }


  return (
    <div>
      <h2>Sign up to help us train our model.</h2>
      <p> To train our model on similarity, we need lots of human opinions on how different songs compare. 
        <br />
        <b>If you love music, sign up to help us!</b> </p>
    
      <form onSubmit={submitSignup}>
        <input 
          type="text" 
          placeholder="Enter your email..." 
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={{ padding: '8px', width: '250px' }}
        />
        <input 
          type="text" 
          placeholder="First Name" 
          value={first}
          onChange={(e) => setFirst(e.target.value)}
          required
          style={{ padding: '8px', width: '250px' }}
        />
        <input 
          type="text" 
          placeholder="Last Name" 
          value={last}
          onChange={(e) => setLast(e.target.value)}
          required
          style={{ padding: '8px', width: '250px' }}
        />
        <button type="submit" style={{ padding: '8px 15px', marginLeft: '10px' }}>
          {loading ? 'Submitting...' : 'Sign Up'}
        </button>
      </form>


    </div>
  );
}

export default SignupPage;