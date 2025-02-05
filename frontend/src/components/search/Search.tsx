import { useLocation } from 'react-router-dom';
import StockChart from './StockChart';

export default function Search() {

    const location = useLocation();
    const { query, symbol } = location.state || {};

    return (
        <section className="search-results">
            <div className="search-bg-section p-5">
                <h3 className="ps-md-5">Search Results for "{query.toUpperCase()}"</h3>
            </div>
            <div className="mt-4">
                <StockChart symbol={symbol} />
            </div>
        </section>
    );
}

