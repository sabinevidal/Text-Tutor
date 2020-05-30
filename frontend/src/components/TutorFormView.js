import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/TutorFormView.css';

class TutorFormView extends Component {
  constructor(props){
    super();
    this.state = {
      name: "",
      phone: null,
      email: "",
      classes: {},
      subjects: {}
    }
  }

  componentDidMount(){
    $.ajax({
      url: `/api/subjects`,
      type: "GET",
      success: (result) => {
        this.setState({ subjects: result.subjects })
        return;
      },
      error: (error) => {
        alert('Unable to load subjects. Please try your request again')
        return;
      }
    })
  }


  submitTutor = (event) => {
    event.preventDefault();
    $.ajax({
      url: '/api/tutors',
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        name: this.state.name,
        phone: this.state.phone,
        email: this.state.email,
        classes: this.state.classes
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        document.getElementById("add-tutor-form").reset();
        return;
      },
      error: (error) => {
        alert('Unable to add tutor. Please try your request again')
        return;
      }
    })
  }

  getSubjects = (input) => {
    return this.props.subjects
      .then((response) => {
        return response.json();
      }).then((json) => {
        return { objects: json };
      });
  }

  // renderFields() {
  //   return _.map(formField, ({ label, name}) => (
  //     <Field
  //       key={id}
  //       component={SubjectView}
  //       type="text"
  //       label={label}
  //       name={name}
  //       />
  //   ));
  // }

  handleChange = (event) => {
    let name = event.target.name;
    let value = event.target.value;
    if (name === 'phone') {
      if (!Number(value)) {
        alert("Your phone must be a number")
      }
    }
    this.setState({[name]: value})
  }

  render() {
    return (
      <div id="add-form">
        <h2>Add a New Tutor</h2>
        <form className="form-view" id="add-tutor-form" onSubmit={this.submitTutor}>
          <label>
            Name
            <input type="text" name="name" onChange={this.handleChange}/>
          </label>
          <label>
            Phone
            <input type="text" name="phone" onChange={this.handleChange}/>
          </label>
          <label>
            Email
            <input type="text" name="email" onChange={this.handleChange}/>
          </label>
          <label>
            Subjects
            <select name="classes" onChange={this.handleChange}>
              {Object.values(this.state.subjects).map(id => {
                  return (
                    <option key={id} value={id}>{this.state.subjects[id]}</option>
                  )
                })}
            </select>
          </label>
          <input type="submit" className="button" value="Submit" />
        </form>
      </div>
    );
  }
}

export default TutorFormView;
