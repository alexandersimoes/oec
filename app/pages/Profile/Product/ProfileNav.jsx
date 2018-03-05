import React, {Component} from "react";
import "pages/Profile/Country/ProfileNav.css";

export default class ProfileNav extends Component {

  render() {
    return (
      <aside>
        <ul className="hierarchy contents country">
          <li className="depth2">Visualizations</li>
          <li className="depth6"><a href="#Exporters">Exporters</a></li>
          <li className="depth6"><a href="#Imports">Importers</a></li>
        </ul>
      </aside>
    );
  }

}
