import React, {Component} from "react";
import Stat from "components/Stat";
import MapIcon from "components/MapIcon";
import "pages/Profile/Country/ProfileHeader.css";

export default class ProfileHeader extends Component {

  render() {
    const {country} = this.props;
    return (
      <div>
        <header className="profile_header country">

          {/* Background header image */}
          <div className="header_image">
            <img src={`/images/headers/country/${country.id}.jpg`} className="loaded" style={{width: "1187px", height: "548.987px", left: "0px", top: "-141.994px"}} />
          </div>

          {/* Country name and flag icon */}
          <div id="title">
            <img className="icon" src={`/images/icons/country/icon_${country.id}.png`} data-height="80" />
            <h1>{country.comtrade_name}</h1>
          </div>

          {/* Zoomed in map of country */}
          <div id="topojson">
            <MapIcon country={country} />
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
