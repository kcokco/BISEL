import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/api';
import '../pages/Register.css'; // Használjuk az auth-hoz készült szép CSS-t (auth-card stb.)

function NewReport() {
    const navigate = useNavigate();
    const today = new Date().toISOString().split('T')[0];

    const [formData, setFormData] = useState({
        watercourse_id: '',
        sampling_site_id: '',
        date: today, // Mai dátum alapértelmezetten
        quality_class: '',
        bisel_index: '',
        notes: ''
    });

    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [isLoading, setIsLoading] = useState(false);

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

        // Alapvető validáció
        if (!formData.watercourse_id || !formData.sampling_site_id || !formData.date) {
            setError('Minden csillaggal jelölt mező kitöltése kötelező!');
            setIsLoading(false);
            return;
        }

        try {
            // A pydantic schemas.ReportCreate sémának megfelelő objektum beküldése
            const response = await api.post('/reports/', {
                watercourse_id: formData.watercourse_id,
                sampling_site_id: formData.sampling_site_id,
                date: formData.date,
                quality_class: formData.quality_class || null,
                bisel_index: formData.bisel_index ? parseInt(formData.bisel_index) : null,
                notes: formData.notes || null,
            });

            setSuccess('Mérés sikeresen elmentve!');
            setFormData({
                watercourse_id: '',
                sampling_site_id: '',
                date: today,
                quality_class: '',
                bisel_index: '',
                notes: ''
            });

            // Sikeres beküldés után ugrás a dashboard-ra
            setTimeout(() => {
                navigate('/dashboard');
            }, 1500);

        } catch (err) {
            console.error(err);
            if (err.response && err.response.data && err.response.data.detail) {
                // Ha Pydantic validációs hiba van (pl. TypeMismatch) az tömbként is jöhet 
                const details = err.response.data.detail;
                if (Array.isArray(details)) {
                    setError('Kitöltési hiba: ' + details.map(d => d.msg).join(', '));
                } else {
                    setError(details);
                }
            } else {
                setError('Hiba történt a mérés mentésekor. Kérlek, próbáld újra!');
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="container">
            <div className="auth-wrapper">
                <div className="auth-card" style={{ maxWidth: '600px', width: '100%' }}>
                    <h2>Új Mérés Rögzítése</h2>
                    <p className="auth-subtitle">Add meg a terepi vizsgálat főbb adatait</p>

                    {error && <div className="alert alert-error">{error}</div>}
                    {success && <div className="alert alert-success">{success}</div>}

                    <form onSubmit={handleSubmit} className="auth-form">
                        <div className="form-group">
                            <label htmlFor="watercourse_id">Vízfolyás Neve / Azonosítója *</label>
                            <input
                                type="text"
                                id="watercourse_id"
                                name="watercourse_id"
                                value={formData.watercourse_id}
                                onChange={handleChange}
                                placeholder="Pl. Rákos-patak"
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="sampling_site_id">Mintavételi Helyszín *</label>
                            <input
                                type="text"
                                id="sampling_site_id"
                                name="sampling_site_id"
                                value={formData.sampling_site_id}
                                onChange={handleChange}
                                placeholder="Pl. Rákoscsaba híd"
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="date">Dátum *</label>
                            <input
                                type="date"
                                id="date"
                                name="date"
                                value={formData.date}
                                onChange={handleChange}
                                max={today}
                                required
                            />
                        </div>

                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                            <div className="form-group">
                                <label htmlFor="bisel_index">Számított BISEL Index</label>
                                <input
                                    type="number"
                                    id="bisel_index"
                                    name="bisel_index"
                                    value={formData.bisel_index}
                                    onChange={handleChange}
                                    placeholder="0 - 10"
                                    min="0"
                                    max="10"
                                />
                            </div>

                            <div className="form-group">
                                <label htmlFor="quality_class">Vízminőségi Osztály</label>
                                <input
                                    type="text"
                                    id="quality_class"
                                    name="quality_class"
                                    value={formData.quality_class}
                                    onChange={handleChange}
                                    placeholder="Pl. I. osztály"
                                />
                            </div>
                        </div>

                        <div className="form-group">
                            <label htmlFor="notes">Megjegyzések (opcionális)</label>
                            <textarea
                                id="notes"
                                name="notes"
                                value={formData.notes}
                                onChange={handleChange}
                                placeholder="Időjárás, furcsaságok, egyéb megfigyelések..."
                                style={{ width: '100%', padding: '0.8rem', border: '1px solid #d1d5db', borderRadius: '8px', minHeight: '100px', fontFamily: 'inherit' }}
                            />
                        </div>

                        <button type="submit" className="btn btn-primary auth-submit" disabled={isLoading} style={{ marginTop: '1rem' }}>
                            {isLoading ? 'Mentés folyamatban...' : 'Mérés Mentése'}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default NewReport;
