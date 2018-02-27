import React, {Component} from "react";
import Stat from "components/Stat";
import MapIcon from "components/MapIcon";
import "pages/Profile/Country/ProfileHeader.css";

export default class ProfileHeader extends Component {

  render() {
    return (
      <div>
        <header className="profile_header country">

          {/* Background header image */}
          <div className="header_image">
            <img src="http://atlas.media.mit.edu/static/img/headers/country/aspak.jpg" className="loaded" style={{width: "1187px", height: "548.987px", left: "0px", top: "-141.994px"}} />
          </div>

          {/* Country name and flag icon */}
          <div id="title">
            <img className="icon" src="http://atlas.media.mit.edu/static/img/icons/country/country_aspak.png" data-height="80" />
            <h1>Pakistan</h1>
          </div>

          {/* Zoomed in map of country */}
          <div id="topojson">
            <MapIcon />
          </div>

          {/* Header sparkline stats */}
          <div id="stats">
            <Stat />
            <Stat />
            <Stat />
          </div>
        </header>
      </div>
    );
  }

}
