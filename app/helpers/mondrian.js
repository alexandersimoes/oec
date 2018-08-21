import {Client as MondrianClient} from "mondrian-rest-client";

const CUBE_API = "https://oec-sandbox.datawheel.us/";
const client = new MondrianClient(CUBE_API);

export default client;
