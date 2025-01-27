import { useState } from "react";
import topgain from "./topgain.json";

export default function TopGain() {
    const [searchTerm, setSearchTerm] = useState("");
    const [percentageChange, setPercentageChange] = useState("");
    const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });

    const requestSort = (key: any) => {
        let direction = 'asc';
        if (sortConfig.key === key && sortConfig.direction === 'asc') {
            direction = 'desc';
        }
        setSortConfig({ key, direction });
    };

    const compareValues = (a: any, b: any, key: string, direction: string) => {
        if (key === 'percentageChange' || key === 'currentPrice') {
            a = parseFloat(a);
            b = parseFloat(b);
        }

        if (a < b) {
            return direction === 'asc' ? -1 : 1;
        }
        if (a > b) {
            return direction === 'asc' ? 1 : -1;
        }
        return 0;
    };

    const sortedStocks = [...topgain.stocks].sort((a, b) => {
        if (sortConfig.key === null) return 0;
        return compareValues(a[sortConfig.key], b[sortConfig.key], sortConfig.key, sortConfig.direction);
    });

    const filteredStocks = sortedStocks.filter(stock => {
        const matchesSearch = stock.symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
            stock.stockName.toLowerCase().includes(searchTerm.toLowerCase());

        const matchesPercentageChange = percentageChange
            ? parseFloat(stock.percentageChange) >= parseFloat(percentageChange)
            : true;

        return matchesSearch && matchesPercentageChange;
    });

    const getPercentageHighlight = (percentage: number) => {
        return percentage >= 0 ? 'text-success' : 'text-danger';
    };

    return (
        <section>

            <div className="d-flex toptrend-sub-banner p-5">
                <div className="container">
                    <div className="row d-flex justify-content-between">
                        <div className="col-md-8">
                            <h3>{topgain.category}</h3>
                            <p>{topgain.description}</p>
                        </div>

                        <div className="col-md-3 text-end my-4">
                            <input
                                type="text"
                                placeholder="Search stocks..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                className="form-control"
                            />
                        </div>
                    </div>
                </div>
            </div>


            <div className="container mb-5">
                <div style={{ overflowX: "auto" }}>
                    <table className="table table-bordered mb-0">
                        <thead>
                            <tr>
                                {['symbol', 'stock Name', 'current Price', 'percentage Change', 'sector', 'marketCap', 'description'].map((key) => (
                                    <th
                                        key={key}
                                        style={{ padding: "20px", whiteSpace: "nowrap", cursor: "pointer" }}
                                        onClick={() => requestSort(key)}
                                    >
                                        {key.charAt(0).toUpperCase() + key.slice(1)}
                                        {sortConfig.key === key ? (sortConfig.direction === 'asc' ? ' ▲' : ' ▼') : ''}
                                    </th>
                                ))}
                            </tr>
                        </thead>

                        <tbody>
                            {filteredStocks.length > 0 ? (
                                filteredStocks.map((stock) => (
                                    <tr key={stock.symbol}>
                                        <td style={{ padding: '12px', cursor: "pointer" }} className="table-active">{stock.symbol}</td>
                                        <td style={{ padding: '20px', whiteSpace: 'nowrap' }}>{stock.stockName}</td>
                                        <td>${stock.currentPrice.toFixed(2)}</td>
                                        <td className={getPercentageHighlight(stock.percentageChange)}>
                                            {stock.percentageChange}%
                                        </td>
                                        <td>{stock.sector}</td>
                                        <td>{stock.marketCap}</td>
                                        <td>{stock.description}</td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan={7} className="text-center">No data available</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </section>
    );
}
