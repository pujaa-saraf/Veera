import { useState } from 'react';
import './App.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import LandingPage from './Pages/LandingPage';
import SearchResult from './Pages/SearchResult';
import PdfDownloadComponent from './components/PdfDownloadComponent';
import Footer from './components/Footer';

function App() {

  const [query, setQuery] = useState("");
  const [search, setSearch] = useState(false);

  return (
    <div className='font-serif'>
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<LandingPage setQuery={setQuery} setSearch={setSearch} query={query} />} />
          <Route path='/search' element={<>
            <SearchResult setQuery={setQuery} setSearch={setSearch} query={query} search={search} />
            <PdfDownloadComponent />
            <Footer/>
          </>} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
