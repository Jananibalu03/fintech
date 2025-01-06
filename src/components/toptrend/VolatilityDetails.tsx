import { useState } from "react";
import { Pagination } from "antd";
import "antd/dist/reset.css";
import volatilityData from "./volatility.json";

export default function VolatilityDetails() {
    const itemsPerPage = 10;
    const [currentPage, setCurrentPage] = useState(1);

    const startIndex = (currentPage - 1) * itemsPerPage;
    const currentItems = volatilityData.data.slice(startIndex, startIndex + itemsPerPage);

    const handlePageChange = (page: any) => {
        setCurrentPage(page);
    };

    return (
        <section>
            <div className='toptrend-sub-banner p-5'>
                <h3 className='ps-md-5'>{volatilityData.category}</h3>
                <p className='ps-md-5'>{volatilityData.description}</p>
            </div>

            <div className="container mt-4">
                {/* <h1 className="text-center mb-3">{volatilityData.category}</h1>
                <p className="text-center">{volatilityData.description}</p> */}
                <div className="table-responsive">
                    <table className="table table-bordered ">
                        <thead>
                            <tr>
                                <th>Stock Name</th>
                                <th>Symbol</th>
                                <th>Current Price ($)</th>
                                <th>Volatility (%)</th>
                                <th>Description</th>
                            </tr>
                        </thead>
                        <tbody>
                            {currentItems.map((stock, index) => (
                                <tr key={index}>
                                    <td>{stock.stockName}</td>
                                    <td>{stock.symbol}</td>
                                    <td>{stock.currentPrice.toFixed(2)}</td>
                                    <td>{stock.volatility}</td>
                                    <td>{stock.description}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <div className="d-flex justify-content-center m-3">
                    <Pagination
                        current={currentPage}
                        pageSize={itemsPerPage}
                        total={volatilityData.data.length}
                        onChange={handlePageChange}
                        showSizeChanger={false}
                    />
                </div>
            </div>
        </section>

    );
}
