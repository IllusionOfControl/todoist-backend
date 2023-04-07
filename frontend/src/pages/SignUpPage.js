import {useState} from 'react';
import {Link, useNavigate} from "react-router-dom";
import {useAuthorizationContext} from "../context";
import {useInput} from "../hooks";

const defaultValidate = (value) => {
  return value.length <= 3;
}

const emailValidate = (value) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return !emailRegex.test(value);
}

export const SignUpPage = () => {
  const [username, usernameHandle, usernameError] = useInput("", defaultValidate)
  const [email, emailHandle, emailError] = useInput("", emailValidate)
  const [password, passwordHandle, passwordError] = useInput("",  defaultValidate)
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const auth = useAuthorizationContext();

  const handleSubmit = (event) => {
    if (!(usernameError || passwordError)) {
      auth.signUp(username, email, password).then(() => {navigate("/")}).catch((error) => {
        if (error.response) {
          setError(error.response.data.detail);
        }
      })
      event.preventDefault();
    }
  }

  return (
    <>
      <header className="header" data-testid="header">
        <nav>
          <div className="logo">
            <img src="/images/logo.png" alt="Todoist" />
          </div>
        </nav>
      </header>

      <section className="auth-section">
        <form onSubmit={handleSubmit}>
          <h2>Sign up Page</h2>
          <label htmlFor="username">username</label>
          <input className={usernameError && "invalid"} type="text" onChange={usernameHandle}/>
          <label htmlFor="username">email</label>
          <input className={emailError && "invalid"} type="email" onChange={emailHandle}/>
          <label htmlFor="password">password</label>
          <input className={passwordError && "invalid"} type="password" onChange={passwordHandle}/>
          { error ? <h3>{error}</h3> : ""}
          <button className="#">Registration</button>
          <div>
            <Link to={"/login"}>Sign in</Link>
          </div>
        </form>
      </section>
    </>
  );
};
