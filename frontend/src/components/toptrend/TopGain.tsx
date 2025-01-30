import { useEffect, useState } from "react";
import { topgain } from "./TopTrendSlice";
import { useDispatch, useSelector } from "react-redux";
import { Pagination } from "antd";
import { RootState } from "../../store/Store";


export default function TopGain() {

  const itemsPerPage = 10;
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortConfig, setSortConfig] = useState({
    key: "",
    direction: "asc",
  });

  const dispatch = useDispatch();
  const { topgainPayload, loading, error } = useSelector((state: RootState) => state.TopTrend);

  useEffect(() => {
    dispatch<any>(topgain({ page: currentPage, limit: itemsPerPage }));
  }, [dispatch, currentPage]);

  const requestSort = (key: any) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const filteredStocks =
    (topgainPayload?.data || topgainPayload || []).filter((item: any) =>
      item.Name && item.Name.toLowerCase().includes(searchTerm.toLowerCase())
    );

  const sortedStocks = [...filteredStocks].sort((a, b) => {
    if (sortConfig.key) {
      const aValue = a[sortConfig.key];
      const bValue = b[sortConfig.key];
      if (aValue < bValue) return sortConfig.direction === "asc" ? -1 : 1;
      if (aValue > bValue) return sortConfig.direction === "asc" ? 1 : -1;
    }
    return 0;
  });

  const currentItems = sortedStocks;

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
        {error && <div className="alert alert-danger">{error}</div>}
        {loading ? (
          <div>Loading...</div>
        ) : (
          <>
            <div style={{ overflowX: "auto" }}>
              <table className="table table-bordered mb-0">
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
                  {filteredStocks.length > 0 ? (
                    currentItems.map((stock) => (
                      <tr key={stock.Symbol}>
                        <td style={{ padding: '12px', cursor: "pointer" }} className="table-active">{stock.Symbol}</td>
                        <td style={{ padding: '20px', whiteSpace: 'nowrap' }}>{stock.Name}</td>
                        <td>${stock.Price}</td>
                        <td>{stock.Volume}</td>
                        <td>{stock.MarketCap}</td>
                        <td className={getNumberColor("DayHigh", stock.DayHigh)}>{stock.DayHigh}</td> {/* Always green */}
                        <td className={getNumberColor("DayLow", stock.DayLow)}>{stock.DayLow}</td> {/* Always red */}
                        <td className={getNumberColor("52WeeksHigh", stock["52WeeksHigh"])}>{stock["52WeeksHigh"]}</td> {/* Always green */}
                        <td className={getNumberColor("52WeeksLow", stock["52WeeksLow"])}>{stock["52WeeksLow"]}</td> {/* Always red */}
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
                      <td colSpan={16} className="text-center">No data available</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            <div className="d-flex justify-content-center m-3">
              <Pagination
                current={currentPage}
                pageSize={itemsPerPage}
                total={topgainPayload?.totalCount || 100}
                onChange={handlePageChange}
                showSizeChanger={false}
              />

            </div>
          </>
        )}
      </div>
    </section>
  );
}
