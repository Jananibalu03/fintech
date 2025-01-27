import { useState } from "react";
import stockData from "./undertendollar.json";

export default function UnderTendollar() {
    const [searchTerm, setSearchTerm] = useState("");
    const [sortConfig, setSortConfig] = useState({ key: null, direction: "asc" });

    const requestSort = (key: any) => {
        let direction = "asc";
        if (sortConfig.key === key && sortConfig.direction === "asc") {
            direction = "desc";
        }
        setSortConfig({ key, direction });
    };

    const compareValues = (a: any, b: any, key: string, direction: string) => {
        const aValue = a[key];
        const bValue = b[key];

        if (typeof aValue === "string" && typeof bValue === "string") {
            const aNormalized = aValue.trim().toLowerCase();
            const bNormalized = bValue.trim().toLowerCase();
            if (aNormalized < bNormalized) {
                return direction === "asc" ? -1 : 1;
            }
            if (aNormalized > bNormalized) {
                return direction === "asc" ? 1 : -1;
            }
        }

        if (typeof aValue === "number" && typeof bValue === "number") {
            return direction === "asc" ? aValue - bValue : bValue - aValue;
        }

        return 0;
    };

    const sortedStocks = [...stockData.stocks].sort((a, b) => {
        if (sortConfig.key) {
            return compareValues(a, b, sortConfig.key, sortConfig.direction);
        }
        return 0;
    });

    const filteredStocks = sortedStocks.filter((stock) =>
        stock.symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
        stock.stockName.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const columns = [
        { key: "symbol", label: "Symbol" },
        { key: "stockName", label: "Stock Name" },
        { key: "currentPrice", label: "Current Price" },
        { key: "sector", label: "Sector" },
        { key: "52WeekHigh", label: "52 Week High" },
        { key: "52WeekLow", label: "52 Week Low" },
        { key: "highPercentage", label: "High Percentage" },
        { key: "lowPercentage", label: "Low Percentage" },
        { key: "volume", label: "Volume" },
        { key: "marketCap", label: "Market Cap" },
        { key: "peRatio", label: "PE Ratio" },
        { key: "beta", label: "Beta" },
        { key: "dividendYield", label: "Dividend Yield" },
        { key: "earningsDate", label: "Earnings Date" },
        { key: "description", label: "Description" },
    ];

    return (
        <section>
            <div className="d-flex toptrend-sub-banner p-5">
                <div className="container">
                    <div className="row d-flex justify-content-between">
                        <div className="col-md-8">
                            <h3>{stockData.category}</h3>
                            <p>{stockData.description}</p>
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
                                {columns.map(({ key, label }) => (
                                    <th
                                        key={key}
                                        style={{ padding: "20px", whiteSpace: "nowrap", cursor: "pointer" }}
                                        onClick={() => requestSort(key)}
                                    >
                                        {label} {sortConfig.key === key && (sortConfig.direction === "asc" ? " ▲" : " ▼")}
                                    </th>
                                ))}
                            </tr>
                        </thead>

                        <tbody>
                            {filteredStocks.length > 0 ? (
                                filteredStocks.map((stock) => (
                                    <tr key={stock.symbol}>
                                        <td className="table-active">{stock.symbol}</td>
                                        <td style={{ padding: "20px", whiteSpace: "nowrap" }}>{stock.stockName}</td>
                                        <td>${stock.currentPrice.toFixed(2)}</td>
                                        <td>{stock.sector}</td>
                                        <td>${stock["52WeekHigh"].toFixed(2)}</td>
                                        <td>${stock["52WeekLow"].toFixed(2)}</td>
                                        <td style={{ color: stock.highPercentage > 0 ? "green" : "red" }}>
                                            {stock.highPercentage.toFixed(2)}%
                                        </td>
                                        <td style={{ color: stock.lowPercentage > 0 ? "green" : "red" }}>
                                            {stock.lowPercentage.toFixed(2)}%
                                        </td>
                                        <td>{stock.volume.toLocaleString()}</td>
                                        <td>{stock.marketCap}</td>
                                        <td>{stock.peRatio !== "N/A" ? stock.peRatio : "N/A"}</td>
                                        <td>{stock.beta}</td>
                                        <td>{stock.dividendYield}%</td>
                                        <td>{stock.earningsDate}</td>
                                        <td style={{ whiteSpace: "nowrap" }}>{stock.description}</td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan={8} className="text-center">
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
