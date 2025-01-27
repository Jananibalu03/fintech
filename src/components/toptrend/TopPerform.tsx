import React from 'react'

export default function TopPerform() {
  return (
    <div>TopPerform</div>
  )
}



// import { useState } from 'react';
// import topperform from "./topperform.json";

// export default function TopPerform() {
//     const [searchTerm, setSearchTerm] = useState("");
//     const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });

//     const columns = [
//         { header: 'Symbol', key: 'symbol' },
//         { header: 'Stock Name', key: 'stockName' },
//         { header: 'Current Price', key: 'currentPrice' },
//         { header: 'Percentage Change', key: 'percentageChange' },
//         { header: 'Sector', key: 'sector' },
//         { header: 'Market Cap', key: 'marketCap' },
//         { header: 'Description', key: 'description' },
//     ];

//     const requestSort = (key:any) => {
//         let direction = 'asc';
//         if (sortConfig.key === key && sortConfig.direction === 'asc') {
//             direction = 'desc';
//         }
//         setSortConfig({ key, direction });
//     };

//     const sortedStocks = [...topperform.stocks].sort((a:any, b:any) => {
//         if (sortConfig.key) {
//             const aValue = a[sortConfig.key];
//             const bValue = b[sortConfig.key];

//             if (typeof aValue === 'number' && typeof bValue === 'number') {
//                 return sortConfig.direction === 'asc' ? aValue - bValue : bValue - aValue;
//             }
//             if (typeof aValue === 'string' && typeof bValue === 'string') {
//                 return sortConfig.direction === 'asc'
//                     ? aValue.localeCompare(bValue)
//                     : bValue.localeCompare(aValue);
//             }
//         }
//         return 0;
//     });

//     const filteredStocks = sortedStocks.filter(
//         (stock) =>
//             stock.symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
//             stock.stockName.toLowerCase().includes(searchTerm.toLowerCase())
//     );

//     return (
//         <section>

//             <div className="d-flex toptrend-sub-banner p-5">
//                 <div className="container">
//                     <div className="row d-flex justify-content-between">
//                         <div className="col-md-8">
//                             <h3>{topperform.category}</h3>
//                             <p>{topperform.description}</p>
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
//                                 {columns.map(({ header, key }) => (
//                                     <th
//                                         key={key}
//                                         style={{ padding: "20px", whiteSpace: "nowrap", cursor: "pointer" }}
//                                         onClick={() => requestSort(key)}
//                                     >
//                                         {header}
//                                         {sortConfig.key === key && (sortConfig.direction === 'asc' ? ' ▲' : ' ▼')}
//                                     </th>
//                                 ))}
//                             </tr>
//                         </thead>
//                         <tbody>
//                             {filteredStocks.length > 0 ? (
//                                 filteredStocks.map((stock:any) => (
//                                     <tr key={stock.symbol}>
//                                         {columns.map(({ key }) => (
//                                             <td key={key} className={key === "symbol" ? "table-active" : ""}>
//                                                 {key === "percentageChange" ? (
//                                                     <span
//                                                         className={
//                                                             stock[key] >= 0 ? "text-success" : "text-danger"
//                                                         }
//                                                     >
//                                                         {stock[key]}%
//                                                     </span>
//                                                 ) : key === "currentPrice" ? (
//                                                     `$${stock[key].toFixed(2)}`
//                                                 ) : (
//                                                     stock[key]
//                                                 )}
//                                             </td>
//                                         ))}
//                                     </tr>
//                                 ))
//                             ) : (
//                                 <tr>
//                                     <td colSpan={columns.length} className="text-center">
//                                         No data available
//                                     </td>
//                                 </tr>
//                             )}
//                         </tbody>
//                     </table>
//                 </div>
//             </div>
//         </section>
//     );
// }
