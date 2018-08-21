import React, {Component} from "react";
import {abbreviate} from "helpers/formatters";
import AnchorList from "components/AnchorList";
import "pages/Profile/Country/ProfileSummary.css";

export default class ProfileSummary extends Component {

  // ¶ 1 Sentence 1
  // This takes the form of:
  //  "<Country> is the <ordinal-rank> largest export economy in the world."
  // An example would be:
  //  "Pakistan is the 54th largest export economy in the world."
  p1s1 = (country, tradeByCountry) => {
    const thisCountryIndex = tradeByCountry
      .sort((a, b) => b.Exports - a.Exports)
      .findIndex(c => c["ID Country"] === country.id);
    // console.log(tradeByCountry, country, thisCountryIndex);
    // return "test";
    return `${country.comtrade_name} is the ${thisCountryIndex + 1}th largest export economy in the world. `;
  }

  // ¶ 1 Sentence 2
  // This takes the form of:
  //  "In 2016, <country> exported <exports> and imported <imports>, resulting in a <positive|negative> trade balance of <abs(exports-imports)>."
  // An example would be:
  //  "In 2016, Pakistan exported $20.5B and imported $45.9B, resulting in a negative trade balance of $25.5B."
  p1s2 = (country, tradeByCountry) => {
    // "test2"
    const thisCountry = tradeByCountry.find(c => c["ID Country"] === country.id);
    const tradeDiff = thisCountry.Exports - thisCountry.Imports;
    const positiveOrNegative = tradeDiff >= 0 ? "positive" : "negative";
    return `
      In 2016, ${country.comtrade_name} exported $${abbreviate(thisCountry.Exports)}
      and imported $${abbreviate(thisCountry.Imports)}, resulting in a ${positiveOrNegative}
      trade balance of $${abbreviate(Math.abs(tradeDiff))}. `;
  }
  

  // ¶ 1 Sentence 3
  // This takes the form of:
  //  "In 2016, the GDP of <country> was <gdp> and its GDP per capita was <gdp_per_capita>."
  // An example would be:
  //  "In 2016 the GDP of Pakistan was $283B and its GDP per capita was $5.25k."
  p1s3 = country => `In 2016 the GDP of ${country.comtrade_name} was $XXX and its GDP per capita was $XXX.`

  //
  // ¶ 3 Sentence 1
  // This takes the form of:
  //  "The top export destinations of <country> are <list_of_destinations>."
  // An example would be:
  //  "The top export destinations of Pakistan are <a href="/en/profile/country/usa/">the United States</a> ($3.43B), <a href="/en/profile/country/chn/">China</a> ($1.59B), <a href="/en/profile/country/gbr/">the United Kingdom</a> ($1.56B), <a href="/en/profile/country/afg/">Afghanistan</a> ($1.37B) and <a href="/en/profile/country/deu/">Germany</a> ($1.19B). The top import origins are <a href="/en/profile/country/chn/">China</a> ($17.2B), <a href="/en/profile/country/usa/">the United States</a> ($2.11B), <a href="/en/profile/country/idn/">Indonesia</a> ($2.02B), <a href="/en/profile/country/jpn/">Japan</a> ($1.93B) and <a href="/en/profile/country/ind/">India</a> ($1.59B)."
  // p3s1 = (country, tradeByCountry) => {
  //   return <span></span>;
  // }

  render() {
    const {country, tradeByCountry, tradeByDestination, tradeByProduct} = this.props;

    if (!tradeByDestination.length || !tradeByProduct.length) {
      return <div>...</div>;
    }

    return (
      <content className="summary">
        <div className="columns">
          <p>
            {this.p1s1(country, tradeByCountry)}
            {this.p1s2(country, tradeByCountry)}
            {this.p1s3(country)}
          </p>
          <p>
            The top exports of {country.comtrade_name} are <AnchorList items={tradeByProduct.sort((a, b) => b.Exports - a.Exports).slice(0, 3)} name={d => `${d.HS4} ($${abbreviate(d.Exports)})`} url={d => `/en/profile/country/${d["ID Product"]}`} />
            Its top imports are .</p>
          <p>
            The top export destinations of {country.comtrade_name} are <AnchorList items={tradeByDestination.sort((a, b) => b.Exports - a.Exports).slice(0, 3)} name={d => `${d.Country} ($${abbreviate(d.Exports)})`} url={d => `/en/profile/country/${d["ID Country"]}`} />.
          </p>
          <p>Pakistan borders <a href="/en/profile/country/afg/">Afghanistan</a>, <a href="/en/profile/country/chn/">China</a>, <a href="/en/profile/country/ind/">India</a> and <a href="/en/profile/country/irn/">Iran</a> by land and <a href="/en/profile/country/omn/">Oman</a> by sea.</p>
        </div>
      </content>
    );
  }

}
