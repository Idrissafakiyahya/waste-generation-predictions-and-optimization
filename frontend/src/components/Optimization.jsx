import { useEffect, useState } from 'react';
import './Optimization.css';

const API_BASE = '/api';

export default function Optimization() {
  const [schedule, setSchedule] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSchedule();
  }, []);

  const fetchSchedule = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE}/optimization/schedule/`);
      const data = await response.json();

      if (data.success) {
        setSchedule(data.data || []);
      } else {
        setError(data.error || 'Failed to load optimization schedule.');
      }
    } catch (err) {
      setError('Unable to connect to optimization service.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const summary = schedule.reduce(
    (acc, item) => {
      const level = String(item.predicted_level).toLowerCase();
      if (level.includes('full') || level.includes('high')) acc.high += 1;
      else if (level.includes('medium')) acc.medium += 1;
      else acc.low += 1;
      return acc;
    },
    { high: 0, medium: 0, low: 0 }
  );

  return (
    <div className="optimization-page">
      <section className="optimization-hero">
        <div className="optimization-header">
          <h1>Optimization Dashboard</h1>
          <p>Real-time schedule recommendations based on predicted waste levels across reported bins.</p>
        </div>
        <div className="optimization-summary-cards">
          <div className="summary-card high-card">
            <h3>High Priority</h3>
            <p>{summary.high}</p>
          </div>
          <div className="summary-card medium-card">
            <h3>Medium Priority</h3>
            <p>{summary.medium}</p>
          </div>
          <div className="summary-card low-card">
            <h3>Low Priority</h3>
            <p>{summary.low}</p>
          </div>
        </div>
      </section>

      <section className="optimization-content">
        <div className="optimization-panel">
          <div className="panel-header">
            <h2>Real-time Collection Schedule</h2>
            <button className="btn btn-secondary" onClick={fetchSchedule}>
              Refresh Schedule
            </button>
          </div>

          {loading ? (
            <div className="panel-loading">Loading schedule...</div>
          ) : error ? (
            <div className="panel-error">{error}</div>
          ) : schedule.length === 0 ? (
            <div className="panel-empty">No scheduled bins available yet.</div>
          ) : (
            <table className="optimization-table">
              <thead>
                <tr>
                  <th>Shehia</th>
                  <th>Bin</th>
                  <th>Current Level</th>
                  <th>Predicted Level</th>
                  <th>Priority</th>
                  <th>Collection Due</th>
                </tr>
              </thead>
              <tbody>
                {schedule.map((item, index) => (
                  <tr key={`${item.shehia}-${item.bin}-${index}`}>
                    <td>{item.shehia}</td>
                    <td>{item.bin}</td>
                    <td>{item.current_report_level || 'Unknown'}</td>
                    <td>{item.predicted_level}</td>
                    <td>{item.priority}</td>
                    <td>{item.recommended_collection}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </section>
    </div>
  );
}
