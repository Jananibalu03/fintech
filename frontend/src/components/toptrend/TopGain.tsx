import { useEffect, useState } from "react";
import { topgain } from "./TopTrendSlice";
import { useDispatch, useSelector } from "react-redux";
import { Pagination } from "antd";
import { RootState } from "../../store/Store";

export default function TopGain() {
  const [searchTerm, setSearchTerm] = useState("");
  const [percentageChange, setPercentageChange] = useState("");
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  const [currentPage, setCurrentPage] = useState(1); // Track the current page
  const itemsPerPage = 10; // Define how many items you want to show per page

  const dispatch = useDispatch();
  const { topgainPayload, loading, error } = useSelector((state: RootState) => state.TopTrend);

  useEffect(() => {
    dispatch<any>(topgain({ page: currentPage, limit: itemsPerPage })); // Fetch all data, no limit applied
  }, [dispatch, currentPage]);

  const requestSort = (key: any) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const compareValues = (a: any, b: any, key: string, direction: string) => {
    if (key === 'Change' || key === 'Price') {
      a = parseFloat(a);
      b = parseFloat(b);
    }

    if (a < b) {
      return direction === 'asc' ? -1 : 1;
    }
    if (a > b) {
      return direction === 'asc' ? 1 : -1;
    }
    return 0;
  };

  const sortedStocks = [...(topgainPayload || [])].sort((a, b) => {
    if (sortConfig.key === null) return 0;
    return compareValues(a[sortConfig.key], b[sortConfig.key], sortConfig.key, sortConfig.direction);
  });

  const filteredStocks = sortedStocks.filter(stock => {
    const matchesSearch = stock.Symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
      stock.Name.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesPercentageChange = percentageChange
      ? parseFloat(stock.Change) >= parseFloat(percentageChange)
      : true;

    return matchesSearch && matchesPercentageChange;
  });

  const getPriceHighlight = (price: string) => {
    const parsedPrice = parseFloat(price);
    return parsedPrice >= 0 ? 'text-success' : 'text-danger';
  };

  const getPercentageHighlight = (percentage: string) => {
    const parsedPercentage = parseFloat(percentage);
    return parsedPercentage >= 0 ? 'text-success' : 'text-danger';
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  const startIndex = (currentPage - 1) * itemsPerPage;
  const currentItems = filteredStocks.slice(startIndex, startIndex + itemsPerPage);

  return (
    <section>
      <div className="d-flex toptrend-sub-banner p-5">
        <div className="container">
          <div className="row d-flex justify-content-between">
            <div className="col-md-8">
              <h3>Top Gainers</h3>
              <p>Stocks that have gained the most today</p>
            </div>

            <div className="col-md-3 text-end my-4">
              <input
                type="text"
                placeholder="Search stocks..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="form-control"
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
                {['Symbol', 'Name', 'Price', 'Change', 'Volume', 'MarketCap', 'DayHigh', 'DayLow', '52WeeksHigh', '52WeeksLow', 'SMA50', 'SMA200', 'Beta', 'PERatio', 'RSI', 'FreeCashFlowTTM', 'ProfitMarginsTTM', 'DividendPayoutRatioTTM', 'RevenueGrowthTTM', 'Sector'].map((key) => (
                  <th
                    key={key}
                    style={{ padding: "20px", whiteSpace: "nowrap", cursor: "pointer" }}
                    onClick={() => requestSort(key)}
                  >
                    {key}
                    {sortConfig.key === key ? (sortConfig.direction === 'asc' ? ' ▲' : ' ▼') : ''}
                  </th>
                ))}
              </tr>
            </thead>

            <tbody>
              {filteredStocks.length > 0 ? (
                currentItems.map((stock) => (
                  <tr key={stock.Symbol}>
                    <td style={{ padding: '12px', cursor: "pointer" }} className="table-active">{stock.Symbol}</td>
                    <td style={{ padding: '20px', whiteSpace: 'nowrap' }}>{stock.Name}</td>
                    <td className={getPriceHighlight(stock.Price)}>${stock.Price}</td>
                    <td className={getPercentageHighlight(stock.Change)}>{stock.Change}</td>
                    <td>{stock.Volume}</td>
                    <td>{stock.MarketCap}</td>
                    <td>{stock.DayHigh}</td>
                    <td>{stock.DayLow}</td>
                    <td>{stock['52WeeksHigh']}</td>
                    <td>{stock['52WeeksLow']}</td>
                    <td>{stock.SMA50}</td>
                    <td>{stock.SMA200}</td>
                    <td>{stock.Beta}</td>
                    <td>{stock.PERatio}</td>
                    <td>{stock.RSI}</td>
                    <td>{stock.FreeCashFlowTTM}</td>
                    <td>{stock.ProfitMarginsTTM}</td>
                    <td>{stock.DividendPayoutRatioTTM}</td>
                    <td>{stock.RevenueGrowthTTM}</td>
                    <td>{stock.Sector}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={20} className="text-center">No data available</td>
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
