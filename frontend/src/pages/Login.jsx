import { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api/api';
import { AuthContext } from '../context/AuthContext';
import './Register.css'; // Használjuk a már meglévő szép auth stílusokat

function Login() {
    const navigate = useNavigate();
    const { login } = useContext(AuthContext);
    const [formData, setFormData] = useState({
        email: '',
        password: ''
    });
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        setIsLoading(true);

        try {
            // OAuth2 token végpont a x-www-form-urlencoded formátumot várja
            const params = new URLSearchParams();
            params.append('username', formData.email);
            params.append('password', formData.password);

            const response = await api.post('/users/login', params, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            });

            // Sikeres belépés, elmentjük a tokent a contexten keresztül
            const token = response.data.access_token;
            login(token);

            setSuccess('Sikeres bejelentkezés! Betöltés...');

            // 1 másodperc múlva ugrás a kezdőlapra/védett oldalra
            setTimeout(() => {
                navigate('/dashboard');
            }, 1000);

        } catch (err) {
            console.error(err);
            if (err.response && err.response.status === 401) {
                setError('Helytelen email vagy jelszó!');
            } else if (err.response && err.response.data && err.response.data.detail) {
                setError(err.response.data.detail);
            } else {
                setError('Hiba a bejelentkezés során. Próbáld újra!');
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="container">
            <div className="auth-wrapper">
                <div className="auth-card">
                    <h2>Bejelentkezés</h2>
                    <p className="auth-subtitle">Jelentkezz be a BISEL fiókodba</p>

                    {error && <div className="alert alert-error">{error}</div>}
                    {success && <div className="alert alert-success">{success}</div>}

                    <form onSubmit={handleSubmit} className="auth-form">
                        <div className="form-group">
                            <label htmlFor="email">Email Cím</label>
                            <input
                                type="email"
                                id="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                placeholder="pelda@email.hu"
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="password">Jelszó</label>
                            <div className="password-input-wrapper">
                                <input
                                    type={showPassword ? "text" : "password"}
                                    id="password"
                                    name="password"
                                    value={formData.password}
                                    onChange={handleChange}
                                    placeholder="Add meg a jelszavad"
                                    required
                                />
                                <button
                                    type="button"
                                    className="password-toggle-btn"
                                    onClick={() => setShowPassword(!showPassword)}
                                >
                                    {showPassword ? "Rejtés" : "Mutat"}
                                </button>
                            </div>
                        </div>

                        <button type="submit" className="btn btn-primary auth-submit" disabled={isLoading}>
                            {isLoading ? 'Bejelentkezés folyamatban...' : 'Bejelentkezés'}
                        </button>
                    </form>

                    <p style={{ marginTop: '20px', textAlign: 'center' }}>
                        Nincs még fiókod? <Link to="/register">Regisztrálok az oldalra</Link>
                    </p>
                </div>
            </div>
        </div>
    );
}

export default Login;
