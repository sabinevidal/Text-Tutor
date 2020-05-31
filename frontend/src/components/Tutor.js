import React, { Component } from 'react';
import '../stylesheets/Tutor.css';

class Tutor extends Component {
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
    const { name, phone, email, classes } = this.props;
    return (
      <div className="Tutor-holder">
        <div className="Name">{name}</div>
        <div className="Tutor-status">
          <div className="classes">Subjects: {classes}</div>
          <div className="phone">Phone: {phone}</div>
          <div className="email">Email: {email}</div>
          <img src="delete.png" className="delete" onClick={() => this.props.tutorAction('DELETE')}/>

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

export default Tutor;