import { Route, Routes } from 'react-router-dom';
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

function App() {
  return (
    <>
      <Header />
      <Bot />
      <Routes>
        <Route path='/dashboard' element={<Dashboard />} />
        <Route path='/search/:stock' element={<Search />} />
        <Route path='/VolatilityDetails' element={<VolatilityDetails />} />
        <Route path='/52-week-high-stocks' element={<HignWeek52 />} />
        <Route path='/52-week-low-stocks' element={<LowWeek52 />} />
        <Route path='/best-stocks-under-$10' element={<UnderTendollar />} />
        <Route path='/best-stocks-under-$50' element={<UnderFiftyDollar />} />
        <Route path='/top-trend' element={<TopTrends/>}/>
        <Route path='/negative-beta' element={<NegativeBeta />} />
        <Route path='/lowbeta' element={<LowBeta />} />
        <Route path='/high-risk-high-reward' element={<HighRishandReward />} />
        <Route path='/debitfree' element={<DebitFree />} />
        <Route path='/dividend' element={<Dividend />} />
        <Route path='/low-pe-ratio' element={<LowPE />} />
        <Route path='/top-gain' element={<TopGain />} />
        <Route path='/top-loss' element={<TopLoss />} />
        <Route path='/top-perform' element={<TopPerform />} />
        <Route path='/high-dividend' element={<HighDividend />} />

      </Routes>
      <Footer />
    </>
  );
}

export default App;
