import React, {useEffect, useState} from 'react';
import {Link, useNavigate} from "react-router-dom";
import {useAuthorizationContext} from "../context";
import {useInput} from "../hooks"


const defaultValidate = (value) => {
  return value.length <= 3;
}

export const SignInPage = () => {
  const [username, usernameHandle, usernameError] = useInput("", defaultValidate)
  const [password, passwordHandle, passwordError] = useInput("",  defaultValidate)
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const auth = useAuthorizationContext();

  const handleSubmit = (event) => {
    if (!(usernameError || passwordError)) {
      auth.signIn(username, password).then(() => {navigate("/")}).catch((error) => {
        if (error.response) {
          setError(error.response.data.detail);
        }
      })
    }
    event.preventDefault();
  }

  return (
    <section className="auth-section">
      <form onSubmit={handleSubmit}>
        <h2>Log-in Page</h2>
        <label htmlFor="username">username</label>
        <input className={usernameError ? "invalid": ""} type="text" onChange={usernameHandle}/>
        <label htmlFor="password">password</label>
        <input className={passwordError ? "invalid": ""} type="password" onChange={passwordHandle}/>
        { error && <p>{error}</p>}
        <button className="#">login</button>
        <div>
          <Link to={"/registration"}>Sign up</Link>
        </div>
      </form>
    </section>
  );
};
