import React from "react";
import { useState, useEffect } from "react";
import instance from "./axios.js";
import "./Row.css";

const BASE_URL = "https://image.tmdb.org/t/p/original";

function Row(props) {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    async function fetchData(url) {
      try {
        const response = await instance.get(url);
        // console.log(response);
        setMovies(response.data.results);
      } catch (error) {
        console.log(error);
      }
    }
    fetchData(props.fetchURL);
  }, [props.fetchURL]);

  return (
    <div className={`row-container ${props.title}`}>
      <h2 class="prop-name">{props.title}</h2>

      <div className="row__posters">
        {movies.map((movie) => (
          <img
            key={movie.id}
            className={`row__poster ${
              props.isLargeRow ? "largeRow__poster" : ""
            }`}
            src={`${BASE_URL}${
              props.isLargeRow ? movie.poster_path : movie.backdrop_path
            }`}
            alt={`${movie.original_title}`}
          />
        ))}
      </div>
    </div>
  );
}

export default Row;
