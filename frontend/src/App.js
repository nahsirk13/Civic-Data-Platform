import { useState } from "react";
import "./App.css";

function App() {
  const [reps, setReps] = useState([]);
  const [district, setDistrict] = useState("");
  const [state, setState] = useState("");
  const [bills, setBills] = useState([]);
  const [billsFor, setBillsFor] = useState("");

  const handleSearch = () => {
    const params = new URLSearchParams();
    if (district) params.append("district", district);
    if (state) params.append("state", state);

    fetch(`http://127.0.0.1:8000/representatives/lookup?${params}`)
      .then((res) => res.json())
      .then((data) => setReps(data));
  };

  const fetchBills = (name) => {
    setBillsFor(name);
    fetch(`http://127.0.0.1:8000/openstates/recent-bills?name=${encodeURIComponent(name)}`)
      .then((res) => res.json())
      .then((data) => setBills(data.results || []));
  };

  return (
    <div className="container">
      <h1>Find Your Representative</h1>
      <div className="search-bar">
        <input
          placeholder="District (e.g. 30)"
          value={district}
          onChange={(e) => setDistrict(e.target.value)}
        />
        <input
          placeholder="State (e.g. NY)"
          value={state}
          onChange={(e) => setState(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>
      </div>
      <ul className="rep-list">
        {reps.map((rep) => (
          <li key={rep.id} className="rep-card">
            <strong>{rep.name}</strong>
            <span>{rep.office}</span>
            <span>
              {rep.state} {rep.district && `— District ${rep.district}`}
            </span>
            <button onClick={() => fetchBills(rep.name)}>Recent bills</button>
            {billsFor === rep.name && (
              <ul className="bills-list">
                {bills.length > 0 ? (
                  bills.map((bill, i) => <li key={i}>{bill.title}</li>)
                ) : (
                  <li>No recent bills found</li>
                )}
              </ul>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;