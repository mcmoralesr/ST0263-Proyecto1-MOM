import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate(); // Hook for navigation

    const handleRegister = async () => {
        try {
            const response = await fetch('http://54.156.65.242:5000/api/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('token', data.token);
                console.log('Token guardado:', data.token);
                setError('');
                alert('Registro exitoso');
                // You can redirect after successful registration if necessary
            } else {
                const errData = await response.json();
                setError(errData.error || 'Error en el registro');
            }
        } catch (err) {
            console.error('Error al conectar con la API:', err);
            setError('No se pudo conectar con el servidor');
        }
    };

    const handleLogin = async () => {
        try {
            const response = await fetch('http://54.156.65.242:5000/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('token', data.token);
                console.log('Token guardado:', data.token);
                setError('');
                alert('Inicio de sesión exitoso');
                // Redirect to the /revistas page upon successful login
                navigate('/revistas');
            } else {
                const errData = await response.json();
                setError(errData.error || 'Error en el inicio de sesión');
            }
        } catch (err) {
            console.error('Error al conectar con la API:', err);
            setError('No se pudo conectar con el servidor');
        }
    };

    return (
        <div className="card shadow-lg p-4 w-100" style={{ maxWidth: '400px' }}>
            <h2 className="text-center text-lg mb-4">Inicio de Sesión</h2>

            <div className="mb-3">
                <label className="form-label text-secondary">Usuario</label>
                <input
                    type="text"
                    className="form-control"
                    placeholder="Ingresa tu usuario"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
            </div>

            <div className="mb-3">
                <label className="form-label text-secondary">Contraseña</label>
                <input
                    type="password"
                    className="form-control"
                    placeholder="Ingresa tu contraseña"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
            </div>

            {error && <div className="alert alert-danger">{error}</div>}
            <div className="mb-3">
                <button className="btn btn-primary w-100 mb-2" onClick={handleRegister}>
                    Registrar
                </button>

                <button className="btn btn-primary w-100" onClick={handleLogin}>
                    Login
                </button>
            </div>
        </div>
    );
}

export default Login;
