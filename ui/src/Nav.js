import React from "react";
import "./Nav.css";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function Nav() {
  const [show, handleShow] = useState(false);

  useEffect(() => {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 100) handleShow(true);
      else handleShow(false);
    });
    return () => {
      // window.removeEventListener("scroll");
    };
  }, []);

  return (
    <div className={`nav__container ${show && "nav__black"}`}>
      <img
        className="nav__logo"
        src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Netflix_2015_logo.svg/1200px-Netflix_2015_logo.svg.png"
        alt="Netflix Logo"
      />
      <img
        className="nav__avatar"
        src="https://upload.wikimedia.org/wikipedia/commons/0/0b/Netflix-avatar.png"
        alt="User Logo"
      />

      <span className="App-header first-link">
        <span className="links">
          <Link to="/">Dashboard_User</Link>
        </span>
        <span className="links">
          <Link to="/about">Dashboard_Item</Link>
        </span>
      </span>
    </div>
  );
}

export default Nav;
