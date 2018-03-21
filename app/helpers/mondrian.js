import {Client as MondrianClient} from "mondrian-rest-client";

const CUBE_API = "http://oeccube.datawheel.us:9292/";
const client = new MondrianClient(CUBE_API);

export default client;
