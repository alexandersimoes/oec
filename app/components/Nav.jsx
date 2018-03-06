import React, {Component} from "react";
import {connect} from "react-redux";
import {translate} from "react-i18next";
import {Popover, PopoverInteractionKind, Position, Button} from "@blueprintjs/core";
import {activateSearch} from "actions/search";
import "components/Nav.css";

class Nav extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isAboutMenuOpen: false,
      isRankingsMenuOpen: false
    };
  }

  activateSearch = () => {
    this.props.activateSearch(true);
  }

  render() {
    const {t, searchActive} = this.props;
    const {isAboutMenuOpen, isRankingsMenuOpen} = this.state;

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
            <Popover
              isOpen={isRankingsMenuOpen}
              onInteraction={state => this.setState({isRankingsMenuOpen: state})}
              popoverClassName="pt-minimal"
              position={Position.BOTTOM_LEFT}
              interactionKind={PopoverInteractionKind.HOVER}
            >
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
            </Popover>
          </li>

          <li id="publications">
            <a href="/publications/">{ t("Publications") }</a>
          </li>

          <li id="resources">
            <Popover
              isOpen={isAboutMenuOpen}
              onInteraction={state => this.setState({isAboutMenuOpen: state})}
              popoverClassName="pt-minimal"
              position={Position.BOTTOM_LEFT}
              interactionKind={PopoverInteractionKind.HOVER}
            >
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
            </Popover>
          </li>


          <li id="api">
            <a href="/api">{ t("API") }</a>
          </li>
        </ul>

        <div id="search_button" onClick={this.activateSearch}>
          <img src="/images/nav/search.png" />
        </div>

      </nav>
    );
  }

}

// export default connect(state => ({
//   searchActive: state.search.searchActive
// }))(translate()(Nav));

const mapStateToProps = state => ({
  searchActive: state.search.searchActive
});

const mapDispatchToProps = dispatch => ({
  activateSearch: searchActive => {
    dispatch(activateSearch(searchActive));
  }
});

Nav = translate()(Nav);
Nav = connect(mapStateToProps, mapDispatchToProps)(Nav);
export default Nav;
