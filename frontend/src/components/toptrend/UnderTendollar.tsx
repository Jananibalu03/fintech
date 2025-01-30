import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { undertendollar } from "./TopTrendSlice";
import { RootState } from "../../store/Store";
import { Pagination } from "antd";


export default function UnderTendollar() {

  const itemsPerPage = 10;
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortConfig, setSortConfig] = useState({ key: "", direction: "asc" });

  const dispatch = useDispatch();
  const { undertendollarPayload } = useSelector(
    (state: RootState) => state.TopTrend
  );

  useEffect(() => {
    dispatch<any>(undertendollar({ page: currentPage, limit: itemsPerPage }));
  }, [currentPage, dispatch]);

  const filteredStocks =
    (undertendollarPayload?.data || undertendollarPayload || []).filter((item: any) =>
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

  const requestSort = (key: any) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  const columns = [
    { key: "Symbol", label: "Symbol" },
    { key: "Name", label: "Stock Name" },
    { key: "Price", label: "Current Price" },
    { key: "Sector", label: "Sector" },
    { key: "Change", label: "Change (%)" },
    { key: "1D", label: "1D (%)" },
    { key: "1M", label: "1M (%)" },
    { key: "1Y", label: "1Y (%)" },
    { key: "Volume", label: "Volume" },
    { key: "MarketCap", label: "Market Cap" },
    { key: "PERatio", label: "PE Ratio" },
    { key: "Beta", label: "Beta" },
    { key: "RSI", label: "RSI" },
    { key: "SMA50", label: "SMA 50" },
    { key: "SMA200", label: "SMA 200" },
  ];

  return (
    <section>
      <div className="d-flex toptrend-sub-banner p-5">
        <div className="container">
          <div className="row d-flex justify-content-between">
            <div className="col-md-8">
              <h3>Under Ten Dollor</h3>
              <p>Stocks with Under Ten Dollor</p>
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
                {columns.map(({ key, label }) => (
                  <th
                    key={key}
                    style={{ padding: "20px", whiteSpace: "nowrap", cursor: "pointer" }}
                    onClick={() => requestSort(key)}
                  >
                    {label} {sortConfig.key === key && (sortConfig.direction === "asc" ? " ▲" : " ▼")}
                  </th>
                ))}
              </tr>
            </thead>

            <tbody>
              {sortedData.length > 0 ? (
                sortedData.map((stock: any) => (
                  <tr key={stock.Symbol}>
                    <td className="table-active">{stock.Symbol}</td>
                    <td style={{ padding: "20px", whiteSpace: "nowrap" }}>{stock.Name}</td>
                    <td>{stock.Price}</td>
                    <td>{stock.Sector}</td>
                    <td style={{ color: stock.Change.startsWith("-") ? "red" : "green" }}>
                      {stock.Change}
                    </td>
                    <td style={{ color: stock["1D"] < 0 ? "red" : "green" }}>
                      {stock["1D"].toFixed(2)}%
                    </td>
                    <td style={{ color: stock["1M"] < 0 ? "red" : "green" }}>
                      {stock["1M"].toFixed(2)}%
                    </td>
                    <td style={{ color: stock["1Y"] < 0 ? "red" : "green" }}>
                      {stock["1Y"].toFixed(2)}%
                    </td>
                    <td>{stock.Volume}</td>
                    <td>{stock.MarketCap}</td>
                    <td>{stock.PERatio}</td>
                    <td>{stock.Beta}</td>
                    <td>{stock.RSI}</td>
                    <td>{stock.SMA50.toFixed(2)}</td>
                    <td>{stock.SMA200.toFixed(2)}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={columns.length} className="text-center">
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
            onChange={handlePageChange}
            showSizeChanger={false}
            total={undertendollarPayload?.totalCount || 100}
          />
        </div>
      </div>
    </section>
  );
}
