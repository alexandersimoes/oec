import React, {Component} from "react";
import {translate} from "react-i18next";
import {Dialog} from "@blueprintjs/core";
import "./Home.css";

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isVideoOpen: false
    };
  }

  toggleVideoOpen = () => this.setState({isVideoOpen: !this.state.isVideoOpen});

  render() {
    const {t} = this.props;

    return (
      <div id="Home">
        <div id="launch">

          <Dialog
            isOpen={this.state.isVideoOpen}
            onClose={this.toggleVideoOpen}
          >
            <div className="pt-dialog-body">
              <iframe id="vimeo_embed" src="https://player.vimeo.com/video/141271203?autoplay=0&api=1&color=ffffff&title=0&byline=0&portrait=0" width="700" height="394" frameBorder="0" allowFullScreen></iframe>
            </div>
          </Dialog>
        </div>
        <div className="bg-frame">
          <div className="ring-pulse"></div>
          <div className="ring-pulse echo-ring"></div>
          <div id="ring">
            <img src="/images/home/stars.png" className="star-rotate" />
            <img id="big_logo" src="/images/home/logo.png" alt="{{ _('The Observatory of Economic Complexity') }}" />
            <img id="observatory" src="/images/home/observatory.png" />
            <p id="info">
              {t("We are the world's leading visualization engine for international trade data.")}
              <br />
              <a href="/">{t("Learn More")}</a>
            </p>
            <div id="launch_vid" title="Launch video" onClick={this.toggleVideoOpen}>
              <img src="/images/home/play.png" alt="launch video" />
              <span>{t("Watch a video")}</span>
            </div>
            <div id="search_home">
              <img src="/images/nav/search.png" />
              { t("Search") }
            </div>
          </div>
        </div>
      </div>
    );
  }

}

export default translate()(Home);
