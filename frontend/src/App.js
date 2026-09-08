import { useState, useEffect } from "react";

function App() {
  const [reps, setReps] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/representatives")
      .then((res) => res.json())
      .then((data) => setReps(data));
  }, []);

  return (
    <div>
      <h1>Representatives</h1>
      <ul>
        {reps.map((rep) => (
          <li key={rep.id}>
            {rep.name} — {rep.office} ({rep.state})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;