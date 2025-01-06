import { useState, useEffect } from 'react';
import { Pagination } from 'antd';
import highweeks from './highweek.json';

export default function HighWeeks52() {
    const itemsPerPage = 10;
    const [currentPage, setCurrentPage] = useState(1);
    const [cameFrom52WeekHighStocks, setCameFrom52WeekHighStocks] = useState(false);

    const highweeksData = highweeks.data;

    useEffect(() => {
        const referrer = document.referrer;
        if (referrer.includes('/52-week-high-stocks')) {
            console.log("eddddddddddddddddd");
            setCameFrom52WeekHighStocks(true);
        } else {
            setCameFrom52WeekHighStocks(false);
        }
    }, []); 

    const startIndex = (currentPage - 1) * itemsPerPage;
    const currentItems = highweeksData.slice(startIndex, startIndex + itemsPerPage);

    const handlePageChange = (page: number) => {
        setCurrentPage(page);
    };

    const getColor = (percentage: number) => {
        return percentage > 0 ? { color: 'green' } : { color: 'red' };
    };

    return (
        <section>
            <div className='toptrend-sub-banner p-5'>
                {cameFrom52WeekHighStocks ? (
                    <>
                        <h3 className='ps-md-5'>52 Weeks Low Stocks</h3>
                        <p className='ps-md-5'>List of stocks that have achieved their 52-week Low, including price changes in percentage, volume, and beta value.</p>
                    </>
                ) : (
                    <>
                        <h3 className='ps-md-5'>{highweeks.category}</h3>
                        <p className='ps-md-5'>{highweeks.description}</p>
                    </>
                )}
            </div>

            <div className='container'>
                <div style={{ overflowX: 'auto' }}>
                    <table className="table table-bordered mt-5 mb-md-0" style={{ borderCollapse: 'collapse' }}>
                        <thead>
                            <tr>
                                <th style={{ padding: '20px', whiteSpace: 'nowrap' }}>Stock Name</th>
                                <th style={{ padding: '20px', whiteSpace: 'nowrap' }}>Symbol</th>
                                <th style={{ padding: '20px', whiteSpace: 'nowrap' }}>Current Price</th>
                                <th style={{ padding: '20px', whiteSpace: 'nowrap' }}>52-Week High</th>
                                <th style={{ padding: '20px', whiteSpace: 'nowrap' }}>52-Week Low</th>
                                <th style={{ padding: '20px', whiteSpace: 'nowrap' }}>High Percentage</th>
                                <th style={{ padding: '20px', whiteSpace: 'nowrap' }}>Low Percentage</th>
                                <th style={{ padding: '20px', whiteSpace: 'nowrap' }}>Volume</th>
                                <th style={{ padding: '20px', whiteSpace: 'nowrap' }}>Beta</th>
                                <th style={{ padding: '20px', whiteSpace: 'nowrap' }}>High Date</th>
                                <th style={{ padding: '20px', whiteSpace: 'nowrap' }}>Low Date</th>
                                <th style={{ padding: '20px', whiteSpace: 'nowrap' }}>Description</th>
                            </tr>
                        </thead>
                        <tbody>
                            {currentItems.map((stock) => (
                                <tr key={stock.symbol}>
                                    <td style={{ padding: '12px' }}>{stock.stockName}</td>
                                    <td style={{ padding: '12px' }}>{stock.symbol}</td>
                                    <td style={{ padding: '12px' }}>{stock.currentPrice}</td>
                                    <td style={{ padding: '12px' }}>{stock.high52Weeks}</td>
                                    <td style={{ padding: '12px' }}>{stock.low52Weeks}</td>
                                    <td style={{ padding: '12px', ...getColor(stock.highPercentage) }}>
                                        {stock.highPercentage}%
                                    </td>
                                    <td style={{ padding: '12px', ...getColor(stock.lowPercentage) }}>
                                        {stock.lowPercentage}%
                                    </td>
                                    <td style={{ padding: '12px' }}>{stock.volume}</td>
                                    <td style={{ padding: '12px' }}>{stock.beta}</td>
                                    <td style={{ padding: '12px', whiteSpace: 'nowrap' }}>{stock.highDate}</td>
                                    <td style={{ padding: '12px', whiteSpace: 'nowrap' }}>{stock.lowDate}</td>
                                    <td style={{ padding: '12px', whiteSpace: 'nowrap' }}>{stock.description}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <div className="d-flex justify-content-center m-3">
                    <Pagination
                        current={currentPage}
                        pageSize={itemsPerPage}
                        total={highweeksData.length}
                        onChange={handlePageChange}
                        showSizeChanger={false}
                    />
                </div>
            </div>
        </section>
    );
}
