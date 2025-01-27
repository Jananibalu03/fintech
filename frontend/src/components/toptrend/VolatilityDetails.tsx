import React from 'react'

export default function VolatilityDetails() {
    return (
        <div>VolatilityDetails</div>
    )
}


// import { useState } from "react";
// import { Pagination } from "antd";
// import "antd/dist/reset.css";
// import volatilityData from "./volatility.json";

// export default function VolatilityDetails() {
//     const itemsPerPage = 10;
//     const [currentPage, setCurrentPage] = useState(1);
//     const [searchTerm, setSearchTerm] = useState("");
//     const [sortConfig, setSortConfig] = useState({ key: null, direction: "ascending" });

//     const headers = [
//         { key: "symbol", label: "Symbol" },

//         { key: "stockName", label: "Stock Name" },
//         { key: "currentPrice", label: "Current Price ($)" },
//         { key: "volatility", label: "Volatility (%)" },
//         { key: "description", label: "Description" },
//     ];

//     const sortedData = [...volatilityData.data].sort((a: any, b: any) => {
//         if (!sortConfig.key) return 0;

//         const aValue = a[sortConfig.key];
//         const bValue = b[sortConfig.key];

//         if (typeof aValue === "string") {
//             return sortConfig.direction === "ascending"
//                 ? aValue.localeCompare(bValue)
//                 : bValue.localeCompare(aValue);
//         }

//         return sortConfig.direction === "ascending" ? aValue - bValue : bValue - aValue;
//     });

//     const filteredData = sortedData.filter((stock) =>
//         [stock.stockName, stock.symbol]
//             .some((field) => field.toLowerCase().includes(searchTerm.toLowerCase()))
//     );


//     const startIndex = (currentPage - 1) * itemsPerPage;
//     const currentItems = filteredData.slice(startIndex, startIndex + itemsPerPage);


//     const handleSort = (key: any) => {
//         setSortConfig((prevState) => ({
//             key,
//             direction: prevState.key === key && prevState.direction === "ascending" ? "descending" : "ascending",
//         }));
//     };

//     const handlePageChange = (page: any) => {
//         setCurrentPage(page);
//     };

//     return (
//         <section>
//             <div className="d-flex toptrend-sub-banner p-5">
//                 <div className="container">
//                     <div className="row d-flex justify-content-between">
//                         <div className="col-md-8">
//                             <h3>{volatilityData.category}</h3>
//                             <p>{volatilityData.description}</p>
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

//             <div className="container mb-4">
//                 <div className="table-responsive">
//                     <table className="table table-bordered">
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
//                                             (sortConfig.direction === "ascending" ? "▲" : "▼")}
//                                     </th>
//                                 ))}
//                             </tr>
//                         </thead>
//                         <tbody>
//                             {currentItems.length > 0 ? (
//                                 currentItems.map((stock, index) => (
//                                     <tr key={index}>
//                                         <td style={{ padding: '12px', cursor: "pointer" }} className="table-active">{stock.symbol}</td>

//                                         <td >{stock.stockName}</td>
//                                         <td>{stock.currentPrice.toFixed(2)}</td>
//                                         <td>{stock.volatility}</td>
//                                         <td>{stock.description}</td>
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
//                         total={filteredData.length}
//                         onChange={handlePageChange}
//                         showSizeChanger={false}
//                     />
//                 </div>
//             </div>
//         </section>
//     );
// }
