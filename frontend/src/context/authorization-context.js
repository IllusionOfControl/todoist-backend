import React, {createContext, useContext, useEffect, useState} from 'react';
import {AuthorizationApi} from "../api/AuthorizationApi";

export const AuthorizationContext = createContext();
export const AuthorizationProvider = ({ children }) => {
  const [userCredentials, setUserCredentials] = useState(() => JSON.parse(localStorage.getItem('userCredentials')));

  const signIn = (username, password) => {
    return AuthorizationApi.signin(username, password).then(
      (response) => {
        const userData = response.data;
        localStorage.setItem('userCredentials', JSON.stringify(userData));
        setUserCredentials(userData);
      }
    )
  }

  const signUp = (username, password) => {
    return AuthorizationApi.signup(username, password).then(
      (response) => {
        const userData = response.data;
        setUserCredentials(userData);
      }
    )
  }

  const clearCredentials = () => {
    localStorage.removeItem('userCredentials');
    setUserCredentials(undefined);
  }

  const value = {userCredentials, signIn, signUp, clearCredentials}

  return (
    <AuthorizationContext.Provider value={value}>
      {children}
    </AuthorizationContext.Provider>
  );
};

export const useAuthorizationContext = () => useContext(AuthorizationContext);
