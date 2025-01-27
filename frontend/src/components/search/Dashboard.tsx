import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { searchData } from './SearchSlice'; 
import { useNavigate } from 'react-router-dom';
import { RootState } from '../../store/Store';


export default function Dashboard() {

    const [query, setQuery] = useState('');
    const [selectedStock, setSelectedStock] = useState('');
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const searchResults = useSelector((state: RootState) => state.search.searchDataPayload);

    const handleSearch = () => {
        if (!query.trim()) {
            alert('Please enter a search query.');
            return;
        }
        dispatch<any>(searchData(query))
    };
 
    const handleStockSelect = (symbol: string) => {
        console.log(symbol);
        setSelectedStock(symbol);
        navigate(`/search/${symbol}`, { state: { query, symbol } });
    };

    return (
        <section className="search-page p-3 p-md-5">
            <div className="pt-md-5 text-center">
                <h6 className="mb-4">
                    "The stock market is a device for transferring money from the impatient to the patient."
                    – Warren Buffett
                </h6>

                <div className="d-flex flex-column flex-md-row justify-content-center align-items-center search-sec mt-4">
                   
                    <div className="input-group mb-3 mb-md-0">
                        
                        <span className="input-group-text" id="basic-addon1">
                            <FontAwesomeIcon icon={faSearch} />
                        </span>

                        <input
                            type="text"
                            className="form-control p-3 me-md-3"
                            placeholder="Search stock by symbol or name"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            aria-label="Search"
                            aria-describedby="basic-addon1"
                        />
                    </div>
                    <button
                        className="search-btn mt-3 mt-md-0 px-4 py-3"
                        onClick={handleSearch}
                    >
                        Search
                    </button>
                </div>

                {searchResults && searchResults.length > 0 && (
                    <div className="search-results-container text-center">
                        <ul className="list-group search-page-result">
                            {searchResults.map((stock: any) => (
                                <li
                                    key={stock.symbol}
                                    className="list-group-item d-flex justify-content-between align-items-center"
                                    onClick={() => handleStockSelect(stock.symbol)}
                                    style={{ cursor: 'pointer' }}
                                >
                                    <span>{stock.name}</span>
                                    <span className="text-black">{stock.symbol}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>
        </section>

    );
}
