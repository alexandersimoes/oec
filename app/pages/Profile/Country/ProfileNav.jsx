import React, {Component} from "react";
import "pages/Profile/Country/ProfileNav.css";

export default class ProfileNav extends Component {

  render() {
    return (
      <aside>
        <ul className="hierarchy contents country">
          <li className="depth2">Visualizations</li>
          <li className="depth6"><a href="#Exports">Exports</a></li>
          <li className="depth6"><a href="#Imports">Imports</a></li>
          <li className="depth6"><a href="#Trade_Balance">Trade Balance</a></li>
          <li className="depth6"><a href="#Destinations">Destinations</a></li>
          <li className="depth6"><a href="#Origins">Origins</a></li>
          <li className="depth6"><a href="#Product_Space">Product Space</a></li>
          <li className="depth6"><a href="#Complexity_and_Income_Inequality">Complexity and Income Inequality</a></li>
          <li className="depth6"><a href="#Economic_Complexity_Ranking">Economic Complexity Ranking</a></li>
        </ul>
      </aside>
    );
  }

}
