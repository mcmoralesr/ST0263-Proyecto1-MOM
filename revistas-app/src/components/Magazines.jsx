import { useState, useEffect, useRef } from "react";

function Magazines({ sendMagazineArray, sendSingleMagazine }) {
    const [selectedMagazines, setSelectedMagazines] = useState([]);
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const [magazineName, setMagazineName] = useState("");
    const dropdownRef = useRef(null);

    const magazines = [
        "Revista A", "Revista B", "Revista C", "Revista D",
        "Revista E", "Revista F", "Revista G", "Revista H"
    ];

    // Manejar clic fuera del dropdown para cerrarlo
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setDropdownOpen(false);
            }
        };
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    const toggleDropdown = () => setDropdownOpen(!dropdownOpen);

    const handleSelectMagazine = (magazine) => {
        setSelectedMagazines((prev) =>
            prev.includes(magazine) ? prev.filter((m) => m !== magazine) : [...prev, magazine]
        );
    };

    return (
        <div className="container py-5 max-w-md mx-auto">
            <div className="card shadow-lg rounded-lg p-4">
                <h2 className="text-center mb-4 text-lg font-bold">Selector de Revistas</h2>

                {/* Input tipo selector */}
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
                                className={`p-2 cursor-pointer flex items-center hover:bg-gray-200 ${
                                    selectedMagazines.includes(mag) ? "bg-blue-100" : ""
                                }`}
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
                    onClick={() => sendMagazineArray(selectedMagazines)}
                >
                    Añadir
                </button>

                {/* Selector de una sola revista */}
                <div className="mt-4">
                    <label className="form-label">Selecciona una revista:</label>
                    <select
                        className="form-select w-full p-2 border rounded-lg mt-2"
                        onChange={(e) => setMagazineName(e.target.value)}
                    >
                        <option value="">Seleccione una revista</option>
                        {magazines.map((mag, index) => (
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
            </div>
        </div>
    );
}

export default Magazines;
