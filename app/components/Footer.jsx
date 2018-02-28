import React, {Component} from "react";
import {LANGUAGES} from "helpers/config";
import "components/Footer.css";

export default class Footer extends Component {

  render() {
    return (
      <footer>
        <div className="top-footer">
          <div className="top-footer-links">
            <a id="mc" href="http://macro.media.mit.edu/" target="_blank">
              <img src="/images/nav/collective-learning-mit-media-lab.png" />
            </a>
            <a id="donate" href="https://giving.mit.edu/search/node/2743736" target="_blank">
              <span className="pt-icon-standard pt-icon-heart"></span> Donate
            </a>
          </div>
        </div>

        <div>
          <ul className="lang">
            {LANGUAGES.map(l =>
              <li key={l.id}><a href={`/${l.id}`}>{l.name}</a></li>
            )}
          </ul>
          The Observatory of Economic Complexity by
          <a href="http://alexandersimoes.com/" property="cc:attributionName" rel="cc:attributionURL">Alexander Simoes</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/">Creative Commons Attribution-ShareAlike 3.0 Unported License</a>. Permissions beyond the scope of this license may be available <a href="/permissions/" rel="cc:morePermissions">here</a>.
          <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/">
            <img alt="Creative Commons License" style={{borderWidth: 0}} src="https://i.creativecommons.org/l/by-sa/3.0/80x15.png" />
          </a>
        </div>

      </footer>
    );
  }

}
