import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { toploss } from './TopTrendSlice';
import { Pagination } from 'antd';
import { RootState } from '../../store/Store';

export default function TopLoss() {

  const itemsPerPage = 10;
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortConfig, setSortConfig] = useState({
    key: "",
    direction: "asc",
  });

  const dispatch = useDispatch();
  const toplossPayload = useSelector((state: RootState) => state.TopTrend.toplossPayload) || [];

  useEffect(() => {
    dispatch<any>(toploss({ page: currentPage, limit: itemsPerPage }));
  }, [dispatch, currentPage]);

  const filteredStocks = (toplossPayload?.data || toplossPayload || []).filter((item: any) =>
    item.Name && item.Name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const sortedData = [...filteredStocks].sort((a, b) => {
    if (sortConfig.key) {
      const aValue = a[sortConfig.key];
      const bValue = b[sortConfig.key];
      if (aValue < bValue) return sortConfig.direction === "asc" ? -1 : 1;
      if (aValue > bValue) return sortConfig.direction === "asc" ? 1 : -1;
    }
    return 0;
  });

  const currentItems = sortedData;

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  const headers = [
    { label: "Symbol", key: "symbol" },
    { label: "Stock Name", key: "stockName" },
    { label: "Current Price", key: "currentPrice" },
    { label: "Market Cap", key: "marketCap" },
    { label: "Day High", key: "dayHigh" },
    { label: "Day Low", key: "dayLow" },
    { label: "52 Week High", key: "52WeeksHigh" },
    { label: "52 Week Low", key: "52WeeksLow" },
    { label: "SMA50", key: "sma50" },
    { label: "SMA200", key: "sma200" },
    { label: "Beta", key: "beta" },
    { label: "PE Ratio", key: "peRatio" },
    { label: "RSI", key: "rsi" },
    { label: "Free Cash Flow", key: "freeCashFlow" },
    { label: "Profit Margins", key: "profitMargins" },
    { label: "Dividend Payout Ratio", key: "dividendPayoutRatio" },
    { label: "Revenue Growth", key: "revenueGrowth" },
    { label: "Sector", key: "sector" },
  ];

  const requestSort = (key: string) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const getNumberColor = (key: string, value: number | string) => {
    const numericValue = Number(value);
    if (isNaN(numericValue)) return "";
    if (key === "DayHigh" || key === "52WeeksHigh") return "text-success";
    if (key === "DayLow" || key === "52WeeksLow") return "text-danger";
    return numericValue < 0 ? "text-danger" : "text-success";
  };

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
              {currentItems.length > 0 ? (
                currentItems.map((stock, index) => (
                  <tr key={index}>
                    <td>{stock.Symbol}</td>
                    <td>{stock.Name}</td>
                    <td>{stock.Price}</td>
                    <td>{stock.MarketCap}</td>
                    <td className={getNumberColor("DayHigh", stock.DayHigh)}>{stock.DayHigh}</td>
                    <td className={getNumberColor("DayLow", stock.DayLow)}>{stock.DayLow}</td>
                    <td className={getNumberColor("52WeeksHigh", stock["52WeeksHigh"])}>{stock["52WeeksHigh"]}</td>
                    <td className={getNumberColor("52WeeksLow", stock["52WeeksLow"])}>{stock["52WeeksLow"]}</td>
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
                  <td colSpan={16} className="text-center">
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
            total={toplossPayload?.totalCount || 100}
            onChange={handlePageChange}
            showSizeChanger={false}
          />
        </div>
      </div>
    </section>
  );
}
