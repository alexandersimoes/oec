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
            <select id="search_mode_selector">
              <option value="all" selected>{ t("No Filter") }</option>
              <option value="country">{ t("Countries") }</option>
              <option value="hs92">{ t("Products") }</option>
              <option value="explore">{ t("Visualizations") }</option>
            </select>
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
