import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import Magazines from './components/magazines';
function App() {
    return (
        <Router>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/magazines" element={<Magazines />} />
            </Routes>
        </Router>
    );
}

export default App;
