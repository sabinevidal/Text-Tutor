import React, { Component } from 'react';

import '../stylesheets/App.css';
import Tutor from './Tutor';
import $ from 'jquery';

class TutorView extends Component {
  constructor(){
    super();
    this.state = {
      tutors: [],
      page: 1,
      totalTutors: 0,
      subjects: {},
      currentSubject: null,
    }
  }

  componentDidMount() {
    this.getTutors();
  }

  getTutors = () => {
    $.ajax({
      url: `/tutors?page=${this.state.page}`, //TODO: update request URL
      type: "GET",
      mode: 'CORS',
      success: (result) => {
        this.setState({
          tutors: result.tutors,
          totalTutors: result.total_tutors,
          subjects: result.subjects,
          currentSubject: result.current_subject })
        return;
      },
      error: (error) => {
        alert('Unable to load tutors. Please try your request again')
        return;
      }
    })
  }

  selectPage(num) {
    this.setState({page: num}, () => this.getTutors());
  }

  createPagination(){
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalTutors / 10)
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => {this.selectPage(i)}}>{i}
        </span>)
    }
    return pageNumbers;
  }

  getBySubject= (id) => {
    $.ajax({
      url: `/subjects/${id}/tutors`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({
          tutors: result.tutors,
          totalTutors: result.total_tutors,
          currentSubject: result.current_subject })
        return;
      },
      error: (error) => {
        alert('Unable to load tutors. Please try your request again')
        return;
      }
    })
  }

  // submitSearch = (searchTerm) => {
  //   $.ajax({
  //     url: `/tutors/search`, //TODO: update request URL
  //     type: "POST",
  //     dataType: 'json',
  //     contentType: 'application/json',
  //     data: JSON.stringify({searchTerm: searchTerm}),
  //     xhrFields: {
  //       withCredentials: true
  //     },
  //     crossDomain: true,
  //     success: (result) => {
  //       this.setState({
  //         tutors: result.tutors,
  //         totalTutors: result.total_tutors,
  //         currentSubject: result.current_subject })
  //       return;
  //     },
  //     error: (error) => {
  //       alert('Unable to load tutors. Please try your request again')
  //       return;
  //     }
  //   })
  // }

  tutorAction = (id) => (action) => {
    if(action === 'DELETE') {
      if(window.confirm('are you sure you want to delete the tutor?')) {
        $.ajax({
          url: `/tutors/${id}`, //TODO: update request URL
          type: "DELETE",
          success: (result) => {
            this.getTutors();
          },
          error: (error) => {
            alert('Unable to load tutors. Please try your request again')
            return;
          }
        })
      }
    }
  }

  render() {
    return (
      <div className="tutor-view">
        <div className="subjects-list">
          <h2 onClick={() => {this.getTutors()}}>Subjects</h2>
          <ul>
            {Object.keys(this.state.subjects).map((id, ) => (
              <li key={id} onClick={() => {this.getBySubject(id)}}>
                {this.state.subjects[id]}
                <p className="subject">{this.state.subjects[id]}</p>
              </li>
            ))}
          </ul>
          {/* <Search submitSearch={this.submitSearch}/> */}
        </div>
        <div className="tutors-list">
          <h2>Tutors</h2>
          {this.state.tutors.map((t, ind) => (
            <Tutor
              key={t.id}
              name={t.name}
              phone={t.phone}
              email={t.email}
              classes={this.state.subjects[t.classes]}
              tutorAction={this.tutorAction(t.id)}
            />
          ))}
          <div className="pagination-menu">
            {this.createPagination()}
          </div>
        </div>

      </div>
    );
  }
}

export default TutorView;
