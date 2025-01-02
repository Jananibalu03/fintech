import { useLocation, useParams } from 'react-router-dom';
import StockGraph from './StockGraph';
import { useSelector } from 'react-redux';
import { RootState } from '../../store/Store';

export default function Search() {

    // const { symbol } = useParams<{ symbol: string }>();


    const location = useLocation();
    const { query, symbol } = location.state || {};
    const { loading, error } = useSelector(
        (state: RootState) => state.search
    );

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <section className="search-results">
            <div className="search-bg-section p-5">
                <h3 className="ps-md-5">Search Results for "{query}"</h3>
            </div>
            <div className="mt-4">
                <StockGraph symbol={symbol} />
            </div>
        </section>
    );
}
