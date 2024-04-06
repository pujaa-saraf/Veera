import React from 'react'
import { useNavigate } from 'react-router-dom';

export default function LandingPage({setSearch, setQuery, query}) {
    const navigate = useNavigate();

    const handleSearch = () => {
        if (query.length > 0) {
            setSearch(true);
            navigate('/search')
        }
    }

    const handleSearchInput = (event) => {
        setQuery(event.target.value)
        setSearch(false)
    }
  return (
    <div className='w-[100%] bg-gradient-to-r from-[#5de0e6] to-[#004aad] h-[100vh] flex flex-col justify-center items-center'>
        <div className='w-[90%] mx-auto pt-12 pb-12'>
          <h1 className='text-4xl text-6xl font-bold text-white text-center'>Insight AI</h1>
          <p className='text-xl text-white text-center mt-8 md:w-[30rem] mx-auto'>Discover smarter search with AI integration, get personalized results tailored just for you.</p>
          <div className="w-[90%] mx-auto mt-12 flex flex-row items-center bg-gradient-to-r from-blue-500 via-purple-500 to-blue-500 justify-between p-1 rounded-xl">
            <input
                className="w-[100%] px-6 py-4 text-xl focus:outline-none rounded-l-lg"
                placeholder="Search..."
                value={query}
                onChange={handleSearchInput}
            />
            <button onClick={handleSearch}><i className="fa-solid fa-magnifying-glass px-6 text-white text-3xl"></i></button>
        </div>
        </div>
    </div>
  )
}
