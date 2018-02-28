import React, {Component} from "react";

export default class Profile extends Component {

  render() {
    const {children} = this.props;
    return (
      <div>
        {children}
      </div>
    );
  }

}
