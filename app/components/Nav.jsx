import React, {Component} from "react";
import {translate} from "react-i18next";
import "components/Nav.css";

class Nav extends Component {

  render() {
    const {t} = this.props;
    return (
      <nav>

        <a id="hamburger">
          <img id="hamburger_button" src="/images/nav/menu.png" />
        </a>

        <a id="logo" href="/">
          <img src="/images/nav/logo-sm.png" alt={t("The Observatory of Economic Complexity")} />
        </a>

        <ul className="navLinks">
          <li id="country">
            <a href="/en/profile/country">{ t("Countries") }</a>
          </li>

          <li id="product">
            <a href="/en/profile/hs92">{ t("Products") }</a>
          </li>

          <li id="explore">
            <a href="/en/visualize">{ t("Visualizations") }</a>
          </li>

          <li id="rankings">
            <a href="/rankings/eci">{ t("Rankings") }</a>
            <div className="sub_menu">
              <ul>
                <li className="country">
                  <a href="/rankings/country">{ t("Countries") }</a>
                </li>
                <li className="product">
                  <a href="/rankings/sitc">{ t("Products") }</a>
                </li>
              </ul>
            </div>
          </li>

          <li id="publications">
            <a href="/publications/">{ t("Publications") }</a>
          </li>

          <li id="resources">
            <a href="/en/resources/about/">{ t("About") }</a>
            <div className="sub_menu">
              <ul>
                <li className="data">
                  <a href="/en/resources/data/">{ t("Data") }</a>
                </li>
                <li className="methodology">
                  <a href="/en/resources/methodology/">{ t("Methodology") }</a>
                </li>
                <li className="about">
                  <a href="/en/resources/about/">{ t("The Site") }</a>
                </li>
                <li className="permissions">
                  <a href="/en/resources/permissions">{ t("Permissions") }</a>
                </li>
                <li className="faqs">
                  <a href="/en/resources/faqs">{ t("FAQs") }</a>
                </li>
              </ul>
            </div>
          </li>

          <li id="api">
            <a href="/api">{ t("API") }</a>
          </li>
        </ul>

        <div id="search_button">
          <img src="/images/nav/search.png" />
        </div>

      </nav>
    );
  }

}

export default translate()(Nav);
