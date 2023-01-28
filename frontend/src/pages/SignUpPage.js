import React, { useState } from 'react';
import {Link, useNavigate} from "react-router-dom";
import {useAuthorizationContext} from "../context";


export const SignUpPage = () => {
  const [username, setUsername] = useState();
  const [email, setEmail] = useState();
  const [password, setPassword] = useState();
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const auth = useAuthorizationContext();

  const handleSubmit = (event) => {
    auth.signUp(username, email, password).then(() => navigate("/")).catch((error) => {
      if (error.response) {
        setError(error.response.data.detail);
      }
    })
    event.preventDefault();
  }

  return (
    <section className="login">
      <h2 className="title">Sign up Page</h2>
      <form onSubmit={handleSubmit}>
        { error ? <h3>{error}</h3> : ""}

        <label htmlFor="username">username</label>
        <input type="text" onChange={(e) => setUsername(e.target.value)}/>
        <label htmlFor="password">email</label>
        <input type="text" onChange={(e) => setEmail(e.target.value)}/>
        <label htmlFor="password">password</label>
        <input type="text" onChange={(e) => setPassword(e.target.value)}/>
        <button className="#">Registration</button>
        <div>
          <a href="#" target="_blank" rel="noopener">Forgot password</a>
          <span>/</span>
          <Link to={"/login"}>Sign in</Link>
        </div>
      </form>
    </section>
  );
};
