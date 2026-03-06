import { Link, useNavigate } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import './Navbar.css';

function Navbar() {
    const { user, logout } = useContext(AuthContext);
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/'); // Kijelentkezés után a kezdőlapra
    };

    return (
        <nav className="navbar">
            <div className="navbar-container">
                {/* Bal oldal: Logó / Főcím */}
                <Link to="/" className="navbar-logo">
                    <span className="logo-icon">💧</span> BISEL <span className="logo-subtitle">Rendszer</span>
                </Link>

                {/* Jobb oldal: Menüpontok */}
                <div className="navbar-menu">
                    <Link to="/" className="nav-item">Kezdőlap</Link>
                    {user ? (
                        <>
                            <Link to="/dashboard" className="nav-item">Kezelőpult</Link>
                            <div className="nav-actions">
                                <Link to="/new-report" className="btn btn-primary" style={{ marginRight: '1rem' }}>
                                    + Új Mérés
                                </Link>
                                <button onClick={handleLogout} className="btn btn-outline" style={{ padding: '0.5rem 1rem', cursor: 'pointer', fontFamily: 'inherit', fontSize: '0.9rem', backgroundColor: 'transparent' }}>
                                    Kijelentkezés
                                </button>
                            </div>
                        </>
                    ) : (
                        <div className="nav-actions">
                            <Link to="/login" className="btn btn-outline">Belépés</Link>
                            <Link to="/register" className="btn btn-primary">Regisztráció</Link>
                        </div>
                    )}
                </div>
            </div>
        </nav>
    );
}

export default Navbar;
