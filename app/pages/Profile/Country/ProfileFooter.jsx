import React, {Component} from "react";
import "pages/Profile/Country/ProfileFooter.css";

export default class ProfileHeader extends Component {

  render() {
    return (
      <article>
        <section className="prof-nav">

          <a href="/en/profile/country/omn/" className="profile_header profile_button prev" style={{backgroundColor: "#c8140a", backgroundImage: "url('http://atlas.media.mit.edu/static/img/headers/country/asomn.jpg')"}}>
            <div className="button_cover"></div>
            <span className="pt-icon-standard pt-icon-chevron-left"></span>
            <h1>Oman</h1>
            <img className="icon" src="http://atlas.media.mit.edu/static/img/icons/country/country_asomn.png" />
          </a>

          <a href="/en/profile/country/phl/" className="profile_header profile_button next" style={{backgroundColor: "#c8140a", backgroundImage: "url('http://atlas.media.mit.edu/static/img/headers/country/asphl.jpg')"}}>
            <div className="button_cover"></div>
            <img className="icon" src="http://atlas.media.mit.edu/static/img/icons/country/country_asphl.png" />
            <h1>Philippines</h1>
            <i className="fa fa-angle-right"></i>
            <span className="pt-icon-standard pt-icon-chevron-right"></span>
          </a>

        </section>
      </article>
    );
  }

}
