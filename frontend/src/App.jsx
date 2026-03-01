import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Register from './pages/Register';

function App() {
  return (
    <Router>
      <div className="app-container">
        {/* Globális Navigációs Sáv (Navbar) */}
        <Navbar />

        <Routes>
          {/* Főoldal útvonal beállítása */}
          <Route path="/" element={<Home />} />

          {/* Regisztrációs felület útvonala */}
          <Route path="/register" element={<Register />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
