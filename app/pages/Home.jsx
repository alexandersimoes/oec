import React, {Component} from "react";
import {translate} from "react-i18next";
import "./Home.css";

class Home extends Component {

  render() {
    const {t} = this.props;

    return (
      <div id="Home">
        {t("Welcome to the OEC!")}
      </div>
    );
  }

}

export default translate()(Home);
