import axios from 'axios';
import React, { useEffect, useState } from 'react'
import searchData from '../data.json';
import LlamaAI from 'llamaai';


export default function SearchResult({ setSearch, setQuery, query, search }) {
    const [results, setResults] = useState(null);
    const [updatedQuery, setUpdatedQuery] = useState(null);
    const [summary, setSummary] = useState(null);
    const [Loading, setLoading] = useState(false);

    const API_KEY = process.env.REACT_APP_API_KEY
    const cx = process.env.REACT_APP_CX

    const handleSearch = () => {
        if (query.length > 0) {
            setSearch(true);
        }
    }

    const handleSearchInput = (event) => {
        setQuery(event.target.value)
        setSearch(false)
    }

    useEffect(() => {

        // const fetchOpenAIResponse = async () => {
        //     const llamaAPI = new LlamaAI();
        //     const apiRequestJson = {
        //         "messages": [
        //             {"role": "system", "content": "I will provide you with a search query taken from a user. Provide me a better version of the query which I could use to find most relevant results. Your answer should contain only the rephrased query."},
        //             {"role": "user", "content": query}
        //         ],
        //         "functions": [],
        //         "stream": false,
        //     };
        //     llamaAPI.run(apiRequestJson)
        //         .then(response => {
        //             console.log(response)
        //             setUpdatedQuery(response.data.choices[0].message.content);
        //         })
        //         .catch(error => {
        //             setUpdatedQuery(query)
        //         });
        // };

        if (search) {
                axios.get(`https://www.googleapis.com/customsearch/v1?key=${API_KEY}&cx=${cx}&q=${query}&gl=in`).then((res) => {
                    setResults(res.data.items);
                    console.log(res.data)
                    // fetchOpenAIResponse();
                    return axios.post('http://127.0.0.1:8000/summarize/', {search_query:query, input_params:res.data.items.map(item => ({ snippet: item.snippet, link: item.link }))})
                }).then((res)=>{
                    setSummary(res.data)
                    console.log(res.data);
                })
                .catch((e) => console.log(e))

            // axios.get("https://serpapi.com/search.json", {
            //         params: {
            //             engine: "google",
            //             q: "Coffee",
            //             api_key: REACT_APP_API_KEY_SERP
            //         }
            //     }).then((res)=>{
            //     setResults(res.data.organic_results)
            //     console.log(res.data.organic_results)
            // }).catch((e)=>console.log(e))
        }
    }, [search, query])

    // useEffect(()=>{
    //     if(results){
    //         const body=;
    //         axios.post('http://127.0.0.1:8000/summarize/', {search_query:query, input_params:body}).then((res)=>{
    //             setSummary(res.data)
    //             console.log(res.data);
    //         }).catch((e) => console.log(e))
    //     }
    // },[results])

    return (
        <div>
            <div className='bg-gradient-to-r from-[#5de0e6] to-[#004aad]'>
                <div className='w-[90%] mx-auto pt-12 pb-12'>
                    <h1 className='text-4xl mt-2 text-4xl md:text-5xl font-bold text-white text-center'>Insight AI</h1>
                    <div className="w-[90%] mx-auto mt-12 md:mt-14 flex flex-row items-center bg-gradient-to-r from-[#a6a6a6] to-[#fff] justify-between p-0.5 rounded-lg">
                        <input
                            className="w-[100%] px-4 py-3 md:px-6 md:py-4 text-xl focus:outline-none rounded-l-lg"
                            placeholder="Search..."
                            value={query}
                            onChange={handleSearchInput}
                        />
                        <button onClick={handleSearch}><i className="fa-solid fa-magnifying-glass px-6 text-[#004aad] text-3xl"></i></button>
                    </div>
                </div>
            </div>
            {summary && 
            <div className='w-[90%] mt-14 mx-auto md:grid md:grid-cols-5 justify-center' id="search_result">
                <div className='md:col-span-3 text-xl text-slate-500 md:border-4 md:border-white md:border-r-[#94b9ff]'>
                    <div className='md:w-[90%] mx-auto'>
                        <p className='mb-4'>Here are some insights about your search - <span>{query}</span></p>
                        <p className='text-lg'>{summary}</p>
                    </div>
                </div>
                <div className='md:col-span-2 mt-8 md:mt-0 w-[90%] md:w-[85%] mx-auto'>
                    <h1 className='text-blue-500 font-bold text-xl mb-4'>Sources:</h1>
                    <div className='flex flex-col gap-5'>
                        {results?.items?.map((item, key) => {
                            return <a key={key} className='cursor-pointer' href={item.link} target='blank'>
                                <p className='text-md text-'>{item.title}</p>
                                <p className='text-sm text-blue-500'>{item.link}</p>
                            </a>
                        })}
                    </div>
                </div>
            </div>
            }
        </div>
    )
}
