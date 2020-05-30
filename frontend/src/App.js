import React, { Component } from 'react';
import {
  BrowserRouter as Router,
  Route,
  Switch
} from 'react-router-dom'

// import logo from './logo.svg';
import './stylesheets/App.css';
import SubjectFormView from './components/SubjectFormView';
import TutorFormView from './components/TutorFormView';
import TutorView from './components/TutorView';
import Header from './components/Header';
import SubjectView from './components/SubjectView';


class App extends Component {
  render() {
    return (
    <div className="App">
      <Header path />
      <Router>
        <Switch>
          <Route path="/" exact component={SubjectView} />
          <Route path="/addsubject" component={SubjectFormView} />
          <Route path="/addtutor" component={TutorFormView} />
          <Route path="/tutors" component={TutorView} />
          <Route path="/subjects" component={SubjectView} />
        </Switch>
      </Router>
    </div>
  );

  }
}

export default App;
