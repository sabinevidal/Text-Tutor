import React, { Component } from 'react';
import logo from '../logo.svg';
import '../stylesheets/Header.css';

class Header extends Component {

  navTo(uri){
    window.location.href = window.location.origin + uri;
  }

  render() {
    return (
      <div className="App-header">
        <h1 onClick={() => {this.navTo('')}}>Text Tutor</h1>
        <h2 onClick={() => {this.navTo('/subjects')}}>Subject List</h2>
        <h2 onClick={() => {this.navTo('/tutors')}}>Tutor List</h2>
        <h2 onClick={() => {this.navTo('/addsubject')}}>Add Subject</h2>
        <h2 onClick={() => {this.navTo('/addtutor')}}>Add Tutor</h2>
      </div>
    );
  }
}

export default Header;
