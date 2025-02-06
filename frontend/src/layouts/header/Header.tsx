import { Link } from "react-router-dom";
import logo from "../../assets/images/fin-logo.png";


export default function Header() {

    return (
        <>
            <nav className="navbar navbar-expand-lg py-md-4">
                <div className="container">
                    <a href="/">
                        <img src={logo} alt="logo" className="main-logo me-4" />
                    </a>
                    <button
                        className="navbar-toggler"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#navbarSupportedContent"
                        aria-controls="navbarSupportedContent"
                        aria-expanded="false"
                        aria-label="Toggle navigation"
                    >
                        <span className="navbar-toggler-icon"></span>
                    </button>

                    <div className="collapse navbar-collapse" id="navbarSupportedContent">

                        <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                            {/* <li className="nav-item">
                                <a className="nav-link" aria-current="page" href="/dashboard">Watchlist</a>
                            </li>
                            <li className="nav-item">
                                <a className="nav-link" href="/top-trend">Top trend</a>
                            </li>

                            <li className="nav-item">
                                <a className="nav-link" href="#">Assistance</a>
                            </li> */}
                        </ul>

                        {/* <form className="d-flex" role="search">
                            <input
                                className="form-control me-2"
                                type="search"
                                placeholder="Search"
                                aria-label="Search"
                            />
                        </form> */}

                        <ul className="navbar-nav me-4 mb-lg-0">
                            <li className="nav-item">
                                <a className="nav-link" aria-current="page" href="/">Watchlist</a>
                            </li>
                            <li className="nav-item">
                                <a className="nav-link" href="/top-trend">Top trend</a>
                            </li>

                            {/* <li className="nav-item dropdown">
                                <Link
                                    to="#"
                                    className="profile nav-link dropdown-toggle"
                                    role="button"
                                    data-bs-toggle="dropdown"
                                    aria-expanded="false"
                                >
                                    <div className="header-without-profile profile-img">
                                        JB
                                    </div>
                                </Link>
                                <ul className="dropdown-menu header-profile">
                                    <li>
                                        <Link to="/profile" className="dropdown-item">
                                            Profile
                                        </Link>
                                    </li>
                                    <li>
                                        <button className="dropdown-item" >
                                            Logout
                                        </button>
                                    </li>
                                </ul>
                            </li> */}

                            {/* <li className="nav-item">
                                <button type="button" className="login-btn">
                                    <a className="nav-link text-white" href="#">Login</a>
                                </button>
                            </li> */}

                            {/* <li className="nav-item dropdown header-without-profile">
                                <a className="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                    JB
                                </a>
                                <ul className="dropdown-menu">
                                    <li>
                                        <Link to="/profile" className="dropdown-item">
                                            Profile
                                        </Link>
                                    </li>
                                    <li>
                                        <Link to="/profile" className="dropdown-item">
                                            Logout
                                        </Link>
                                    </li>
                                </ul>
                            </li> */}
                        </ul>

                    </div>
                </div>
            </nav>
        </>
    );
}
