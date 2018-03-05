import React, {Component} from "react";
import ProfileHeader from "pages/Profile/Product/ProfileHeader";
import ProfileNav from "pages/Profile/Product/ProfileNav";
import ProfileSummary from "pages/Profile/Product/ProfileSummary";
import SectionExporters from "pages/Profile/Product/sections/SectionExporters";
import SectionImporters from "pages/Profile/Product/sections/SectionImporters";
import ProfileFooter from "pages/Profile/Product/ProfileFooter";

export default class Product extends Component {

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
          <SectionExporters />
          <SectionImporters />
        </article>

        {/* links to other sites */}

        {/* links to the previous and next country */}
        <ProfileFooter />
        
      </div>
    );
  }

}
