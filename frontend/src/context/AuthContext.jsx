import React, { createContext, useState, useEffect } from 'react';
import api from '../api/api';

// Ez a kontextus teszi elérhetővé az azonosítási (Auth) információkat a teljes alkalmazásban
export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // Alkalmazás indulásakor leellenőrizzük, hogy van-e már elmentett tokenünk
    useEffect(() => {
        const checkUserLoggedIn = () => {
            const token = localStorage.getItem('token');
            if (token) {
                // Ha van token, beállítjuk az alapértelmezett hitelesítési fejlécet minden jövőbeli Axios kéréshez
                api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
                setUser({ token: token });
            }
            setLoading(false);
        };

        checkUserLoggedIn();
    }, []);

    // Bejelentkezés esetén frissítjük a state-t és a localStorage-t
    const login = (token) => {
        localStorage.setItem('token', token);
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        setUser({ token: token });
    };

    // Kijelentkezés esetén mindent törlünk
    const logout = () => {
        localStorage.removeItem('token');
        delete api.defaults.headers.common['Authorization'];
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export default AuthProvider;
