import { useState, useEffect } from 'react';
import { Pagination } from 'antd';
import highweeks from './highweek.json';

export default function HighWeeks52() {
    const itemsPerPage = 10;
    const [currentPage, setCurrentPage] = useState(1);
    const [cameFrom52WeekHighStocks, setCameFrom52WeekHighStocks] = useState(false);
    const [filteredData, setFilteredData] = useState([...highweeks.data]);
    const [sortConfig, setSortConfig] = useState({ key: '', direction: 'asc' });
    const [searchTerm, setSearchTerm] = useState("");

    const columnHeaders = [
        { displayName: 'Symbol', dataKey: 'symbol' },
        { displayName: 'Stock Name', dataKey: 'stockName' },
        { displayName: 'Current Price', dataKey: 'currentPrice' },
        { displayName: '52 Weeks high', dataKey: 'high52Weeks' },
        { displayName: '52 Weeks low', dataKey: 'low52Weeks' },
        { displayName: 'High in %', dataKey: 'highPercentage' },
        { displayName: 'Low in %', dataKey: 'lowPercentage' },
        { displayName: 'Volume', dataKey: 'volume' },
        { displayName: 'Beta', dataKey: 'beta' },
        { displayName: 'High Date', dataKey: 'highDate' },
        { displayName: 'Low Date', dataKey: 'lowDate' },
        { displayName: 'Description', dataKey: 'description' }
    ];

    useEffect(() => {
        const referrer = document.referrer;
        if (referrer.includes('/52-week-high-stocks')) {
            setCameFrom52WeekHighStocks(true);
        } else {
            setCameFrom52WeekHighStocks(false);
        }
    }, []);

    useEffect(() => {
        const filtered = highweeks.data.filter((stock) => {
            return (
                stock.symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
                stock.stockName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                stock.description.toLowerCase().includes(searchTerm.toLowerCase())
            );
        });
        setFilteredData(filtered);
        setCurrentPage(1);
    }, [searchTerm]);

    const handleSort = (key: string) => {
        let direction = 'asc';
        if (sortConfig.key === key && sortConfig.direction === 'asc') {
            direction = 'desc';
        }
        setSortConfig({ key, direction });
        sortData(key, direction);
    };

    const sortData = (key: string, direction: string) => {
        const sortedData = [...filteredData].sort((a: any, b: any) => {
            if (typeof a[key] === 'number' && typeof b[key] === 'number') {
                return direction === 'asc' ? a[key] - b[key] : b[key] - a[key];
            }
            if (typeof a[key] === 'string' && typeof b[key] === 'string') {
                return direction === 'asc' ? a[key].localeCompare(b[key]) : b[key].localeCompare(a[key]);
            }
            return 0;
        });
        setFilteredData(sortedData);
    };

    const startIndex = (currentPage - 1) * itemsPerPage;
    const currentItems = filteredData.slice(startIndex, startIndex + itemsPerPage);

    const handlePageChange = (page: number) => {
        setCurrentPage(page);
    };

    const getHighlightColor = (currentPrice: number, value: number, isHigh: boolean) => {
        if (isHigh) {
            return currentPrice < value ? "text-success" : "";
        }
        return currentPrice > value ? "text-danger" : "";
    };

    const getColor = (percentage: number) => {
        return percentage > 0 ? { color: 'green' } : { color: 'red' };
    };

    const getSortIcon = (column: string) => {
        if (sortConfig.key === column) {
            return sortConfig.direction === 'asc' ? ' ▲' : ' ▼';
        }
        return '';
    };

    return (
        <section>
            <div className="d-flex toptrend-sub-banner p-5">
                <div className="container">
                    <div className="row d-flex justify-content-between">
                        <div className="col-md-8">
                            {cameFrom52WeekHighStocks ? (
                                <>
                                    <h3>52 Weeks Low Stocks</h3>
                                    <p>List of stocks that have achieved their 52-week Low, including price changes in percentage, volume, and beta value.</p>
                                </>
                            ) : (
                                <>
                                    <h3>{highweeks.category}</h3>
                                    <p>{highweeks.description}</p>
                                </>
                            )}
                        </div>

                        <div className="col-md-3 text-end my-4">
                            <input
                                type="text"
                                placeholder="Search stocks..."
                                className="form-control"
                                onChange={(e) => setSearchTerm(e.target.value)}
                                value={searchTerm}
                            />
                        </div>
                    </div>
                </div>
            </div>

            <div className='container mb-5'>
                <div style={{ overflowX: 'auto' }}>
                    <table className="table table-bordered table-hover mb-md-0" style={{ borderCollapse: 'collapse' }}>
                        <thead>
                            <tr>
                                {columnHeaders.map(({ displayName, dataKey }) => (
                                    <th
                                        key={dataKey}
                                        style={{ padding: '20px', whiteSpace: 'nowrap', cursor: 'pointer' }}
                                        onClick={() => handleSort(dataKey)}
                                    >
                                        {displayName} {getSortIcon(dataKey)}
                                    </th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {currentItems.length > 0 ? (
                                currentItems.map((stock) => (
                                    <tr key={stock.symbol}>
                                        <td style={{ padding: '12px', cursor: "pointer" }} className='table-active'>{stock.symbol}</td>
                                        <td style={{ padding: '12px' }}>{stock.stockName}</td>
                                        <td style={{ padding: '12px' }}>${stock.currentPrice.toFixed(2)}</td>
                                        <td className={getHighlightColor(stock.currentPrice, stock.high52Weeks, true)}>
                                            ${stock.high52Weeks.toFixed(2)}
                                        </td>
                                        <td className={getHighlightColor(stock.currentPrice, stock.low52Weeks, false)}>
                                            ${stock.low52Weeks.toFixed(2)}
                                        </td>
                                        <td style={{ padding: '12px', ...getColor(stock.highPercentage) }} >
                                            {stock.highPercentage.toFixed(2)}%
                                        </td>
                                        <td style={{ padding: '12px', ...getColor(stock.lowPercentage) }} >
                                            {stock.lowPercentage.toFixed(2)}%
                                        </td>
                                        <td style={{ padding: '12px' }}>{stock.volume.toLocaleString()}</td>
                                        <td style={{ padding: '12px' }}>{stock.beta}</td>
                                        <td style={{ padding: '12px', whiteSpace: 'nowrap' }}>{stock.highDate}</td>
                                        <td style={{ padding: '12px', whiteSpace: 'nowrap' }}>{stock.lowDate}</td>
                                        <td style={{ padding: '12px', whiteSpace: 'nowrap' }}>{stock.description}</td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan={12} style={{ textAlign: 'center' }}>No data available</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>

                <div className="d-flex justify-content-center m-3">
                    <Pagination
                        current={currentPage}
                        pageSize={itemsPerPage}
                        total={filteredData.length}
                        onChange={handlePageChange}
                        showSizeChanger={false}
                    />
                </div>
            </div>
        </section>
    );
}
