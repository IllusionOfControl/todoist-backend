import React from 'react';
import {render} from 'react-dom';
import {App} from './App';
import {AuthorizationProvider, ThemeProvider} from "./context";
import './App.scss';

render(
  <React.StrictMode>
    <ThemeProvider>
      <AuthorizationProvider>
        <App/>
      </AuthorizationProvider>
    </ThemeProvider>
  </React.StrictMode>,
  document.getElementById('root')
);
