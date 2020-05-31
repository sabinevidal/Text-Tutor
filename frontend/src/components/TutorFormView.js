import React, { Component } from 'react';
import Select from 'react-select';
import {availableClasses} from '../api.js';
import $ from 'jquery';
import axios  from 'axios';

import '../stylesheets/TutorFormView.css';

class TutorFormView extends Component {
  constructor(props){
    super(props);
    this.state = {
      name: "",
      phone: null,
      email: "",
      classes: "",
      subjects: [],
    }
  }

  componentDidMount(){
    // $.ajax({
    //   url: `/api/subjects`,
    //   type: "GET",
    //   success: (result) => {
    //     this.setState({ subjects: result.subjects })
    //     return { value: subject.grade, label: subject.name };
    //   },
    //   error: (error) => {
    //     alert('Unable to load subjects. Please try your request again')
    //     return;
    //   }
    // });
    // availableClasses()
    //   .then(response => {
    //     this.setState({
    //       subjects: response.Subject
    //     })
    //     console.log("hello", this.state.subjects)
    //   });
    // axios.get(`/api/subjects`)
    //   .then(res => {
    //     const subjects = res.data;
    //     this.setState({subjects: subjects.subject})
    //     console.log(this.state.subjects)
    //     return { value: subject.grade, label: subject.name };
    //   })
    this.fetchSubjects()
  }

  fetchSubjects() {
    fetch(`/api/subjects`)
      .then(response => response.json())
      .then(data => this.setState({ subjects: data }));
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

  // getSubjects = (input) => {
  //   return this.props.subjects
  //     .then((response) => {
  //       return response.json();
  //     }).then((json) => {
  //       return { objects: json };
  //     });
  // }

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

  // let printClasses = arrayOfClasses.map(opt => ({ label: opt, value: opt }));

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
  // TODO: carry on looking at
  // https://stackoverflow.com/questions/47672117/react-select-how-to-show-iterate-through-data-from-api-call-in-option-instea

  render() {
    // let classes = this.state.subjects.map((c, i) => key={i}, value={c});
    //   // return { value: subject.grade, label: subject.name };
    const {subjects} = this.state;
    const { name, grade } = subject;
    let classes = this.state.subjects.map(subjects => (
      <p key={subject.id}>grade: {subject.grade} name: {subject.name} </p>

    ))
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
            {/* <select name="classes" onChange={this.handleChange}>
              {Object.values(this.state.subjects).map(id => {
                  return (
                    <option key={id} value={id}>{this.state.subjects[id]}</option>
                  )
                })}
            </select> */}
            <Select options={classes} />
          </label>
          <input type="submit" className="button" value="Submit" />
        </form>
      </div>
    );
  }
}

export default TutorFormView;
