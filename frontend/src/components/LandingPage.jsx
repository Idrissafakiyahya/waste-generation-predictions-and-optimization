import { useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import img1 from '../assets/hero.png';
import './LandingPage.css';

export default function LandingPage() {
  const navigate = useNavigate();
  const images = [img1, img1, img1, img1];
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setIndex((i) => (i + 1) % images.length);
    }, 6000);
    return () => clearInterval(timer);
  }, [images.length]);

  return (
    <div className="landing-page">
      {/* Hero Section with background slider */}
      <section className="hero">
        <div className="slider">
          {images.map((src, i) => (
            <div
              key={i}
              className={`slide ${i === index ? 'active' : ''}`}
              style={{ backgroundImage: `url(${src})` }}
            />
          ))}
          <div className="slider-overlay" />
        </div>

        <div className="hero-content">
          <div className="hero-icon">♻️</div>
          <h1>Community Waste Reporting System</h1>
          <p className="hero-subtitle">
            Help keep our community clean by reporting waste issues in your area.
          </p>
          <button 
            className="btn btn-primary btn-large hero-cta"
            onClick={() => navigate('/report')}
          >
            Report Waste Now
          </button>
        </div>
      </section>

      {/* Features Section */}
      <section className="features">
        <h3>How It Works</h3>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">📍</div>
            <h4>Select Your Location</h4>
            <p>Choose your Shehia and the specific waste bin location</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">⏰</div>
            <h4>Report Issues</h4>
            <p>Timestamp your waste management concerns</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">💬</div>
            <h4>Add Details</h4>
            <p>Include comments to help our team understand the issue</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">✅</div>
            <h4>Track Impact</h4>
            <p>Your report helps improve waste management in our community</p>
          </div>
        </div>
      </section>

      {/* Call to Action Section */}
      <section className="cta-section">
        <div className="cta-content">
          <h3>Ready to Make a Difference?</h3>
          <p>
            Every report matters. Help us build a cleaner, healthier community 
            by reporting waste issues in your neighborhood today.
          </p>
          <button 
            className="btn btn-success btn-large"
            onClick={() => navigate('/report')}
          >
            Start Reporting
          </button>
        </div>
      </section>

      {/* Info Section */}
      <section className="info">
        <div className="info-box">
          <h4>About This System</h4>
          <p>
            This Community Waste Reporting System is designed to help identify 
            and address waste management issues in your area. Your reports 
            contribute valuable data for improving our community's cleanliness 
            and environmental health.
          </p>
          <button 
            className="btn btn-secondary"
            onClick={() => navigate('/about')}
          >
            Learn More
          </button>
        </div>
      </section>
    </div>
  );
}
