import React, {Component} from "react";
import {connect} from "react-redux";
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
import mondrianClient from "helpers/mondrian";
import countries from "data/attr_country.json";
import "pages/Profile/Profile.css";

class Country extends Component {

  componentDidMount() {
  }

  render() {
    const {data, params} = this.props;
    const {id: countryId} = params;
    const country = countries.find(c => c.id === countryId);

    if (!Object.keys(data).length) {
      return <div className="message-container fullscreen">
        <span className="message is-error">Loading country data...</span>
      </div>;
    }

    const {countryProfile} = data;
    const tradeByCountry = countryProfile.find(d => d ? d.key === "tradeByCountry" : null).data;
    console.log("countryProfile", countryProfile);
    console.log("tradeByCountry", tradeByCountry);

    return (
      <div id="content">

        {/* this includes header image, name and sparkline stats */}
        <ProfileHeader country={country} />

        {/* text intro section (with page navigation and summary text) */}
        <article className="intro-article">
          <section>
            <ProfileNav />
            <ProfileSummary country={country} tradeByCountry={tradeByCountry} />
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

Country.need = [
  params => {
    const {id} = params;
    console.log("Country Need ID!", id);

    const prmTradeByCountry = mondrianClient
      .cube("2015_2016_hs_rev2007_yearly_data")
      .then(cube => {
        const qry = cube.query
          .drilldown("Origin Country", "Countries", "Country")
          .measure("Exports")
          .measure("Imports")
          .cut("[year].[year].[year].&[2016]");
        return mondrianClient.query(qry, "jsonrecords");
      })
      .then(res => ({
        key: "tradeByCountry",
        data: res.data.data
      }));

    const prmAll = Promise.all([prmTradeByCountry]).then(values => ({
      key: "countryProfile",
      data: values
    }));

    return {
      type: "GET_DATA",
      promise: prmAll
    };
  }
];

export default connect(state => ({
  data: state.data
}))(Country);
