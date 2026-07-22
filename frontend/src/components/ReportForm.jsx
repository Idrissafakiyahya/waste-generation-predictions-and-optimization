import { useState, useEffect } from 'react';
import './ReportForm.css';

const API_BASE = '/api';

export default function ReportForm() {
  const [shehias, setShehias] = useState([]);
  const [bins, setBins] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState(null);

  const [formData, setFormData] = useState({
    shehia_id: '',
    bin_id: '',
    timestamp: new Date().toISOString().slice(0, 16),
    waste_level: 'unknown',
    description: '',
  });

  // Fetch Shehias on component mount
  useEffect(() => {
    fetchShehias();
  }, []);

  // Fetch Bins when Shehia changes
  useEffect(() => {
    if (formData.shehia_id) {
      fetchBins(formData.shehia_id);
      setFormData(prev => ({ ...prev, bin_id: '' }));
    } else {
      setBins([]);
    }
  }, [formData.shehia_id]);

  const fetchShehias = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE}/shehias/`);
      const data = await response.json();
      if (data.success) {
        setShehias(data.data);
      } else {
        setMessage({ type: 'error', text: 'Failed to load Shehias' });
      }
    } catch (error) {
      console.error('Error fetching shehias:', error);
      setMessage({ type: 'error', text: 'Error loading Shehias. Please check your connection.' });
    } finally {
      setLoading(false);
    }
  };

  const fetchBins = async (shehiaId) => {
    try {
      const response = await fetch(`${API_BASE}/bins/?shehia_id=${shehiaId}`);
      const data = await response.json();
      if (data.success) {
        setBins(data.data);
      } else {
        setBins([]);
        setMessage({ type: 'error', text: 'Failed to load Bins' });
      }
    } catch (error) {
      console.error('Error fetching bins:', error);
      setMessage({ type: 'error', text: 'Error loading Bins' });
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
    // Clear any existing message when user starts typing
    if (message) setMessage(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate required fields
    if (!formData.shehia_id || !formData.bin_id || !formData.timestamp || formData.waste_level === 'unknown') {
      setMessage({ type: 'error', text: 'Please fill in all required fields and choose a waste level' });
      return;
    }

    const isoTimestamp = formData.timestamp.endsWith('Z')
      ? formData.timestamp
      : new Date(formData.timestamp).toISOString();

    try {
      setSubmitting(true);
      const response = await fetch(`${API_BASE}/reports/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          shehia_id: parseInt(formData.shehia_id),
          bin_id: parseInt(formData.bin_id),
          timestamp: isoTimestamp,
          waste_level: formData.waste_level,
          description: formData.description,
        }),
      });

      const data = await response.json();

      if (data.success) {
        setMessage({ type: 'success', text: 'Report submitted successfully! Thank you for helping keep our community clean.' });
        // Reset form
        setFormData({
          shehia_id: '',
          bin_id: '',
          timestamp: new Date().toISOString().slice(0, 16),
          waste_level: 'unknown',
          description: '',
        });
      } else {
        setMessage({ type: 'error', text: data.error || 'Failed to submit report' });
      }
    } catch (error) {
      console.error('Error submitting report:', error);
      setMessage({ type: 'error', text: 'Error submitting report. Please try again.' });
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="report-page">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  const selectedShehia = shehias.find(s => s.id === parseInt(formData.shehia_id));

  return (
    <div className="report-page">
      <section className="report-hero">
        <h1>Report Waste Issue</h1>
        <p>Help us maintain a clean community</p>
      </section>

      <div className="report-container">
        <form onSubmit={handleSubmit} className="report-form">
          {/* Message Display */}
          {message && (
            <div className={`message message-${message.type}`}>
              {message.type === 'success' ? '✓ ' : '✕ '}
              {message.text}
            </div>
          )}

          {/* Form Fields */}
          <div className="form-group">
            <label htmlFor="shehia_id" className="form-label">
              Shehia (Location) <span className="required">*</span>
            </label>
            <select
              id="shehia_id"
              name="shehia_id"
              value={formData.shehia_id}
              onChange={handleInputChange}
              className="form-control"
              required
            >
              <option value="">Select a Shehia</option>
              {shehias.map(shehia => (
                <option key={shehia.id} value={shehia.id}>
                  {shehia.name} {shehia.description ? `- ${shehia.description}` : ''}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="bin_id" className="form-label">
              Waste Bin <span className="required">*</span>
            </label>
            <select
              id="bin_id"
              name="bin_id"
              value={formData.bin_id}
              onChange={handleInputChange}
              className="form-control"
              required
              disabled={!formData.shehia_id}
            >
              <option value="">
                {formData.shehia_id ? 'Select a Bin' : 'First select a Shehia'}
              </option>
              {bins.map(bin => (
                <option key={bin.id} value={bin.id}>
                  {bin.name} {bin.location}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="timestamp" className="form-label">
              Timestamp <span className="required">*</span>
            </label>
            <input
              id="timestamp"
              type="datetime-local"
              name="timestamp"
              value={formData.timestamp}
              onChange={handleInputChange}
              className="form-control"
              required
            />
            <small className="form-hint">When did you observe this issue?</small>
          </div>

          <div className="form-group">
            <label htmlFor="waste_level" className="form-label">
              Waste Level <span className="required">*</span>
            </label>
            <select
              id="waste_level"
              name="waste_level"
              value={formData.waste_level}
              onChange={handleInputChange}
              className="form-control"
              required
            >
              <option value="unknown">Select waste level</option>
              <option value="low">Low (25%)</option>
              <option value="medium">Medium (50%)</option>
              <option value="high">High (75%)</option>
              <option value="full">Full (100%)</option>
            </select>
            <small className="form-hint">Estimate how full the bin is</small>
          </div>

          <div className="form-group">
            <label htmlFor="description" className="form-label">
              Description
            </label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              placeholder="Describe the waste issue in detail. For example: Overflowing bin, scattered waste, etc."
              className="form-control form-textarea"
              rows="5"
            />
            <small className="form-hint">Help us understand the issue better</small>
          </div>

          {/* Form Info Box */}
          {selectedShehia && formData.bin_id && (
            <div className="form-info">
              <h4>Report Summary</h4>
              <p><strong>Shehia:</strong> {selectedShehia.name}</p>
              <p><strong>Date/Time:</strong> {new Date(formData.timestamp).toLocaleString()}</p>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            className="btn btn-primary btn-submit"
            disabled={submitting}
          >
            {submitting ? 'Submitting...' : 'Submit Report'}
          </button>
        </form>

        {/* Instructions Box */}
        <aside className="instructions-box">
          <h3>How to Report</h3>
          <ol>
            <li>
              <strong>Select Your Location:</strong> Choose your Shehia and the 
              specific waste bin from the dropdown
            </li>
            <li>
              <strong>Set the Time:</strong> Select when you observed the issue
            </li>
            <li>
              <strong>Add Details:</strong> Describe the waste problem clearly 
              (optional but helpful)
            </li>
            <li>
              <strong>Submit:</strong> Click the Submit button to send your report
            </li>
          </ol>

          <div className="tips-section">
            <h4>Tips for Better Reports</h4>
            <ul>
              <li>Be specific about the location</li>
              <li>Include exact time when possible</li>
              <li>Describe what type of waste is overflowing</li>
              <li>Mention if it's a recurring issue</li>
            </ul>
          </div>
        </aside>
      </div>
    </div>
  );
}
