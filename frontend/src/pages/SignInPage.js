import React, { useState } from 'react';
import {Link, useNavigate} from "react-router-dom";
// import style from "./login.css"
import {useAuthorizationContext} from "../context/authorization-context";


export const SignInPage = () => {
  const [username, setUsername] = useState();
  const [password, setPassword] = useState();
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const auth = useAuthorizationContext();

  const handleSubmit = (event) => {
    auth.signIn(username, password).then(() => navigate("/")).catch((error) => {
      if (error.response) {
        setError(error.response.data.detail);
      }
    })
    event.preventDefault();
  }

  return (
    <section className="login">
      <h2 className="title">Log-in / Sign up Page</h2>
      <form onSubmit={handleSubmit}>
        { error ? <h3>{error}</h3> : ""}

        <label htmlFor="username">username or email</label>
        <input type="text" onChange={(e) => setUsername(e.target.value)}/>
        <label htmlFor="password">password</label>
        <input type="text" onChange={(e) => setPassword(e.target.value)}/>
        <button className="#">login</button>
        <div>
          <a href="#" target="_blank" rel="noopener">forgot password</a>
          <span>/</span>
          <Link to={"/registration"}>aaa</Link>
        </div>
      </form>
    </section>
  );
};
