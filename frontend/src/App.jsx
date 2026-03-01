import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';

function App() {
  return (
    <Router>
      <div className="app-container">
        {/* Ide jöhet később a globális Navigációs Sáv (Navbar) komponens */}

        <Routes>
          {/* Főoldal útvonal beállítása */}
          <Route path="/" element={<Home />} />

          {/* További útvonalak helye (pl. /login, /dashboard) */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
