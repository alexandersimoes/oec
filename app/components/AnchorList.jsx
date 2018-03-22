import React from "react";
import {Link} from "react-router";

const AnchorList = ({items, name, url}) =>
  <span>
    {items.map((item, index) =>
      <span key={index}>
        {index && index === items.length - 1 ? " and " : null }
        <Link to={url(item)}>{name(item)}</Link>
        {items.length !== 2 ? index < items.length - 1 ? ", " : null : null}
      </span>
    )}
  </span>;

export default AnchorList;
