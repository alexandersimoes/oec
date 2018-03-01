import {combineReducers} from "redux";

const searchActive = (state = false, action) => {
  switch (action.type) {
    case "ACTIVATE_SEARCH":
      return action.activate ? action.activate : !state;
    default:
      return state;
  }
};

export default {search: combineReducers({searchActive})};
