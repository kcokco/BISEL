import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
    return (
        <nav className="navbar">
            <div className="navbar-container">
                {/* Bal oldal: Logó / Főcím */}
                <Link to="/" className="navbar-logo">
                    <span className="logo-icon">💧</span> BISEL <span className="logo-subtitle">Rendszer</span>
                </Link>

                {/* Jobb oldal: Menüpontok */}
                <div className="navbar-menu">
                    {/* Ide jönnek majd a tényleges funkció gombok, most csak demó/előkészület */}
                    <Link to="/" className="nav-item">Kezdőlap</Link>
                    <div className="nav-actions">
                        <Link to="/login" className="btn btn-outline">Belépés</Link>
                        <Link to="/register" className="btn btn-primary">Regisztráció</Link>
                    </div>
                </div>
            </div>
        </nav>
    );
}

export default Navbar;
