import React from 'react'

export default function UnderFiftyDollar() {
  return (
    <div>UnderFiftyDollar</div>
  )
}




// import { useState, useMemo } from "react";
// import underFiftydollar from "./underfiftydollar.json";
// import { Pagination } from "antd";

// export default function UnderFiftyDollar() {
//     const [searchTerm, setSearchTerm] = useState("");
//     const [sortConfig, setSortConfig] = useState<{ key: string | null; direction: "asc" | "desc" | null }>({
//         key: null,
//         direction: null,
//     });

//     const itemsPerPage = 10;
//     const [currentPage, setCurrentPage] = useState(1);

//     const handlePageChange = (page: number) => {
//         setCurrentPage(page);
//     };

//     const headers = [
//         { key: "symbol", label: "Symbol" },
//         { key: "stockName", label: "Stock Name" },
//         { key: "currentPrice", label: "Current Price" },
//         { key: "sector", label: "Sector" },
//         { key: "industry", label: "Industry" },
//         { key: "52WeekHigh", label: "52 Week High" },
//         { key: "52WeekLow", label: "52 Week Low" },
//         { key: "marketCap", label: "Market Cap" },
//         { key: "peRatio", label: "P/E Ratio" },
//         { key: "dividendYield", label: "Dividend Yield" },
//         { key: "earningsDate", label: "Earnings Date" },
//         { key: "description", label: "Description" },
//     ];

//     const filteredStocks = useMemo(() => {
//         return underFiftydollar.stocks.filter(
//             (stock) =>
//                 stock.symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
//                 stock.stockName.toLowerCase().includes(searchTerm.toLowerCase()) ||
//                 stock["peRatio"].toString().includes(searchTerm)
//         );
//     }, [searchTerm]);

//     const sortedStocks = useMemo(() => {
//         return [...filteredStocks].sort((a: any, b: any) => {
//             if (sortConfig.key === null) return 0;
//             const aValue = a[sortConfig.key];
//             const bValue = b[sortConfig.key];

//             if (typeof aValue === "string") {
//                 return sortConfig.direction === "asc"
//                     ? aValue.localeCompare(bValue)
//                     : bValue.localeCompare(aValue);
//             }
//             if (typeof aValue === "number") {
//                 return sortConfig.direction === "asc" ? aValue - bValue : bValue - aValue;
//             }
//             return 0;
//         });
//     }, [filteredStocks, sortConfig]);

//     const handleSort = (key: string) => {
//         setSortConfig((prevConfig) => {
//             const isAscending = prevConfig.key === key && prevConfig.direction === "asc";
//             return {
//                 key,
//                 direction: isAscending ? "desc" : "asc",
//             };
//         });
//     };

//     const getSortIndicator = (key: string) => {
//         if (sortConfig.key !== key) return null;
//         return sortConfig.direction === "asc" ? " ▲" : " ▼";
//     };

//     const startIndex = (currentPage - 1) * itemsPerPage;
//     const currentPageStocks = sortedStocks.slice(startIndex, startIndex + itemsPerPage);

//     return (
//         <section>

//             <div className="d-flex toptrend-sub-banner p-5">
//                 <div className="container">
//                     <div className="row d-flex justify-content-between">
//                         <div className="col-md-8">
//                             <h3>{underFiftydollar.category}</h3>
//                             <p>{underFiftydollar.description}</p>
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
//                                         {header.label} {getSortIndicator(header.key)}
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
//                                         <td>{stock.industry}</td>
//                                         <td>${stock["52WeekHigh"].toFixed(2)}</td>
//                                         <td>${stock["52WeekLow"].toFixed(2)}</td>
//                                         <td>{stock.marketCap}</td>
//                                         <td>{stock.peRatio}</td>
//                                         <td>{stock.dividendYield}</td>
//                                         <td>{stock.earningsDate}</td>
//                                         <td style={{ whiteSpace: "nowrap" }}>{stock.description}</td>
//                                     </tr>
//                                 ))
//                             ) : (
//                                 <tr>
//                                     <td colSpan={headers.length} className="text-center">
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
