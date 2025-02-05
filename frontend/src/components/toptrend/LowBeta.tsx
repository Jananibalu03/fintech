import { useState, useEffect } from "react";
import { Pagination } from "antd";
import { lowbeta } from "./TopTrendSlice";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../../store/Store";


export default function LowBeta() {

  const itemsPerPage = 10;
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortConfig, setSortConfig] = useState({
    key: "",
    direction: "asc",
  });

  const dispatch = useDispatch()
  const { lowbetaPayload, loading } = useSelector(
    (state: RootState) => state.TopTrend
  );

  function debounce<T extends (...args: any[]) => void>(func: T, delay: number): T {
    let timer: ReturnType<typeof setTimeout>;
    return function (this: any, ...args: Parameters<T>) {
      clearTimeout(timer);
      timer = setTimeout(() => func.apply(this, args), delay);
    } as T;
  }

  const fetchData = debounce((Search, page) => {
    dispatch<any>(lowbeta({ Search, page, limit: itemsPerPage }));
  }, 500);

  useEffect(() => {
    fetchData(searchTerm, currentPage);
  }, [searchTerm, currentPage, dispatch]);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  const filteredData = (lowbetaPayload?.data || lowbetaPayload || []).filter((item: any) =>
    item.Name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.Symbol?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const sortedData = [...filteredData].sort((a, b) => {
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

  const handleSort = (key: string) => {
    const direction =
      sortConfig.key === key && sortConfig.direction === "asc" ? "desc" : "asc";
    setSortConfig({ key, direction });
  };


  const headers = [
    { key: "Symbol", label: "Symbol" },
    { key: "Name", label: "Stock Name" },
    { key: "Price", label: "Current Price" },
    { key: "1DVolatility", label: "1D Volatility" },
    { key: "1D", label: "1 Day Change" },
    { key: "1M", label: "1 Month Change" },
    { key: "1Y", label: "1 Year Change" },
    { key: "Volume", label: "Volume" },
    { key: "MarketCap", label: "Market Cap" },
    { key: "52WeeksHigh", label: "52 Week High" },
    { key: "52WeeksLow", label: "52 Week Low" },
    { key: "SMA50", label: "50-day SMA" },
    { key: "SMA200", label: "200-day SMA" },
    { key: "Beta", label: "Beta" },
    { key: "RSI", label: "RSI" },
    { key: "Sector", label: "Sector" }
  ];

  // const handleSort = (key: string) => {
  //   const direction =
  //     sortConfig.key === key && sortConfig.direction === "asc" ? "desc" : "asc";
  //   setSortConfig({ key, direction });
  // };

  const getNumberColor = (value: number | string) => {
    const numericValue = Number(value);
    if (isNaN(numericValue)) return "";
    if (numericValue < 0) return "text-danger";
    if (numericValue > 0) return "text-success";
    return "";
  };

  return (
    <section>
      <div className="d-flex toptrend-sub-banner p-5">
        <div className="container">
          <div className="row d-flex justify-content-between">
            <div className="col-md-8">
              <h3>Low Beta Stocks</h3>
              <p>Stocks with Low Beta</p>
            </div>

            <div className="col-md-3 text-end my-4">
              <input
                type="text"
                placeholder="Search stocks..."
                className="form-control"
                value={searchTerm}
                onChange={handleSearchChange}
              />
            </div>
          </div>
        </div>
      </div>

      <div className="container mb-5">
        {loading ? (
          <div className="d-flex justify-content-center">Loading...</div>
        ) : (
          <>

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
                        {sortConfig.key === header.key ? (
                          sortConfig.direction === "asc" ? (
                            " ▲"
                          ) : (
                            " ▼"
                          )
                        ) : (
                          ""
                        )}
                      </th>
                    ))}
                  </tr>
                </thead>

                <tbody>
                  {currentItems.length > 0 ? (
                    currentItems.map((stock, index) => (
                      <tr key={index}>
                        <td className='table-active'>{stock.Symbol}</td>
                        <td>{stock.Name}</td>
                        <td
                          style={{ padding: '1px 20px', cursor: "pointer" }}
                          className={getNumberColor(stock.Price)}
                        >
                          {stock.Price ? `$${parseFloat(stock.Price.replace("USD", "").trim())}` : "-"}
                        </td>
                        <td >{stock["1DVolatility"]}</td>
                        <td className={getNumberColor(stock["1D"])}>{stock["1D"]}</td>
                        <td className={getNumberColor(stock["1M"])}>{stock["1M"]}</td>
                        <td className={getNumberColor(stock["1Y"])}>{stock["1Y"]}</td>
                        <td>{stock.Volume}</td>
                        <td>{stock.MarketCap}</td>
                        < td style={{
                          padding: '12px',
                          color: 'green',
                        }}> ${stock['52WeeksHigh']} </td>
                        < td style={{
                          padding: '12px',
                          color: 'red',
                        }}> ${stock['52WeeksLow']} </td>
                        <td>{stock.SMA50}</td>
                        <td>{stock.SMA200}</td>
                        <td>{stock.Beta}</td>
                        <td>{stock.RSI}</td>
                        <td>{stock.Sector}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={12} className="text-center">
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
                total={lowbetaPayload?.totalCount || 100}
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
