import { useState } from 'react';
import highdividend from './highdividend.json';
import { Pagination } from 'antd';


export default function HighDividend() {

    const [searchTerm, setSearchTerm] = useState('');
    const [sortConfig, setSortConfig] = useState({ key: null, direction: 'ascending' });
    const itemsPerPage = 10;
    const [currentPage, setCurrentPage] = useState(1);

    const handlePageChange = (page: number) => {
        setCurrentPage(page);
    };

    const headers = [
        { key: 'symbol', label: 'Symbol' },
        { key: 'stockName', label: 'Stock Name' },
        { key: 'currentPrice', label: 'Current Price' },
        { key: 'sector', label: 'Sector' },
        { key: 'dividendYield', label: 'Dividend Yield' },
        { key: 'peRatio', label: 'PE Ratio' },
        { key: 'marketCap', label: 'Market Cap' },
        { key: 'beta', label: 'Beta' },
        { key: 'dividendPayoutRatio', label: 'Dividend Payout Ratio' },
    ];

    const sortedStocks = [...highdividend.stocks].sort((a: any, b: any) => {
        if (!sortConfig.key) return 0;
        const aValue = a[sortConfig.key];
        const bValue = b[sortConfig.key];
        if (typeof aValue === 'string') {
            return sortConfig.direction === 'ascending'
                ? aValue.localeCompare(bValue)
                : bValue.localeCompare(aValue);
        }
        return sortConfig.direction === 'ascending' ? aValue - bValue : bValue - aValue;
    });

    const filteredStocks = sortedStocks.filter((stock) =>
        [stock.symbol, stock.stockName].some((value) =>
            value.toLowerCase().includes(searchTerm.toLowerCase())
        )
    );

    const handleSort = (key: any) => {
        setSortConfig((prevState) => ({
            key,
            direction: prevState.key === key && prevState.direction === 'ascending' ? 'descending' : 'ascending',
        }));
    };


    const startIndex = (currentPage - 1) * itemsPerPage;
    const currentPageStocks = filteredStocks.slice(startIndex, startIndex + itemsPerPage);

    return (
        <section>

            <div className="d-flex toptrend-sub-banner p-5">
                <div className="container">
                    <div className="row d-flex justify-content-between">
                        <div className="col-md-8">
                            <h3>{highdividend.category}</h3>
                            <p>{highdividend.description}</p>
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
                <div style={{ overflowX: 'auto' }}>
                    <table className="table table-bordered mb-0">
                        <thead>
                            <tr>
                                {headers.map((header) => (
                                    <th
                                        key={header.key}
                                        style={{ padding: '20px', whiteSpace: 'nowrap', cursor: 'pointer' }}
                                        onClick={() => handleSort(header.key)}
                                    >
                                        {header.label}{' '}
                                        {sortConfig.key === header.key &&
                                            (sortConfig.direction === 'ascending' ? '▲' : '▼')}
                                    </th>
                                ))}
                            </tr>
                        </thead>

                        <tbody>
                            {currentPageStocks.length > 0 ? (
                                currentPageStocks.map((stock) => (
                                    <tr key={stock.symbol}>
                                        <td style={{ padding: '12px', cursor: "pointer" }} className='table-active'>{stock.symbol}</td>
                                        <td style={{ padding: '20px', whiteSpace: 'nowrap' }}>{stock.stockName}</td>
                                        <td>${stock.currentPrice.toFixed(2)}</td>
                                        <td>{stock.sector}</td>
                                        <td>{stock.dividendYield}</td>
                                        <td>{stock.peRatio}</td>
                                        <td>{stock.marketCap}</td>
                                        <td>{stock.beta}</td>
                                        <td>{stock.dividendPayoutRatio}</td>
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

                <div className="d-flex justify-content-center m-3">
                    <Pagination
                        current={currentPage}
                        pageSize={itemsPerPage}
                        total={filteredStocks.length}
                        onChange={handlePageChange}
                        showSizeChanger={false}
                    />
                </div>
            </div>
        </section>
    );
}
