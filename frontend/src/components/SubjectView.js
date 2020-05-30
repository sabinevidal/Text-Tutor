import React, { Component } from 'react';

import '../stylesheets/App.css';
import Subject from './Subject';
import $ from 'jquery';

class SubjectView extends Component {
  constructor(){
    super();
    this.state = {
      subjects: [],
    }
  }

  componentDidMount() {
    this.getSubjects();
  }

  getSubjects = () => {
    $.ajax({
      url: `/subjects`, //TODO: update request URL
      type: "GET",
      mode: 'CORS',
      success: (result) => {
        this.setState({
          subjects: result.subjects,
          totalSubjects: result.total_subjects,
 })
        return;
      },
      error: (error) => {
        alert('Unable to load subjects. Please try your request again')
        return;
      }
    })
  }

  // selectPage(num) {
  //   this.setState({page: num}, () => this.getTutors());
  // }

  // createPagination(){
  //   let pageNumbers = [];
  //   let maxPage = Math.ceil(this.state.totalTutors / 10)
  //   for (let i = 1; i <= maxPage; i++) {
  //     pageNumbers.push(
  //       <span
  //         key={i}
  //         className={`page-num ${i === this.state.page ? 'active' : ''}`}
  //         onClick={() => {this.selectPage(i)}}>{i}
  //       </span>)
  //   }
  //   return pageNumbers;
  // }

  // getBySubject= (id) => {
  //   $.ajax({
  //     url: `/subjects/${id}/subjects`, //TODO: update request URL
  //     type: "GET",
  //     success: (result) => {
  //       this.setState({
  //         subjects: result.subjects,
  //         totalSubjects: result.total_subjects,
  //         currentSubject: result.current_subject })
  //       return;
  //     },
  //     error: (error) => {
  //       alert('Unable to load subjects. Please try your request again')
  //       return;
  //     }
  //   })
  // }

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

  subjectAction = (id) => (action) => {
    if(action === 'DELETE') {
      if(window.confirm('are you sure you want to delete the subject?')) {
        $.ajax({
          url: `/subjects/${id}`, //TODO: update request URL
          type: "DELETE",
          success: (result) => {
            this.getSubjects();
          },
          error: (error) => {
            alert('Unable to load subjects. Please try your request again')
            return;
          }
        })
      }
    }
  }

  render() {
    return (
      <div className="subject-view">
        <div className="subjects-list">
          <h2>Subjects</h2>
          {/* <ul>
            {Object.keys(this.state.subjects).map((id, ) => (
              <li key={id} onClick={() => {this.getBySubject(id)}}>
                {this.state.subjects[id]}
                <p className="subject">{this.state.subjects[id]}</p>
              </li>
            ))}
          </ul>
          {/* <Search submitSearch={this.submitSearch}/> 
        </div>
        <div className="subjects-list"> */}
          <h2>Subjects</h2>
          {this.state.subjects.map((t, ind) => (
            <Subject
              key={t.id}
              name={t.name}
              grade={t.grade}
              subjectAction={this.subjectAction(t.id)}
            />
          ))}
        </div>

      </div>
    );
  }
}

export default SubjectView;
