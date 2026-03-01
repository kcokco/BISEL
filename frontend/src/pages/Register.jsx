import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/api';
import './Register.css';

function Register() {
    const navigate = useNavigate();
    // Űrlap adatainak tárolása
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        confirmPassword: ''
    });

    // Állapotok a visszajelzéshez
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);

    // Bemeneti mezők változásának kezelése
    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    // Űrlap elküldése
    const handleSubmit = async (e) => {
        e.preventDefault(); // Megakadályozzuk a böngésző újratöltését
        setError('');
        setSuccess('');

        // Jelszavak egyezésének ellenőrzése
        if (formData.password !== formData.confirmPassword) {
            setError('A két jelszó nem egyezik meg!');
            return;
        }

        setIsLoading(true);

        try {
            // API hívás a backend felé (a Pydantic UserCreate sémának megfelelően)
            const response = await api.post('/users/', {
                name: formData.name,
                email: formData.email,
                password: formData.password
            });

            // Sikeres ág
            setSuccess('Sikeres regisztráció! Visszairányítunk a kezdőlapra...');
            setFormData({ name: '', email: '', password: '', confirmPassword: '' });

            // 2 másodperc múlva ugrás a kezdőlapra
            setTimeout(() => navigate('/'), 2000);

        } catch (err) {
            console.error(err);
            if (err.response && err.response.data && err.response.data.detail) {
                // Ha a FastAPI valami konkrét értelmes hibát dob vissza (pl. "Email already exists")
                setError(err.response.data.detail);
            } else {
                setError('Hiba történt a regisztráció során. Kérjük, próbáld újra!');
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="container">
            <div className="auth-wrapper">
                <div className="auth-card">
                    <h2>Regisztráció</h2>
                    <p className="auth-subtitle">Hozd létre a BISEL fiókodat</p>

                    {/* Hiba és siker üzenetek megjelenítése */}
                    {error && <div className="alert alert-error">{error}</div>}
                    {success && <div className="alert alert-success">{success}</div>}

                    <form onSubmit={handleSubmit} className="auth-form">
                        <div className="form-group">
                            <label htmlFor="name">Teljes Név</label>
                            <input
                                type="text"
                                id="name"
                                name="name"
                                value={formData.name}
                                onChange={handleChange}
                                placeholder="Pl. Gipsz Jakab"
                                required
                            />
                        </div>

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
                                    placeholder="Legalább 8 karakter"
                                    required
                                    minLength="8"
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

                        <div className="form-group">
                            <label htmlFor="confirmPassword">Jelszó Megerősítése</label>
                            <div className="password-input-wrapper">
                                <input
                                    type={showPassword ? "text" : "password"}
                                    id="confirmPassword"
                                    name="confirmPassword"
                                    value={formData.confirmPassword}
                                    onChange={handleChange}
                                    placeholder="Jelszó újra"
                                    required
                                    minLength="8"
                                />
                            </div>
                        </div>

                        <button type="submit" className="btn btn-primary auth-submit" disabled={isLoading}>
                            {isLoading ? 'Feldolgozás...' : 'Regisztrálok'}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default Register;
