import React, {Component} from "react";
import Nav from "components/Nav";
import Footer from "components/Footer";
import Search from "components/Search";
import "./App.css";

export default class App extends Component {

  render() {
    return (
      <div>
        <Search />
        <Nav />
        <div id="container">
          {this.props.children}
          <Footer />
        </div>
      </div>
    );
  }

}
