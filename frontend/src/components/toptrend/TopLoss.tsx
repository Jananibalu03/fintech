import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { toploss } from './TopTrendSlice';
import { Pagination } from 'antd';
import { RootState } from '../../store/Store';

export default function TopLoss() {

  const [searchTerm, setSearchTerm] = useState("");
  const [percentageChange, setPercentageChange] = useState("");
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  const dispatch = useDispatch();
  const toplossPayload = useSelector((state: RootState) => state.TopTrend.toplossPayload) || [];
  console.log(toplossPayload);

  useEffect(() => {
    dispatch(toploss({ page: currentPage, limit: itemsPerPage }));
  }, [dispatch]);

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    dispatch(toploss({ page, limit: itemsPerPage }));
  };

  const headers = [
    { label: "Symbol", key: "symbol" },
    { label: "Stock Name", key: "stockName" },
    { label: "Current Price", key: "currentPrice" },
    { label: "Percentage Change", key: "percentageChange" },
    { label: "Sector", key: "sector" },
    { label: "Market Cap", key: "marketCap" },
    { label: "Day High", key: "dayHigh" },
    { label: "Day Low", key: "dayLow" },
    { label: "52 Week High", key: "fiftyTwoWeekHigh" },
    { label: "52 Week Low", key: "fiftyTwoWeekLow" },
    { label: "SMA50", key: "sma50" },
    { label: "SMA200", key: "sma200" },
    { label: "Beta", key: "beta" },
    { label: "PE Ratio", key: "peRatio" },
    { label: "RSI", key: "rsi" },
    { label: "Free Cash Flow", key: "freeCashFlow" },
    { label: "Profit Margins", key: "profitMargins" },
    { label: "Dividend Payout Ratio", key: "dividendPayoutRatio" },
    { label: "Revenue Growth", key: "revenueGrowth" },
  ];

  const requestSort = (key: any) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const sortedStocks = Array.isArray(toplossPayload) ? [...toplossPayload].sort((a: any, b: any) => {
    if (sortConfig.key) {
      const aValue = a[sortConfig.key];
      const bValue = b[sortConfig.key];
      // Check if the values are numbers and sort accordingly
      if (typeof aValue === "number" && typeof bValue === "number") {
        return sortConfig.direction === 'asc' ? aValue - bValue : bValue - aValue;
      }
      // If the values are strings, use localeCompare
      if (typeof aValue === "string" && typeof bValue === "string") {
        return sortConfig.direction === 'asc'
          ? aValue.localeCompare(bValue)
          : bValue.localeCompare(aValue);
      }
      return 0;
    }
    return 0;
  }) : [];


  const filteredStocks = sortedStocks.filter(stock =>
    stock.symbol && stock.symbol.toLowerCase().includes(searchTerm.toLowerCase()) &&
    (percentageChange ? stock.Change >= percentageChange : true)
  );

  const getColor = (percentage: number) => {
    return percentage > 0 ? { color: 'green' } : { color: 'red' };
  };

  // Paginate the filteredStocks
  const startIndex = (currentPage - 1) * itemsPerPage;
  const paginatedStocks = filteredStocks.slice(startIndex, startIndex + itemsPerPage);


  return (
    <section>
      <div className="d-flex toptrend-sub-banner p-5">
        <div className="container">
          <div className="row d-flex justify-content-between">
            <div className="col-md-8">
              <h3>Top Loss Stocks</h3>
              <p>Detailed information for the stocks with the biggest losses today.</p>
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
        <div style={{ overflowX: "auto" }}>
          <table className="table table-bordered mb-0">
            <thead>
              <tr>
                {headers.map((header) => (
                  <th
                    key={header.key}
                    style={{ padding: '20px', whiteSpace: 'nowrap', cursor: "pointer" }}
                    onClick={() => requestSort(header.key)}
                  >
                    {header.label}
                    {sortConfig.key === header.key && (sortConfig.direction === 'asc' ? ' ▲' : ' ▼')}
                  </th>
                ))}
              </tr>
            </thead>

            <tbody>
              {paginatedStocks.length > 0 ? (
                paginatedStocks.map((stock, index) => (

                  <tr key={index}>

                    <td>{stock.Symbol}</td>
                    <td>{stock.Name}</td>
                    <td>{stock.Price}</td>
                    <td style={{ ...getColor(parseFloat(stock.Change)) }}>
                      {stock.Change}
                    </td>
                    <td>{stock.Sector}</td>
                    <td>{stock.MarketCap}</td>
                    <td>{stock.DayHigh}</td>
                    <td>{stock.DayLow}</td>
                    <td>{stock["52WeeksHigh"]}</td>
                    <td>{stock["52WeeksLow"]}</td>
                    <td>{stock.SMA50}</td>
                    <td>{stock.SMA200}</td>
                    <td>{stock.Beta}</td>
                    <td>{stock.PERatio}</td>
                    <td>{stock.RSI}</td>
                    <td>{stock.FreeCashFlowTTM}</td>
                    <td>{stock.ProfitMarginsTTM}</td>
                    <td>{stock.DividendPayoutRatioTTM}</td>
                    <td>{stock.RevenueGrowthTTM}</td>
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
