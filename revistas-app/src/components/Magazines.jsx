import { useEffect, useRef, useState } from "react";

function Magazines({ sendMagazineArray }) {
    const [selectedMagazines, setSelectedMagazines] = useState([]);
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const [magazineName, setMagazineName] = useState("");
    const [mensajesTopico, setMensajesTopico] = useState([]);
    const dropdownRef = useRef(null);

    const [magazines, setMagazines] = useState([]);
    const [misTopicos, setMisTopicos] = useState([]);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setDropdownOpen(false);
            }
        };
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    const fetchMagazines = async () => {
        if (magazines.length > 0) return;

        try {
            const token = localStorage.getItem("token");
            const response = await fetch("http://54.156.65.242:5000//api/topicos", {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error("Error al obtener las revistas");
            }

            const data = await response.json();
            setMagazines(data.topicos);
        } catch (error) {
            console.error("Error al cargar revistas:", error);
        }
    };

    const fetchMisTopicos = async () => {
        if (misTopicos.length > 0) return;

        try {
            const token = localStorage.getItem("token");
            const response = await fetch("http://54.156.65.242:5000//api/mis-topicos", {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error("Error al obtener mis tópicos");
            }

            const data = await response.json();
            setMisTopicos(data.topicos); // Asegúrate que la respuesta tenga 'topicos'
        } catch (error) {
            console.error("Error al cargar mis tópicos:", error);
        }
    };

    const toggleDropdown = async () => {
        setDropdownOpen(!dropdownOpen);
        if (magazines.length === 0) {
            await fetchMagazines();
        }
    };

    const handleSelectMagazine = (magazine) => {
        setSelectedMagazines((prev) =>
            prev.includes(magazine) ? prev.filter((m) => m !== magazine) : [...prev, magazine]
        );
    };

    const handleSendToBackend = async () => {
        const token = localStorage.getItem("token");
    
        try {
            // Enviar un POST por cada revista
            const responses = await Promise.all(
                selectedMagazines.map(async (magazine) => {
                    const response = await fetch(`http://54.156.65.242:5000/api/topicos/${encodeURIComponent(magazine)}/suscribir`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "Authorization": `Bearer ${token}`
                        }
                    });
    
                    if (!response.ok) {
                        const error = await response.json();
                        throw new Error(error.error || `Error al suscribirse a '${magazine}'`);
                    }
    
                    return response.json();
                })
            );
    
            alert("Revistas añadidas correctamente");
            setSelectedMagazines([]);
            setDropdownOpen(false);
        } catch (err) {
            console.error("Error al enviar revistas:", err);
            alert(err.message || "Error al enviar revistas");
        }
    };
    

    const sendSingleMagazine = async (nombreTopico) => {
        if (!nombreTopico) {
            alert("Selecciona una revista");
            return;
        }

        try {
            const token = localStorage.getItem("token");

            const response = await fetch(`http://54.156.65.242:5000//api/topicos/${nombreTopico}/mensajes`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.status === 200) {
                const data = await response.json();
                setMensajesTopico(data.mensajes);
            } else if (response.status === 404) {
                alert("Tópico no encontrado");
            } else {
                alert("Error al obtener la revista");
            }
        } catch (error) {
            console.error("Error en la petición:", error);
        }
    };

    return (
        <div className="container py-5 max-w-md mx-auto">
            <div className="card shadow-lg rounded-lg p-4">
                <h2 className="text-center mb-4 text-lg font-bold">Selector de Revistas</h2>

                {/* Selector múltiple */}
                <div className="relative" ref={dropdownRef}>
                    <div
                        className="border rounded-lg p-2 cursor-pointer flex flex-wrap gap-1 bg-white"
                        onClick={toggleDropdown}
                    >
                        {selectedMagazines.length === 0 ? (
                            <span className="text-gray-400">Selecciona revistas...</span>
                        ) : (
                            selectedMagazines.map((mag, index) => (
                                <span key={index} className="bg-blue-200 text-blue-700 px-2 py-1 rounded-md text-sm">
                                    {mag}
                                </span>
                            ))
                        )}
                    </div>

                    {dropdownOpen && (
                        <div className="selector-container bg-white border rounded-lg overflow-y-auto shadow-md z-10">
                            {magazines.map((mag, index) => (
                                <div
                                    key={index}
                                    onClick={() => handleSelectMagazine(mag)}
                                    className={`p-2 cursor-pointer flex items-center hover:bg-gray-200 ${selectedMagazines.includes(mag) ? "bg-blue-100" : ""}`}
                                >
                                    <input
                                        type="checkbox"
                                        checked={selectedMagazines.includes(mag)}
                                        className="input-box"
                                        readOnly
                                    />
                                    {mag}
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                <button 
                    className="btn btn-primary w-full mt-4 bg-blue-400 text-white p-2 rounded-md"
                    onClick={handleSendToBackend}
                >
                    Añadir
                </button>

                {/* Selector de una sola revista */}
                <div className="mt-4">
                    <label className="form-label">Selecciona una revista:</label>
                    <select
                        className="form-select w-full p-2 border rounded-lg mt-2"
                        onClick={fetchMisTopicos}
                        onChange={(e) => setMagazineName(e.target.value)}
                    >
                        <option value="">Seleccione una revista</option>
                        {misTopicos.map((mag, index) => (
                            <option key={index} value={mag}>{mag}</option>
                        ))}
                    </select>
                </div>

                <button
                    className="btn btn-success w-full mt-4 bg-green-500 text-white p-2 rounded-md"
                    onClick={() => sendSingleMagazine(magazineName)}
                >
                    Ver Revista
                </button>

                {/* Mostrar mensajes de la revista seleccionada */}
                {mensajesTopico.length > 0 && (
                    <div className="mt-6">
                        <h2 className="text-xl font-semibold mb-2">Mensajes de la revista:</h2>
                        <ul className="space-y-2">
                            {mensajesTopico.map((msg) => (
                                <li key={msg.id} className="border p-3 rounded-md shadow-sm">
                                    <p><strong>Emisor:</strong> {msg.emisor}</p>
                                    <p><strong>Contenido:</strong> {msg.contenido}</p>
                                    <p className="text-sm text-gray-500"><strong>Fecha:</strong> {new Date(msg.timestamp).toLocaleString()}</p>
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Magazines;
