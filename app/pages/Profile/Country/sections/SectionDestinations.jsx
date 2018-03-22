import React, {Component} from "react";
import {Treemap} from "d3plus-react";
import mondrianClient from "helpers/mondrian";
import continents from "data/attr_continent.json";
import "pages/Profile/Profile.css";

export default class SectionDestinations extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: null
    };
  }

  // componentDidMount() {
  //   console.log("SectionDestinations Triggered!");
  //   mondrianClient
  //     .cube("2015_2016_hs_rev2007_yearly_data")
  //     .then(cube => {
  //       const qry = cube.query
  //         .drilldown("Destination Country", "Country")
  //         // .caption("Destination Country", "Country", "Country ES")
  //         .option("parents", true)
  //         .measure("Exports")
  //         .cut("[Origin Country].[Countries].[Country].&[pak]")
  //         .cut("[year].[year].[year].&[2016]");
  //       return Promise.all([mondrianClient.query(qry, "jsonrecords"), Promise.resolve(qry.path("csv"))]);
  //     })
  //     .then(([apiData]) => {
  //       console.log("SectionDestinations", apiData.data.data);
  //       this.setState({data: apiData.data.data});
  //     });
  // }

  render() {
    const {tradeByDestination} = this.props;
    return (
      <section>
        <aside>
          <a name="Destinations" className="anchor"></a>
          <h2>Destinations</h2>
          <p>In 2016 Pakistan exported $20.5B, making it the 54th largest exporter in the world. During the last five years the exports of Pakistan have decreased at an annualized rate of -7.018%, from $29.1B in 2011 to $20.5B in 2016. The most recent exports are led by <a href="/en/profile/hs92/6302/">House Linens</a> which represent 14.6% of the total exports of Pakistan, followed by <a href="/en/profile/hs92/1006/">Rice</a>, which account for 8.31%.</p>
          <p>
            <a className="explore-link" href="/en/visualize/tree_map/hs92/export/pak/all/show/2016/" target="_blank">Explore on Visualizations page <i className="fa fa-external-link"></i></a>
            <a className="explore-link" href="/en/resources/data/" target="_blank">Data Sources <i className="fa fa-external-link"></i></a>
          </p>
          <div className="share_container">
            <div className="share_icons_container">
              <a href="https://twitter.com/share?url=http://atlas.media.mit.edu/en/visualize/tree_map/hs92/export/pak/all/show/2016/&amp;text=Products exported by Pakistan (2016)&amp;hashtags=oec" title="Share on Twitter">
                <i className="fa fa-twitter"></i>
              </a>
              <a href="http://www.facebook.com/dialog/feed?caption=The Observatory of Economic Complexity&amp;display=popup&amp;app_id=426745600805300&amp;name=Products exported by Pakistan (2016)&amp;link=http://atlas.media.mit.edu/en/visualize/tree_map/hs92/export/pak/all/show/2016/&amp;redirect_uri=http://atlas.media.mit.edu/close/&amp;picture=http://atlas.media.mit.edu/static/img/facebook.jpg" title="Share on Facebook">
                <i className="fa fa-facebook"></i>
              </a>
              <a href="#" className="share_toggle" data-target="share_short_url" title="Direct URL">
                <i className="fa fa-link"></i>
              </a>
              <a href="#" className="share_toggle" data-target="share_embed_url" title="Embed URL">
                <i className="fa fa-image"></i>
              </a>
            </div>
            <div className="share_input_container">
              <input className="share_input share_short_url" type="text" value="http://atlas.media.mit.edu/en/visualize/tree_map/hs92/export/pak/all/show/2016/" />
              <input className="share_input share_embed_url" type="text" value="<iframe width=&quot;560&quot; height=&quot;315&quot; src=&quot;http://atlas.media.mit.edu/en/visualize/embed/tree_map/hs92/export/pak/all/show/2016/?controls=false&quot; frameborder=&quot;0&quot; ></iframe>" />
            </div>
          </div>
        </aside>
        <content>
          {tradeByDestination
            ? <Treemap ref={comp => this.viz = comp} config={{
              data: tradeByDestination,
              groupBy: ["Continent", "Country"],
              sum: d => d.Exports,
              height: 650,
              shapeConfig: {
                fill: d => {
                  const continent = continents.find(c => c.id === d.Continent);
                  return continent ? continent.color : "#C7C7C7";
                }
              }
            }} />
            : <div>Loading...</div>}
        </content>
      </section>
    );
  }

}
