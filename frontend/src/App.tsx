import { Route, Routes, Navigate, useLocation } from 'react-router-dom';
import './App.css';
import Bot from './bot/Bot';
import Header from './layouts/header/Header';
import Footer from './layouts/footer/Footer';
import "bootstrap/dist/css/bootstrap.min.css";
import Dashboard from './components/search/Dashboard';
import Search from './components/search/Search';
import VolatilityDetails from './components/toptrend/VolatilityDetails';
import UnderTendollar from './components/toptrend/UnderTendollar';
import UnderFiftyDollar from './components/toptrend/UnderFiftyDollar';
import NegativeBeta from './components/toptrend/NegativeBeta';
import LowBeta from './components/toptrend/LowBeta';
import HighRishandReward from './components/toptrend/HighRishandReward';
import DebitFree from './components/toptrend/DebitFree';
import Dividend from './components/toptrend/Dividend';
import LowPE from './components/toptrend/LowPE';
import TopGain from './components/toptrend/TopGain';
import TopLoss from './components/toptrend/TopLoss';
import TopPerform from './components/toptrend/TopPerform';
import HighDividend from './components/toptrend/HighDividend';
import TopTrends from './components/toptrend/TopTrends';
import LowWeek52 from './components/toptrend/LowWeek52';
import HignWeek52 from './components/toptrend/HignWeek52';
import Login from './account/Login';
import Registration from './account/Registration';
import Cookies from 'js-cookie';
import Forgotpassword from './account/Forgotpassword';
import { useEffect } from 'react';

function App() {
  const token = Cookies.get('access_token');
  const location = useLocation();
  const isAuthenticated = !!token;

  useEffect(() => {
    if (isAuthenticated) {
      if (location.pathname === "/register" || location.pathname === "/forgetpassword") {
        return <Navigate to="/dashboard" />;
      }
    }
  }, [isAuthenticated, location.pathname]);

  return (
    <>
      {isAuthenticated && <Header />}
      {isAuthenticated && <Bot />}

      <Routes>
        <Route path="/" element={isAuthenticated ? <Navigate to="/dashboard" /> : <Login />} />
        <Route path="/register" element={isAuthenticated ? <Navigate to="/dashboard" /> : <Registration />} />
        <Route path="/forgetpassword" element={isAuthenticated ? <Navigate to="/dashboard" /> : <Forgotpassword />} />
        <Route path="/resetpassword" element={isAuthenticated ? <Navigate to="/dashboard" /> : <Forgotpassword />} />
        <Route path="/dashboard" element={isAuthenticated ? <Dashboard /> : <Navigate to="/" />} />
        <Route path="/search/:stock" element={isAuthenticated ? <Search /> : <Navigate to="/" />} />
        <Route path="/VolatilityDetails" element={isAuthenticated ? <VolatilityDetails /> : <Navigate to="/" />} />
        <Route path="/52-week-high-stocks" element={isAuthenticated ? <HignWeek52 /> : <Navigate to="/" />} />
        <Route path="/52-week-low-stocks" element={isAuthenticated ? <LowWeek52 /> : <Navigate to="/" />} />
        <Route path="/best-stocks-under-$10" element={isAuthenticated ? <UnderTendollar /> : <Navigate to="/" />} />
        <Route path="/best-stocks-under-$50" element={isAuthenticated ? <UnderFiftyDollar /> : <Navigate to="/" />} />
        <Route path="/top-trend" element={isAuthenticated ? <TopTrends /> : <Navigate to="/" />} />
        <Route path="/negative-beta" element={isAuthenticated ? <NegativeBeta /> : <Navigate to="/" />} />
        <Route path="/lowbeta" element={isAuthenticated ? <LowBeta /> : <Navigate to="/" />} />
        <Route path="/high-risk-high-reward" element={isAuthenticated ? <HighRishandReward /> : <Navigate to="/" />} />
        <Route path="/debitfree" element={isAuthenticated ? <DebitFree /> : <Navigate to="/" />} />
        <Route path="/dividend" element={isAuthenticated ? <Dividend /> : <Navigate to="/" />} />
        <Route path="/low-pe-ratio" element={isAuthenticated ? <LowPE /> : <Navigate to="/" />} />
        <Route path="/top-gain" element={isAuthenticated ? <TopGain /> : <Navigate to="/" />} />
        <Route path="/top-loss" element={isAuthenticated ? <TopLoss /> : <Navigate to="/" />} />
        <Route path="/top-perform" element={isAuthenticated ? <TopPerform /> : <Navigate to="/" />} />
        <Route path="/high-dividend" element={isAuthenticated ? <HighDividend /> : <Navigate to="/" />} />
      </Routes>

      {isAuthenticated && <Footer />}
    </>
  );
}

export default App;
