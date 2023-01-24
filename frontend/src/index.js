import React from 'react';
import {render} from 'react-dom';
import {App} from './App';
import {AuthorizationProvider, ThemeProvider} from "./context";
import './App.scss';

render(
  <ThemeProvider>
    <AuthorizationProvider>
      <App/>
    </AuthorizationProvider>
  </ThemeProvider>,
  document.getElementById('root')
);
