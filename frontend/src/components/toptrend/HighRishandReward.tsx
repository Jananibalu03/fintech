import React from 'react'

export default function HighRishandReward() {
  return (
    <div>HighRishandReward</div>
  )
}


// import { useState, useMemo } from "react";
// import highrishandreward from "./highriskandreward.json";
// import { Pagination } from "antd";

// export default function HighRishandReward() {
//     const [searchTerm, setSearchTerm] = useState("");
//     const [sortConfig, setSortConfig] = useState({ key: null, direction: "asc" });

//     const itemsPerPage = 10;
//     const [currentPage, setCurrentPage] = useState(1);

//     const handlePageChange = (page: number) => {
//         setCurrentPage(page);
//     };

//     const getHighlightColor = (currentPrice: any, value: any, isHigh: any) => {
//         if (isHigh) {
//             return currentPrice < value ? "text-success" : "";
//         }
//         return currentPrice > value ? "text-danger" : "";
//     };

//     const getPercentageHighlight = (percentage: any) => {
//         return percentage >= 0 ? "text-success" : "text-danger";
//     };

//     const headers = [
//         { key: "symbol", label: "Symbol" },
//         { key: "stockName", label: "Stock Name" },
//         { key: "currentPrice", label: "Current Price" },
//         { key: "sector", label: "Sector" },
//         { key: "52WeekHigh", label: "52 Week High" },
//         { key: "52WeekLow", label: "52 Week Low" },
//         { key: "highPercentage", label: "High Percentage" },
//         { key: "lowPercentage", label: "Low Percentage" },
//         { key: "volume", label: "Volume" },
//         { key: "marketCap", label: "Market Cap" },
//         { key: "peRatio", label: "P/E Ratio" },
//         { key: "beta", label: "Beta" },
//         { key: "dividendYield", label: "Dividend Yield" },
//     ];

//     const filteredStocks = useMemo(() => {
//         return highrishandreward.stocks.filter(
//             (stock) =>
//                 stock.symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
//                 stock.stockName.toLowerCase().includes(searchTerm.toLowerCase())
//         );
//     }, [searchTerm]);

//     const sortedStocks = useMemo(() => {
//         const sorted = [...filteredStocks].sort((a, b) => {
//             if (!sortConfig.key) return 0;

//             const aValue = a[sortConfig.key];
//             const bValue = b[sortConfig.key];

//             if (aValue < bValue) {
//                 return sortConfig.direction === "asc" ? -1 : 1;
//             }
//             if (aValue > bValue) {
//                 return sortConfig.direction === "asc" ? 1 : -1;
//             }
//             return 0;
//         });
//         return sorted;
//     }, [filteredStocks, sortConfig]);

//     const handleSort = (key: any) => {
//         setSortConfig((prevConfig) => {
//             if (prevConfig.key === key) {
//                 return { key, direction: prevConfig.direction === "asc" ? "desc" : "asc" };
//             }
//             return { key, direction: "asc" };
//         });
//     };

//     const startIndex = (currentPage - 1) * itemsPerPage;
//     const currentPageStocks = sortedStocks.slice(startIndex, startIndex + itemsPerPage);

//     return (
//         <section>

//             <div className="d-flex toptrend-sub-banner p-5">
//                 <div className="container">
//                     <div className="row d-flex justify-content-between">
//                         <div className="col-md-8">
//                             <h3>{highrishandreward.category}</h3>
//                             <p>{highrishandreward.description}</p>
//                         </div>

//                         <div className="col-md-3 text-end my-4">
//                             <input
//                                 type="text"
//                                 placeholder="Search stocks..."
//                                 className="form-control"
//                                 value={searchTerm}
//                                 onChange={(e) => setSearchTerm(e.target.value)}
//                             />
//                         </div>
//                     </div>
//                 </div>
//             </div>

//             <div className="container mb-5">
//                 <div style={{ overflowX: "auto" }}>
//                     <table className="table table-bordered mb-0">
//                         <thead>
//                             <tr>
//                                 {headers.map((header) => (
//                                     <th
//                                         key={header.key}
//                                         style={{ padding: "20px", whiteSpace: "nowrap", cursor: "pointer" }}
//                                         onClick={() => handleSort(header.key)}
//                                     >
//                                         {header.label}{" "}
//                                         {sortConfig.key === header.key &&
//                                             (sortConfig.direction === "asc" ? ' ▲' : ' ▼')}
//                                     </th>
//                                 ))}
//                             </tr>
//                         </thead>
//                         <tbody>
//                             {currentPageStocks.length > 0 ? (
//                                 currentPageStocks.map((stock) => (
//                                     <tr key={stock.symbol}>
//                                         <td className="table-active">{stock.symbol}</td>
//                                         <td style={{ padding: "20px", whiteSpace: "nowrap" }}>{stock.stockName}</td>
//                                         <td>${stock.currentPrice.toFixed(2)}</td>
//                                         <td>{stock.sector}</td>
//                                         <td className={getHighlightColor(stock.currentPrice, stock["52WeekHigh"], true)}>
//                                             ${stock["52WeekHigh"].toFixed(2)}
//                                         </td>
//                                         <td className={getHighlightColor(stock.currentPrice, stock["52WeekLow"], false)}>
//                                             ${stock["52WeekLow"].toFixed(2)}
//                                         </td>
//                                         <td className={getPercentageHighlight(stock.highPercentage)}>
//                                             {stock.highPercentage}%
//                                         </td>
//                                         <td className={getPercentageHighlight(stock.lowPercentage)}>
//                                             {stock.lowPercentage}%
//                                         </td>
//                                         <td>{stock.volume}</td>
//                                         <td>{stock.marketCap}</td>
//                                         <td>{stock.peRatio}</td>
//                                         <td>{stock.beta}</td>
//                                         <td>{stock.dividendYield}</td>
//                                     </tr>
//                                 ))
//                             ) : (
//                                 <tr>
//                                     <td colSpan={9} className="text-center">
//                                         No data available
//                                     </td>
//                                 </tr>
//                             )}
//                         </tbody>
//                     </table>
//                 </div>
//                 <div className="d-flex justify-content-center m-3">
//                     <Pagination
//                         current={currentPage}
//                         pageSize={itemsPerPage}
//                         total={sortedStocks.length}
//                         onChange={handlePageChange}
//                         showSizeChanger={false}
//                     />
//                 </div>
//             </div>
//         </section>
//     );
// }
