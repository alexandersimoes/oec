import React, {Component} from "react";
import ProfileHeader from "pages/Profile/Country/ProfileHeader";
import ProfileNav from "pages/Profile/Country/ProfileNav";
import ProfileSummary from "pages/Profile/Country/ProfileSummary";
import SectionExports from "pages/Profile/Country/sections/SectionExports";
import SectionImports from "pages/Profile/Country/sections/SectionImports";
import SectionTradeBalance from "pages/Profile/Country/sections/SectionTradeBalance";
import SectionDestinations from "pages/Profile/Country/sections/SectionDestinations";
import SectionOrigins from "pages/Profile/Country/sections/SectionOrigins";
import SectionProductSpace from "pages/Profile/Country/sections/SectionProductSpace";
import SectionPgiSpace from "pages/Profile/Country/sections/SectionPgiSpace";
import SectionEciRanking from "pages/Profile/Country/sections/SectionEciRanking";
import ProfileFooter from "pages/Profile/Country/ProfileFooter";
import "pages/Profile/Profile.css";

export default class Country extends Component {

  render() {
    return (
      <div id="content">

        {/* this includes header image, name and sparkline stats */}
        <ProfileHeader />

        {/* text intro section (with page navigation and summary text) */}
        <article className="intro-article">
          <section>
            <ProfileNav />
            <ProfileSummary />
          </section>
        </article>

        {/* simple visualizations sections */}
        <article className="viz-article">
          <SectionExports />
          <SectionImports />
          <SectionTradeBalance />
          <SectionDestinations />
          <SectionOrigins />
        </article>

        {/* economic complexity sections (product space etc...) */}
        <article className="viz-article">
          <h1>Economic Complexity of Pakistan</h1>
          <SectionProductSpace />
          <SectionPgiSpace />
          <SectionEciRanking />
        </article>

        {/* links to other sites */}

        {/* links to the previous and next country */}
        <ProfileFooter />

      </div>
    );
  }

}
