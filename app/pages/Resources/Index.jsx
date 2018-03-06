import React, {Component} from "react";
import "pages/Resources/Resources.css";

export default class Resources extends Component {

  render() {
    const {children} = this.props;
    return (
      <div id="content" className="resources">
        <section>
          {children}
        </section>
      </div>
    );
  }

}
