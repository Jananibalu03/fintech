import { Route, Routes } from 'react-router-dom';
import './App.css';
import Bot from './bot/Bot';
import Header from './layouts/header/Header';
import Footer from './layouts/footer/Footer';
import "bootstrap/dist/css/bootstrap.min.css";
import Dashboard from './components/search/Dashboard';
import Search from './components/search/Search';
import TopTrend from './components/toptrend/TopTrend';
import VolatilityDetails from './components/toptrend/VolatilityDetails';
import HighWeeks52 from './components/toptrend/HighWeeks52';
import UnderFiveDollor from './components/toptrend/UnderFiveDollor';

function App() {
  return (
    <>
      <Header />
      <Bot />
      <Routes>
        <Route path='/dashboard' element={<Dashboard />} />
        <Route path='/search/:stock' element={<Search />} />
        <Route path='/top-trend' element={<TopTrend />} />
        <Route path='/VolatilityDetails' element={<VolatilityDetails/>}/>
        <Route path='/52-week-high-stocks' element={<HighWeeks52 />} />
        <Route path='/52-week-low-stocks' element={<HighWeeks52 />} />
        <Route path='/best-stocks-under-$5' element={<UnderFiveDollor />} />



      </Routes>
      <Footer />
    </>
  );
}

export default App;
