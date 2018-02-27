import React, {Component} from "react";
import ProfileHeader from "pages/Profile/Country/ProfileHeader";
import ProfileNav from "pages/Profile/Country/ProfileNav";
import ProfileSummary from "pages/Profile/Country/ProfileSummary";
import "pages/Profile/Profile.css";

export default class Country extends Component {

  render() {
    return (
      <div id="content">
        <ProfileHeader />
        <article className="intro-article">
          <section>
            <ProfileNav />
            <ProfileSummary />
          </section>
        </article>
        Sections...
      </div>
    );
  }

}
