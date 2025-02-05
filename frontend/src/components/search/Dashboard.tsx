import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { searchData } from './SearchSlice';
import { useNavigate } from 'react-router-dom';
import { RootState } from '../../store/Store';


export default function Dashboard() {

    const [query, setQuery] = useState('');
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const searchResults = useSelector((state: RootState) => state.search.searchDataPayload);

    useEffect(() => {
        if (query.length > 1) {
            dispatch<any>(searchData(query));
        }
    }, [query]);

    const handleStockSelect = (symbol: string) => {
        setQuery('');
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
                        <span className="input-group-text">
                            <FontAwesomeIcon icon={faSearch} />
                        </span>
                        <input
                            type="text"
                            className="form-control p-3 "
                            placeholder="Search stock by symbol or name"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                        />
                    </div>
                </div>

                {searchResults?.length > 0 && query.length > 1 && (
                    <ul className="list-group search-page-result">
                        {searchResults.map((stock: any) => (
                            <li
                                key={stock.Symbol}
                                className="list-group-item d-flex justify-content-between align-items-center"
                                onClick={() => handleStockSelect(stock.Symbol)}
                                style={{ cursor: 'pointer' }}
                            >
                                <span className="text-black">{stock.Symbol}</span>
                                <span>{stock.Name}</span>
                            </li>
                        ))}
                    </ul>
                )}

            </div>
        </section>
    );
}
