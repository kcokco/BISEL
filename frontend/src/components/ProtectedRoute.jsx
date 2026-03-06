import { Navigate, Outlet } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

function ProtectedRoute({ children }) {
    const { user, loading } = useContext(AuthContext);

    if (loading) {
        return <div style={{ textAlign: "center", padding: "50px" }}>Jogosultságok ellenőrzése...</div>;
    }

    if (!user) {
        // Ha nem vagyunk bejelentkezve, visszadobjuk a login oldalra
        return <Navigate to="/login" replace />;
    }

    return children ? children : <Outlet />;
}

export default ProtectedRoute;
