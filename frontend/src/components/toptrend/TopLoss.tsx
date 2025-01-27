import { useState } from 'react';
import toploss from "./toploss.json";

export default function TopLoss() {
    const [searchTerm, setSearchTerm] = useState("");
    const [percentageChange, setPercentageChange] = useState("");
    const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });

    const headers = [
        { label: "Symbol", key: "symbol" },
        { label: "Stock Name", key: "stockName" },
        { label: "Current Price", key: "currentPrice" },
        { label: "Percentage Change", key: "percentageChange" },
        { label: "Sector", key: "sector" },
        { label: "Market Cap", key: "marketCap" },
        { label: "Description", key: "description" }
    ];

    const requestSort = (key: any) => {
        let direction = 'asc';
        if (sortConfig.key === key && sortConfig.direction === 'asc') {
            direction = 'desc';
        }
        setSortConfig({ key, direction });
    };

    const sortedStocks = [...toploss.stocks].sort((a: any, b: any) => {
        if (sortConfig.key) {
            const aValue = a[sortConfig.key];
            const bValue = b[sortConfig.key];
            if (typeof aValue === "number" && typeof bValue === "number") {
                return sortConfig.direction === 'asc' ? aValue - bValue : bValue - aValue;
            }
            return sortConfig.direction === 'asc'
                ? aValue.localeCompare(bValue)
                : bValue.localeCompare(aValue);
        }
        return 0;
    });

    const filteredStocks = sortedStocks.filter(stock => {
        const matchesSearch = stock.symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
            stock.stockName.toLowerCase().includes(searchTerm.toLowerCase());

        const matchesPercentageChange = percentageChange
            ? stock.percentageChange <= parseFloat(percentageChange)
            : true;

        return matchesSearch && matchesPercentageChange;
    });

    const getColor = (percentage: number) => {
        return percentage > 0 ? { color: 'green' } : { color: 'red' };
    };

    return (
        <section>

            <div className="d-flex toptrend-sub-banner p-5">
                <div className="container">
                    <div className="row d-flex justify-content-between">
                        <div className="col-md-8">
                            <h3>{toploss.category}</h3>
                            <p>{toploss.description}</p>
                        </div>

                        <div className="col-md-3 text-end my-4">
                            <input
                                type="text"
                                placeholder="Search stocks..."
                                className="form-control"
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
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
                                {headers.map((header) => (
                                    <th
                                        key={header.key}
                                        style={{ padding: '20px', whiteSpace: 'nowrap', cursor: "pointer" }}
                                        onClick={() => requestSort(header.key)}
                                    >
                                        {header.label}
                                        {sortConfig.key === header.key && (sortConfig.direction === 'asc' ? ' ▲' : ' ▼')}
                                    </th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {filteredStocks.length > 0 ? (
                                filteredStocks.map((stock) => (
                                    <tr key={stock.symbol}>
                                        <td style={{ padding: '12px', cursor: "pointer" }} className='table-active'>{stock.symbol}</td>
                                        <td>{stock.stockName}</td>
                                        <td>${stock.currentPrice.toFixed(2)}</td>

                                        <td style={{ ...getColor(stock.percentageChange) }}>
                                            {stock.percentageChange}%
                                        </td>
                                        <td>{stock.sector}</td>
                                        <td>{stock.marketCap}</td>
                                        <td>{stock.description}</td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan={headers.length} className="text-center">
                                        No data available
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </section>
    );
}
