import { useState, useEffect } from "react";
import { Pagination } from "antd";
import { useDispatch, useSelector } from "react-redux";
import { highriskandreward } from "./TopTrendSlice";
import { RootState } from "../../store/Store";

export default function HighRishandReward() {

  const itemsPerPage = 10;
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortConfig, setSortConfig] = useState({
    key: "",
    direction: "asc",
  });

  const dispatch = useDispatch();
  const { highrandrPayload, loading } = useSelector(
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
    dispatch<any>(highriskandreward({ Search, page, limit: itemsPerPage }));
  }, 500);

  useEffect(() => {
    fetchData(searchTerm, currentPage);
  }, [searchTerm, currentPage, dispatch]);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  const filteredData = (highrandrPayload?.data || highrandrPayload || []).filter((item: any) =>
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
    { label: "Symbol", key: "Symbol" },
    { label: "Name", key: "Name" },
    { label: "Price", key: "Price" },
    { label: "1D Volatility", key: "1DVolatility" },
    { label: "1D", key: "1D" },
    { label: "1M", key: "1M" },
    { label: "1Y", key: "1Y" },
    { label: "Volume", key: "Volume" },
    { label: "MarketCap", key: "MarketCap" },
    { label: "52WeeksHigh", key: "52WeeksHigh" },
    { label: "52WeeksLow", key: "52WeeksLow" },
    { label: "SMA50", key: "SMA50" },
    { label: "SMA200", key: "SMA200" },
    { label: "Beta", key: "Beta" },
    { label: "RSI", key: "RSI" },
    { label: "PERatio", key: "PERatio" },
    { label: "PBRatioTTM", key: "PBRatioTTM" },
    { label: "EarningGrowthTTM", key: "EarningGrowthTTM" },
    { label: "DebttoEquityTTM", key: "DebttoEquityTTM" },
    { label: "RisktoRewardRatioTTM", key: "RisktoRewardRatioTTM" },
    { label: "DividendYieldTTM", key: "DividendYieldTTM" },
    { label: "Sector", key: "Sector" },
  ];

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
              <h3>High Risk and high Reword</h3>
              <p>Stocks with High Risk and high Reword, offering great opportunities for short-term gains.</p>
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
          <div>Loading...</div>
        ) : (
          <>
            <div className="table-responsive mb-0">
              <table className="table table-hover table-bordered mb-0">
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
                        <td style={{ padding: '12px', cursor: "pointer" }} className='table-active'>{stock.Symbol}</td>
                        <td style={{ padding: '12px', cursor: "pointer" }}>{stock.Name}</td>
                        <td style={{ padding: '1px 20px', cursor: "pointer" }} className={getNumberColor(stock.Price)}>{stock.Price}</td>
                        <td style={{ cursor: "pointer" }} className={getNumberColor(stock["1DVolatility"])}>
                          {stock["1DVolatility"]}
                        </td>
                        <td className={getNumberColor(stock["1D"])}>{stock["1D"]}</td>
                        <td className={getNumberColor(stock["1M"])}>{stock["1M"]}</td>
                        <td className={getNumberColor(stock["1Y"])}>{stock["1Y"]}</td>
                        <td>{stock.Volume}</td>
                        <td>{stock.MarketCap}</td>
                        < td style={{ padding: '12px' }}> ${stock['52WeeksHigh']} </td>
                        < td style={{ padding: '12px' }}> ${stock['52WeeksLow']} </td>
                        <td>{stock.SMA50}</td>
                        <td>{stock.SMA200}</td>
                        <td>{stock.Beta}</td>
                        <td>{stock.RSI}</td>

                        <td>{stock.PERatio}</td>
                        <td>{stock.PBRatioTTM}</td>
                        <td>{stock.EarningGrowthTTM}</td>
                        <td>{stock.DebttoEquityTTM}</td>
                        <td>{stock.RisktoRewardRatioTTM}</td>
                        <td>{stock.DividendYieldTTM}</td>
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
                onChange={handlePageChange}
                showSizeChanger={false}
                total={highrandrPayload?.totalCount || 100}
              />

            </div>
          </>
        )}
      </div>
    </section>
  );
}
