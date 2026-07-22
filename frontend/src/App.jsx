import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import LandingPage from './components/LandingPage';
import About from './components/About';
import ReportForm from './components/ReportForm';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/about" element={<About />} />
            <Route path="/report" element={<ReportForm />} />
          </Routes>
        </main>
        <footer className="app-footer">
          <p>&copy; 2026 Community Waste Reporting System. All rights reserved.</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
