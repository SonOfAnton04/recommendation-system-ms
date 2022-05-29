import React from "react";
import "./Row.css";
import requests from "./requests";
import "./Banner.css";
import Banner from "./Banner";
import Row from "./Row";

function DashboardUser(props) {
  return (
    <div>
      <Banner />
      <Row
        title="Trending"
        fetchURL={requests.fetchTrending}
        isLargeRow={true}
      />
      <Row title="Top Rated" fetchURL={requests.fetchTopRated} />
      <Row title="Action" fetchURL={requests.fetchActionMovies} />
      <Row title="Comedy" fetchURL={requests.fetchComedyMovies} />
      <Row title="Horror" fetchURL={requests.fetchHorrorMovies} />
      <Row title="Romance" fetchURL={requests.fetchRomanceMovies} />
      <Row title="Documentaries" fetchURL={requests.fetchDocumentaries} />
    </div>
  );
}

export default DashboardUser;
