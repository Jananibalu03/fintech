import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../../store/Store';
import { topperform } from './TopTrendSlice';
import { Pagination } from 'antd';


export default function TopPerform() {

  const [searchTerm, setSearchTerm] = useState("");
  const [sortConfig, setSortConfig] = useState({ key: "", direction: 'asc' });
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  const dispatch = useDispatch();

  useEffect(() => {
    dispatch<any>(topperform({ page: currentPage, limit: itemsPerPage }));
  }, [dispatch, currentPage, sortConfig, searchTerm]);

  const { topperformPayload } = useSelector((state: RootState) => state.TopTrend);

  const filteredStocks = (topperformPayload || []).filter((item: any) =>
    item.Name && item.Name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const requestSort = (key: string) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const sortedStocks = [...filteredStocks].sort((a: any, b: any) => {
    if (sortConfig.key) {
      const aValue = a[sortConfig.key];
      const bValue = b[sortConfig.key];
      if (typeof aValue === 'number' && typeof bValue === 'number') {
        return sortConfig.direction === 'asc' ? aValue - bValue : bValue - aValue;
      }
      if (typeof aValue === 'string' && typeof bValue === 'string') {
        return sortConfig.direction === 'asc'
          ? aValue.localeCompare(bValue)
          : bValue.localeCompare(aValue);
      }
    }
    return 0;
  });

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
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
              <h3>Top Performing Stocks</h3>
              <p>Stocks that have gained the Top Performing Stocks</p>
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
          <table className="table table-bordered table-hover mb-0">
            <thead>
              <tr>
                {['Symbol', 'Name', 'Price', 'Volume', 'MarketCap', 'DayHigh', 'DayLow', '52WeeksHigh', '52WeeksLow', 'SMA50', 'SMA200', 'Beta', 'PERatio', 'RSI', 'FreeCashFlowTTM', 'ProfitMarginsTTM', 'DividendPayoutRatioTTM', 'RevenueGrowthTTM', 'Sector'].map((key) => (
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
              {sortedStocks.length > 0 ? (
                sortedStocks.map((stock: any) => (
                  <tr key={stock.Symbol}>
                    <td style={{ padding: '12px', cursor: "pointer" }} className="table-active">{stock.Symbol}</td>
                    <td style={{ padding: '20px', whiteSpace: 'nowrap' }}>{stock.Name}</td>
                    <td>${stock.Price}</td>
                    <td>{stock.Volume}</td>
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
                  <td colSpan={13} className="text-center">
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
            total={topperformPayload?.totalCount || 100}
            onChange={handlePageChange}
            showSizeChanger={false}
          />
        </div>
      </div>
    </section>
  );
}
