import React, {createContext, useContext, useState} from 'react';
import {AuthorizationApi} from "../api/AuthorizationApi";

export const AuthorizationContext = createContext();

const loadUserCredentials = () => {
  return JSON.parse(localStorage.getItem('userCredentials'));
}

export const AuthorizationProvider = ({ children }) => {
  const [userCredentials, setUserCredentials] = useState(loadUserCredentials());

  const signIn = (username, password) => {
    return AuthorizationApi.signin(username, password).then(
      (response) => {
        const userData = response.data;
        localStorage.setItem('userCredentials', JSON.stringify(userData));
        setUserCredentials(userData);
      }
    )
  }

  const signUp = (username, email, password) => {
    return AuthorizationApi.signup(username, email, password).then(
      (response) => {
        const userData = response.data;
        localStorage.setItem('userCredentials', JSON.stringify(userData));
        setUserCredentials(userData);
      }
    )
  }

  const resetCredentials = () => {
    localStorage.removeItem('userCredentials');
    setUserCredentials(undefined);
  }

  const value = {...userCredentials, signIn, signUp, resetCredentials};

  return (
    <AuthorizationContext.Provider value={value}>
      {children}
    </AuthorizationContext.Provider>
  );
};

export const useAuthorizationContext = () => useContext(AuthorizationContext);
