import React from 'react'

export default function LowPE() {
  return (
    <div>LowPE</div>
  )
}




// import { useState } from 'react';
// import lowpe from './lowpe.json';

// interface Stock {
//     symbol: string;
//     stockName: string;
//     currentPrice: number;
//     sector: string;
//     "52WeekHigh": number;
//     "52WeekLow": number;
//     highPercentage: number;
//     lowPercentage: number;
//     volume: number;
//     marketCap: number;
//     peRatio: number;
//     beta: number;
//     dividendYield: number;
// }

// export default function LowPE() {

//     const [stocks, setStocks] = useState<Stock[]>(lowpe.stocks);
//     const [sortConfig, setSortConfig] = useState<{ key: keyof Stock | null; direction: 'ascending' | 'descending' }>({
//         key: null,
//         direction: 'ascending',
//     });
//     const [searchTerm, setSearchTerm] = useState('');

//     const handleSort = (key: keyof Stock) => {
//         setSortConfig((prevState) => ({
//             key,
//             direction: prevState.key === key && prevState.direction === 'ascending' ? 'descending' : 'ascending',
//         }));
//     };

//     const getSortIcon = (key: keyof Stock) =>
//         sortConfig.key === key ? (sortConfig.direction === 'ascending' ? ' ▲' : ' ▼') : '';

//     const getHighlightColor = (currentPrice: number, value: number, isHigh: boolean) =>
//         isHigh ? (currentPrice < value ? 'text-success' : '') : (currentPrice > value ? 'text-danger' : '');

//     const getPercentageHighlight = (percentage: number) => (percentage >= 0 ? 'text-success' : 'text-danger');

//     const filteredStocks = stocks.filter((stock) =>
//         Object.values(stock).some((val) => val.toString().toLowerCase().includes(searchTerm.toLowerCase()))
//     );

//     const sortedStocks = [...filteredStocks].sort((a, b) => {
//         if (!sortConfig.key) return 0;
//         const aValue = a[sortConfig.key];
//         const bValue = b[sortConfig.key];
//         if (aValue < bValue) return sortConfig.direction === 'ascending' ? -1 : 1;
//         if (aValue > bValue) return sortConfig.direction === 'ascending' ? 1 : -1;
//         return 0;
//     });

//     const columns = [
//         { key: 'symbol', label: 'Symbol' },
//         { key: 'stockName', label: 'Stock Name' },
//         { key: 'currentPrice', label: 'Current Price' },
//         { key: 'sector', label: 'Sector' },
//         { key: '52WeekHigh', label: '52 Week High' },
//         { key: '52WeekLow', label: '52 Week Low' },
//         { key: 'highPercentage', label: 'High Percentage' },
//         { key: 'lowPercentage', label: 'Low Percentage' },
//         { key: 'volume', label: 'Volume' },
//         { key: 'marketCap', label: 'Market Cap' },
//         { key: 'peRatio', label: 'PE Ratio' },
//         { key: 'beta', label: 'Beta' },
//         { key: 'dividendYield', label: 'Dividend Yield' },
//     ];

//     return (
//         <section>
//             <div className="d-flex toptrend-sub-banner p-5">
//                 <div className="container">
//                     <div className="row d-flex justify-content-between">
//                         <div className="col-md-8">
//                             <h3>{lowpe.category}</h3>
//                             <p>{lowpe.description}</p>
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
//                 <div style={{ overflowX: 'auto' }}>
//                     <table className="table table-bordered mb-0">
//                         <thead>
//                             <tr>
//                                 {columns.map(({ key, label }) => (
//                                     <th
//                                         key={key}
//                                         onClick={() => handleSort(key as keyof Stock)}
//                                         style={{ padding: '20px', whiteSpace: 'nowrap', cursor: 'pointer' }}
//                                         aria-label={`Sort by ${label}`}
//                                     >
//                                         {label} {getSortIcon(key as keyof Stock)}
//                                     </th>
//                                 ))}
//                             </tr>
//                         </thead>

//                         <tbody>
//                             {sortedStocks.length === 0 ? (
//                                 <tr>
//                                     <td colSpan={columns.length} className="text-center">
//                                         No data available
//                                     </td>
//                                 </tr>
//                             ) : (
//                                 sortedStocks.map((stock) => (
//                                     <tr key={stock.symbol}>
//                                         {columns.map(({ key }) => (
//                                             <td
//                                                 key={key}
//                                                 className={
//                                                     key === 'symbol'
//                                                         ? 'table-active'
//                                                         : key === 'highPercentage' || key === 'lowPercentage'
//                                                             ? getPercentageHighlight(stock[key as keyof Stock] as number)
//                                                             : key === '52WeekHigh'
//                                                                 ? getHighlightColor(stock.currentPrice, stock[key as keyof Stock] as number, true)
//                                                                 : key === '52WeekLow'
//                                                                     ? getHighlightColor(stock.currentPrice, stock[key as keyof Stock] as number, false)
//                                                                     : ''
//                                                 }
//                                             >
//                                                 {typeof stock[key as keyof Stock] === 'number'
//                                                     ? key === 'currentPrice'
//                                                         ? `$${(stock[key as keyof Stock] as number).toFixed(2)}`
//                                                         : key === 'highPercentage' || key === 'lowPercentage'
//                                                             ? `${(stock[key as keyof Stock] as number).toFixed(2)}%`
//                                                             : (stock[key as keyof Stock] as number).toFixed(2)
//                                                     : stock[key as keyof Stock]}
//                                             </td>
//                                         ))}
//                                     </tr>
//                                 ))
//                             )}
//                         </tbody>
//                     </table>
//                 </div>
//             </div>
//         </section>
//     );
// }
