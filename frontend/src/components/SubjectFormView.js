import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/SubjectFormView.css';

class SubjectFormView extends Component {
  constructor(props){
    super();
    this.state = {
      name: "",
      grade: ""
    }
  }

  submitSubject = (event) => {
    event.preventDefault();
    $.ajax({
      url: '/api/subjects',
      type: "POST",
      mode: 'CORS',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        name: this.state.name,
        grade: this.state.grade
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        document.getElementById("add-subject-form").reset();
        return;
      },
      error: (error) => {
        alert('Unable to add subject. Please try your request again')
        return;
      }
    })
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value})
  }

  render() {
    return (
      <div id="add-form">
        <h2>Add a New Subject</h2>
        <form className="form-view" id="add-subject-form" onSubmit={this.submitSubject}>
          <label>
            Name
            <input type="text" name="name" onChange={this.handleChange}/>
          </label>
          <label>
            Grade
            <select name="grade" onChange={this.handleChange}>
              <option value="7">7</option>
              <option value="8">8</option>
              <option value="9">9</option>
              <option value="10">10</option>
              <option value="11">11</option>
              <option value="12">12</option>
            </select>
          </label>
          {/* TODO Move this to TUTOR for Classes */}
          {/* <label>
            Category
            <select name="category" onChange={this.handleChange}>
              {Object.keys(this.state.categories).map(id => {
                  return (
                    <option key={id} value={id}>{this.state.categories[id]}</option>
                  )
                })}
            </select>
          </label> */}
          <input type="submit" className="button" value="Submit" />
        </form>
      </div>
    );
  }
}

export default SubjectFormView;
