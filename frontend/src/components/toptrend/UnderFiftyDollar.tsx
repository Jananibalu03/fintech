import { useState, useEffect } from "react";
import { Pagination } from "antd";
import { useDispatch, useSelector } from "react-redux";
import { underfiftydollor } from "./TopTrendSlice";
import { RootState } from "../../store/Store";

export default function UnderFiftyDollar() {
  const itemsPerPage = 10;
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortConfig, setSortConfig] = useState<{ key: string | null; direction: "asc" | "desc" | null }>({
    key: "",
    direction: "asc",
  });

  const dispatch = useDispatch();
  const { underfiftydollorPayload } = useSelector((state: RootState) => state.TopTrend);

  useEffect(() => {
    dispatch<any>(underfiftydollor({ page: currentPage, limit: itemsPerPage }));
  }, [dispatch, currentPage]);

  const headers = [
    { key: "Symbol", label: "Symbol" },
    { key: "Name", label: "Stock Name" },
    { key: "Price", label: "Current Price" },
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
    { key: "Sector", label: "Sector" },
  ];


  const filteredData = (underfiftydollorPayload?.data || underfiftydollorPayload || []).filter((item: any) =>
    item.Name && item.Name.toLowerCase().includes(searchTerm.toLowerCase())
  );
  const sortedStocks = [...filteredData].sort((a, b) => {
    if (sortConfig.key) {
      const aValue = a[sortConfig.key];
      const bValue = b[sortConfig.key];
      if (aValue < bValue) return sortConfig.direction === "asc" ? -1 : 1;
      if (aValue > bValue) return sortConfig.direction === "asc" ? 1 : -1;
    }
    return 0;
  });

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  const handleSort = (key: string) => {
    const direction = sortConfig.key === key && sortConfig.direction === "asc" ? "desc" : "asc";
    setSortConfig({ key, direction });
  };

  return (
    <section>
      <div className="d-flex toptrend-sub-banner p-5">
        <div className="container">
          <div className="row d-flex justify-content-between">
            <div className="col-md-8">
              <h3>Under Fifty Dollor</h3>
              <p>Stocks with Under Fifty Dollor</p>
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
                    onClick={() => handleSort(header.key)}
                    style={{ padding: "20px", whiteSpace: "nowrap", cursor: "pointer" }}
                  >
                    {header.label}
                    {sortConfig.key === header.key ? (sortConfig.direction === "asc" ? " ▲" : " ▼") : ""}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {sortedStocks.length > 0 ? (
                sortedStocks.map((stock: any) => (
                  <tr key={stock.Symbol}>
                    <td className="table-active">{stock.Symbol}</td>
                    <td style={{ padding: "20px", whiteSpace: "nowrap" }}>{stock.Name}</td>
                    <td>{stock.Price}</td>
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
                    <td>{stock.Sector}</td>

                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={14} className="text-center">
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
            total={sortedStocks.totalcount || 100}
            onChange={handlePageChange}
            showSizeChanger={false}
          />
        </div>
      </div>
    </section>
  );
}
