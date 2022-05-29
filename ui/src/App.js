import "./App.css";
import requests from "./requests.js";
import Row from "./Row.js";
import Banner from "./Banner.js";
import Nav from "./Nav.js";

function App() {
  return (
    <div className="App">
      <Nav />
      <Banner />
      <Row
        title="Trending"
        fetchURL={requests.fetchTrending}
        isLargeRow={true}
      />
      {/* <Row
          title="Netflix Originals"
          fetchURL={requests.fetchNetflixOriginals}
        /> */}
      <Row title="Top Rated" fetchURL={requests.fetchTopRated} />
      <Row title="Action" fetchURL={requests.fetchActionMovies} />
      <Row title="Comedy" fetchURL={requests.fetchComedyMovies} />
      <Row title="Horror" fetchURL={requests.fetchHorrorMovies} />
      <Row title="Romance" fetchURL={requests.fetchRomanceMovies} />
      <Row title="Documentaries" fetchURL={requests.fetchDocumentaries} />
    </div>
  );
}

export default App;
