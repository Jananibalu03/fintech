import React from 'react'

export default function LowBeta() {
  return (
    <div>LowBeta</div>
  )
}



// import React, { useState, useMemo } from "react";
// import lowbeta from "./lowbata.json";
// import { Pagination } from "antd";

// export default function LowBeta() {

//     const [searchTerm, setSearchTerm] = useState("");
//     const [sortConfig, setSortConfig] = useState<{ key: string; direction: "asc" | "desc" } | null>(null);
//     const itemsPerPage = 10;
//     const [currentPage, setCurrentPage] = useState(1);

//     const handlePageChange = (page: number) => {
//         setCurrentPage(page);
//     };

//     const getHighlightColor = (currentPrice: number, value: number, isHigh: boolean) => {
//         if (isHigh) {
//             return currentPrice < value ? "text-success" : "";
//         }
//         return currentPrice > value ? "text-danger" : "";
//     };

//     const getPercentageHighlight = (percentage: number) => {
//         return percentage >= 0 ? "text-success" : "text-danger";
//     };

   

//     const handleSort = (key: string) => {
//         let direction: "asc" | "desc" = "asc";
//         if (sortConfig?.key === key && sortConfig.direction === "asc") {
//             direction = "desc";
//         }
//         setSortConfig({ key, direction });
//     };

//     const filteredStocks = useMemo(() => {
//         return lowbeta.stocks.filter(
//             (stock) =>
//                 stock.symbol.toLowerCase().includes(searchTerm) ||
//                 stock.stockName.toLowerCase().includes(searchTerm)
//         );
//     }, [searchTerm]);

//     const sortedStocks = useMemo(() => {
//         const sorted = [...filteredStocks].sort((a: any, b: any) => {
//             if (!sortConfig) return 0;

//             const { key, direction } = sortConfig;
//             if (a[key] < b[key]) {
//                 return direction === "asc" ? -1 : 1;
//             }
//             if (a[key] > b[key]) {
//                 return direction === "asc" ? 1 : -1;
//             }
//             return 0;
//         });
//         return sorted;
//     }, [filteredStocks, sortConfig]);

//     const startIndex = (currentPage - 1) * itemsPerPage;
//     const currentPageStocks = sortedStocks.slice(startIndex, startIndex + itemsPerPage);

//     return (
//         <section>

//             <div className="d-flex toptrend-sub-banner p-5">
//                 <div className="container">
//                     <div className="row d-flex justify-content-between">
//                         <div className="col-md-8">
//                             <h3>{lowbeta.category}</h3>
//                             <p>{lowbeta.description}</p>
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
//                                 {[
//                                     { key: "symbol", label: "Symbol" },
//                                     { key: "stockName", label: "Stock Name" },
//                                     { key: "currentPrice", label: "Current Price" },
//                                     { key: "sector", label: "Sector" },
//                                     { key: "52WeekHigh", label: "52 Week High" },
//                                     { key: "52WeekLow", label: "52 Week Low" },
//                                     { key: "highPercentage", label: "High Percentage" },
//                                     { key: "lowPercentage", label: "Low Percentage" },
//                                     { key: "volume", label: "Volume" },
//                                     { key: "marketCap", label: "Market Cap" },
//                                     { key: "peRatio", label: "PE Ratio" },
//                                     { key: "beta", label: "Beta" },
//                                     { key: "dividendYield", label: "Dividend Yield" },
//                                 ].map((header) => (
//                                     <th
//                                         key={header.key}
//                                         style={{ padding: "20px", whiteSpace: "nowrap", cursor: "pointer" }}
//                                         onClick={() => handleSort(header.key)}
//                                     >
//                                         {header.label}
//                                         {sortConfig?.key === header.key && (
//                                             <span>{sortConfig.direction === "asc" ? ' ▲' : ' ▼'}</span>
//                                         )}
//                                     </th>
//                                 ))}
//                             </tr>
//                         </thead>

//                         <tbody>
//                             {currentPageStocks.length > 0 ? (
//                                 currentPageStocks.map((stock) => (
//                                     <tr key={stock.symbol}>
//                                         <td className="table-active">{stock.symbol}</td>
//                                         <td>{stock.stockName}</td>
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
//                                     <td colSpan={10} className="text-center">
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
