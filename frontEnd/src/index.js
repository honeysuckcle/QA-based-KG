import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import Home from './Home';
import Admin from './Admin';
import reportWebVitals from './reportWebVitals';
import {Route, BrowserRouter as Router, Switch} from 'react-router-dom';

const routing = (
    <Router>
            <Switch>
                <Route exact path="/" component={Home} />
                <Route path="/user" component={App} />
                <Route path="/admin" component={Admin} />
            </Switch>
    </Router>
);

ReactDOM.render(
  routing,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
