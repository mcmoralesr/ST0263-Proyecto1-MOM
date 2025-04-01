import { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = () => {
        console.log('Usuario:', username, 'Contraseña:', password);
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
                
                <button className="btn btn-primary w-100" onClick={handleLogin}>Ingresar</button>
                

            </div>
    );
}

export default Login;
