import { Link, useLocation } from 'react-router-dom';
import './Header.css';

export default function Header() {
  const location = useLocation();

  return (
    <header className="header">
      <div className="header-container">
        <div className="logo-section">
          <div className="logo-circle">♻️</div>
          <h1 className="app-title">Waste Reporting System</h1>
        </div>
        <nav className="nav">
          <Link 
            to="/" 
            className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
          >
            Home
          </Link>
          <Link 
            to="/report" 
            className={`nav-link ${location.pathname === '/report' ? 'active' : ''}`}
          >
            Report Waste
          </Link>
          <Link 
            to="/about" 
            className={`nav-link ${location.pathname === '/about' ? 'active' : ''}`}
          >
            About
          </Link>
        </nav>
      </div>
    </header>
  );
}
