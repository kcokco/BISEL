import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Register from './pages/Register';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import NewReport from './pages/NewReport';
import ProtectedRoute from './components/ProtectedRoute';

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

          {/* Bejelentkezési felület útvonala */}
          <Route path="/login" element={<Login />} />

          {/* Védett Kezelőpult (Dashboard) */}
          <Route path="/dashboard" element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } />

          {/* Védett Új Mérés Rögzítése (NewReport) */}
          <Route path="/new-report" element={
            <ProtectedRoute>
              <NewReport />
            </ProtectedRoute>
          } />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
