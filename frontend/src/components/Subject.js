import React, { Component } from 'react';
import '../stylesheets/Subject.css';

class Subject extends Component {
  // constructor(){
  //   super();
  //   this.state = {
  //     visibleDetails: false
  //   }
  // }

  // flipVisibility() {
  //   this.setState({visibleAnswer: !this.state.visibleAnswer});
  // }

  render() {
    const { name, grade } = this.props;
    return (
      <div className="Subject-holder">
        <div className="Name">{name}</div>
        <div className="Subject-status">
          <div className="grade">Grade: {grade}</div>
          <img src="delete.png" className="delete" onClick={() => this.props.subjectAction('DELETE')}/>

        </div>
        {/* <div className="show-answer button"
            onClick={() => this.flipVisibility()}>
            {this.state.visibleAnswer ? 'Hide' : 'Show'} Answer
          </div>
        <div className="answer-holder">
          <span style={{"visibility": this.state.visibleAnswer ? 'visible' : 'hidden'}}>Answer: {answer}</span>
        </div> */}
      </div>
    );
  }
}

export default Subject;
