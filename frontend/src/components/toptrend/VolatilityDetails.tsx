import { useEffect, useState } from "react";
import { Pagination } from "antd";
import "antd/dist/reset.css";
import { useDispatch, useSelector } from "react-redux";
import { fetchVolatility } from "./TopTrendSlice";
import { RootState } from "../../store/Store";


export default function VolatilityDetails() {

    const itemsPerPage = 10;
    const [currentPage, setCurrentPage] = useState(1);
    const [searchTerm, setSearchTerm] = useState("");
    const [sortConfig, setSortConfig] = useState({
        key: "",
        direction: "asc",
    });

    const dispatch = useDispatch();
    const { fetchVolatilityPayload, error, loading } = useSelector(
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
        dispatch<any>(fetchVolatility({ Search, page, limit: itemsPerPage }));
    }, 500);

    useEffect(() => {
        fetchData(searchTerm, currentPage);
    }, [searchTerm, currentPage, dispatch]);

    const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSearchTerm(e.target.value);
    };

    const filteredData = (fetchVolatilityPayload?.data || fetchVolatilityPayload || []).filter((item: any) =>
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
        { label: "SMA50", key: "SMA50" },
        { label: "SMA200", key: "SMA200" },
        { label: "Beta", key: "Beta" },
        { label: "DividendYieldTTM", key: "DividendYieldTTM" },
        { label: "RSI", key: "RSI" },
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
                            <h3>Volatility</h3>
                            <p>Stocks with high price swings, offering great opportunities for short-term gains.</p>
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
                {/* {error && <div className="alert/ alert-danger">{error}</div>} */}
                {loading ? (
                    <div className="d-flex justify-content-center">Loading...</div>
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
                                                <td
                                                    style={{ padding: '1px 20px', cursor: "pointer" }}
                                                    className={getNumberColor(stock.Price)}
                                                >
                                                    {stock.Price ? `$${parseFloat(stock.Price.replace("USD", "").trim())}` : "-"}
                                                </td>
                                                <td style={{ cursor: "pointer" }}>
                                                    {stock["1DVolatility"]}
                                                </td>
                                                <td className={getNumberColor(stock["1D"])}>{stock["1D"]}</td>
                                                <td className={getNumberColor(stock["1M"])}>{stock["1M"]}</td>
                                                <td className={getNumberColor(stock["1Y"])}>{stock["1Y"]}</td>
                                                <td>{stock.Volume}</td>
                                                <td>{stock.MarketCap}</td>
                                                <td>{stock.SMA50}</td>
                                                <td>{stock.SMA200}</td>
                                                <td>{stock.Beta}</td>
                                                <td>{stock.DividendYieldTTM}</td>
                                                <td>{stock.RSI}</td>
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
                                total={fetchVolatilityPayload?.totalCount || 100}
                            />

                        </div>
                    </>
                )}
            </div>
        </section>
    );
}
