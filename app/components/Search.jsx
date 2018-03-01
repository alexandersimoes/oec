import React, {Component} from "react";
import {connect} from "react-redux";
import {translate} from "react-i18next";
import {activateSearch} from "actions/search";
import "components/Search.css";

class Search extends Component {

  deactivateSearch = () => {
    this.props.activateSearch(false);
  }

  render() {
    const {t, searchActive} = this.props;
    return (
      <div id="search" className={`${searchActive ? "open" : "close" }`}>

        <div id="search_close" onClick={this.deactivateSearch}>
          <img src="/images/nav/x.png" alt="close search" />
          <div>[ esc ]</div>
        </div>

        <div id="search_div">
          <input id="search_input" type="text" placeholder={ t("Search") } />
          <div id="search_modes">
            <div className="pt-button-group pt-minimal pt-large">
              <button className="pt-button pt-icon-disable" tabIndex="0" role="button">{ t("No Filter") }</button>
              <button className="pt-button pt-icon-globe" tabIndex="0" role="button">{ t("Countries") }</button>
              <button className="pt-button pt-icon-box" tabIndex="0" role="button">{ t("Products") }</button>
              <button className="pt-button pt-icon-timeline-area-chart" tabIndex="0" role="button">{ t("Visualizations") }</button>
            </div>
          </div>
        </div>
        <div id="search_results"></div>

      </div>
    );
  }

}

const mapStateToProps = state => ({
  searchActive: state.search.searchActive
});

const mapDispatchToProps = dispatch => ({
  activateSearch: searchActive => {
    dispatch(activateSearch(searchActive));
  }
});

Search = translate()(Search);
Search = connect(mapStateToProps, mapDispatchToProps)(Search);
export default Search;
