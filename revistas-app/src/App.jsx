import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import Magazines from './components/Magazines';
function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/revistass" element={<Magazines />} />
            </Routes>
        </Router>
    );
}

export default App;
