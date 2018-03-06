import React, {Component} from "react";
import {translate} from "react-i18next";

class Site extends Component {
  constructor(props) {
    super(props);
    this.currentTeam = [
      {
        name: "Alexander Simoes",
        slug: "alexander_simoes",
        time: "2010 – Present",
        text: "Alex is the lead developer on the Observatory project. He has been working in the Macro Connections group developing technologies to better inform policy and decision makers by equipping them with tools to make sense of large datasets.",
        links: [
          {type: "github", url: "https://github.com/alexandersimoes"},
          {type: "twitter", url: "https://twitter.com/ximoes"},
          {type: "linkedin", url: "http://www.linkedin.com/pub/alex-simoes/42/71a/728"}
        ]
      },
      {
        name: "Dave Landry",
        slug: "dave_landry",
        time: "2012 – Present",
        text: "Dave designed the 2013 version of the website, along with being co-author of the underlying visualization engine <a href='http://www.d3plus.org' target='_blank'>D3plus</a>. He continues to support the site with improvements to the front-end in both the visualizations and the overall navigation.",
        links: [
          {type: "github", url: "https://github.com/davelandry"},
          {type: "twitter", url: "https://twitter.com/davelandry"},
          {type: "linkedin", url: "http://www.linkedin.com/in/davelandry/"}
        ]
      },
      {
        name: "César Hidalgo",
        slug: "cesar_hidalgo",
        time: "2010 – Present",
        text: "César is the Asahi Broadcast Corporation Career Development Professor and an Associate Professor at the MIT Media Lab. His work focuses on improving the understanding of systems using and developing concepts of complexity, evolution and network science.",
        links: [
          {type: "twitter", url: "https://twitter.com/cesifoti"},
          {type: "linkedin", url: "http://www.linkedin.com/pub/cesar-a-hidalgo/5/30a/a61"}
        ]
      }
    ];

    this.formerTeam = [
      {
        name: "Melissa Teng",
        slug: "melissa_teng",
        time: "2015 – Present",
        text: "Melissa led the 2015 redesign of the website, focusing on a humanist approach to data. She built on the site's visual identity and user experience, as well as supported some front-end development.",
        links: [
          {type: "github", url: "https://github.com/melteng"},
          {type: "twitter", url: "https://twitter.com/melisteng"},
          {type: "linkedin", url: "http://www.linkedin.com/in/mqteng/"}
        ]
      },
      {
        name: "Eric Franco",
        slug: "eric_franco",
        time: "2012 – 2013",
        text: "Eric was responsible for maintaining the site and incorporating new data as it became available.",
        links: [
          {type: "github", url: "https://github.com/ericjohnf"},
          {type: "linkedin", url: "http://www.linkedin.com/in/ericjohnf"}
        ]
      },
      {
        name: "Sarah Chung",
        slug: "sarah_chung",
        time: "2011 – 2012",
        text: "Sarah worked on developing algorithms for cleaning the raw SITC bilateral trade used on the site.",
        links: [
          {type: "linkedin", url: "http://www.linkedin.com/in/sarahchung7/"}
        ]
      },
      {
        name: "Crystal Noel",
        slug: "crystal_noel",
        time: "2011 – 2012",
        text: "Crystal helped improve some of the original visualizations and code-base.",
        links: [
          {type: "twitter", url: "https://twitter.com/crystalMIT13"}
        ]
      },
      {
        name: "Ali Almossawi",
        slug: "ali_almossawi",
        time: "2010 – 2011",
        text: "Ali was instrumental in the initial design, programming, and launch of The Observatory.",
        links: [
          {type: "github", url: "https://github.com/almossawi"},
          {type: "twitter", url: "https://twitter.com/alialmossawi"},
          {type: "linkedin", url: "http://www.linkedin.com/in/almossawi"}
        ]
      }
    ];
  }

  render() {
    const {t} = this.props;
    return (
      <content>
        <h1>{ t("About the Observatory") }</h1>
        <p>
          The Observatory of Economic Complexity is a tool that allows users to quickly compose a visual narrative about countries and the products they exchange. It was Alexander Simoes' Master Thesis in Media Arts and Sciences at the MIT Media Lab, which you can read <a href="http://macroconnections.media.mit.edu/papers/SimoesMasterThesis.pdf" alt="Alex Simoes' MIT Master's Thesis on Observatory of Economic Complexity">here</a>.
        </p>
        <p>
          The project was conducted at The MIT Media Lab <a href="http://macroconnections.media.mit.edu/">Macro Connections</a> group. Alex’s Advisor was <a href="http://chidalgo.com">César A. Hidalgo</a>, principal investigator of the Collective Learning Group. Since its creation in 2010, the development of The Observatory of Economic Complexity has been supported by The MIT Media Lab consortia for undirected research.
        </p>
        <p>
          For a history of the contributions to The Observatory of Economic Complexity, you can <a href="https://github.com/alexandersimoes/atlas_economic_complexity/network">view the project’s contributions timeline on Github</a>. A predecessor of the Observatory of Economic Complexity is the <a href="http://chidalgo.com/productspace/index.htm">product space site</a>, built by César Hidalgo as a graduate student at Notre Dame in 2007.
        </p>
        <p>
          If you would like more info on the OEC or to create a similar site for your country, state, or city, get in touch with us at <a href="mailto:oec@media.mit.edu">oec@media.mit.edu</a>.
        </p>

        <h2>{ t("Current Team") }</h2>
        {this.currentTeam.map(member =>
          <div key={member.slug} className="member" id={ member.slug }>
            <img className="face" src={`/images/about/${member.slug}.png`} />
            <h3>
              {member.name}
              {member.links.map(link =>
                <a key={link.type} href={link.url} alt={member.slug} target="_blank">
                  <img className="icon" src={`/images/icons/${link.type}.svg`} alt={`${link.type} icon`} />
                </a>
              )}
            </h3>
            <h4>{member.time}</h4>
            <p dangerouslySetInnerHTML={{__html: member.text}}></p>
          </div>
        )}

        <h2>{ t("Past Contributors") }</h2>
        <div id="past">
          {this.formerTeam.map(member =>
            <div key={member.slug} className="member" id={ member.slug }>
              <img className="face" src={`/images/about/${member.slug}.png`} />
              <h3>
                {member.name}
                {member.links.map(link =>
                  <a key={link.type} href={link.url} alt={member.slug} target="_blank">
                    <img className="icon" src={`/images/icons/${link.type}.svg`} alt={`${link.type} icon`} />
                  </a>
                )}
              </h3>
              <h4>{member.time}</h4>
              <p dangerouslySetInnerHTML={{__html: member.text}}></p>
            </div>
          )}
        </div>
      </content>
    );
  }

}

export default translate()(Site);
