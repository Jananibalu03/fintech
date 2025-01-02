import { Route, Routes } from 'react-router-dom';
import './App.css';
import Bot from './bot/Bot';
import Header from './layouts/header/Header';
import Footer from './layouts/footer/Footer';
import "bootstrap/dist/css/bootstrap.min.css";
import Dashboard from './components/search/Dashboard';
import Search from './components/search/Search';

function App() {
  return (
    <>
      <Header />
      <Bot />
      <Routes>
        <Route path='/dashboard' element={<Dashboard />} />
        <Route path='/search/:stock' element={<Search />} />
      </Routes>
      <Footer />
    </>
  );
}

export default App;
