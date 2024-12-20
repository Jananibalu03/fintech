
import { Route, Routes } from 'react-router-dom'
import './App.css'
import Bot from './bot/Bot'

function App() {

  return (
    <>

      <Routes>
        <Route path='/bot' element={<Bot />} />
      </Routes>

    </>
  )
}

export default App
