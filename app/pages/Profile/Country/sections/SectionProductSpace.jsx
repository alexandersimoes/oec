import React, {Component} from "react";
import {Network} from "d3plus-react";
import "pages/Profile/Profile.css";

const nodes = [
  {id: "alpha",   x: 1,   y: 1},
  {id: "beta",    x: 2,   y: 1},
  {id: "gamma",   x: 1,   y: 2},
  {id: "epsilon", x: 3,   y: 2},
  {id: "zeta",    x: 2.5, y: 1.5},
  {id: "theta",   x: 2,   y: 2}
];

const links = [
  {source: 0, target: 1},
  {source: 0, target: 2},
  {source: 3, target: 4},
  {source: 3, target: 5},
  {source: 5, target: 0}
];

export default class SectionProductSpace extends Component {

  render() {
    return (
      <section>
        <aside>
          <a name="Product-Space" className="anchor"></a>
          <h2>Product Space</h2>
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
          <Network ref={comp => this.viz = comp} config={{
            nodes,
            links,
            height: 650
          }} />
        </content>
      </section>
    );
  }

}
