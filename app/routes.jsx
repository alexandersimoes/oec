import React from "react";
import {Route, IndexRoute, browserHistory} from "react-router";

import App from "./App";
import Home from "./pages/Home";
import Profile from "./pages/Profile/Index";
import Country from "./pages/Profile/Country/Index";
import Product from "./pages/Profile/Product/Index";
import Publications from "./pages/Publications";

export default function RouteCreate() {
  function genRandId(path) {
    let candidates;
    if (path.includes("country")) {
      candidates = ["ind", "gbr", "fra", "ita", "chl", "bra", "bul", "tha", "idn", "phl", "can"];
    }
    else if (path.includes("/hs92")) {
      candidates = ["5810", "0810", "4812"];
    }
    return candidates[Math.floor(Math.random() * candidates.length)];
  }

  function checkForId(nextState, replace) {
    if (!nextState.params.id) {
      const reqestedUrl = nextState.location.pathname;
      const randId = genRandId(reqestedUrl);
      const nextUrl = reqestedUrl.slice(-1) === "/" ? `${reqestedUrl}${randId}` : `${reqestedUrl}/${randId}`;
      return replace({pathname: nextUrl});
    }
    else {
      // make sure it's legal
      // return NotFound;
      return console.log("Not Found!");
    }
  }

  return (
    <Route path="/" component={App} history={browserHistory}>
      <IndexRoute component={Home} />

      <Route path=":lang/profile" component={Profile}>
        <Route path="country(/:id)" component={Country} onEnter={checkForId} />
        <Route path="hs92(/:id)" component={Product} onEnter={checkForId} />
      </Route>

      <Route path="publications" component={Publications} />

    </Route>
  );
}
